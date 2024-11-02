import os
from flask import Flask, render_template
import logging
from .extensions import mongo, mail, socketio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .admin import admin_bp  
from .voters import voters_bps  

logging.basicConfig(level=logging.INFO)


def check_elections(app):
    """Check for elections older than 24 hours and mark them as ended."""
    from flask_mail import Message  # Import inside the function to avoid circular imports
    now = datetime.utcnow()
    try:
        expired_elections = mongo.db.elections.find({
            "created_at": {"$lt": now - timedelta(hours=24)},
            "status": {"$ne": "ended"}
        })
        for election in expired_elections:
            mongo.db.elections.update_one({"_id": election["_id"]}, {"$set": {"status": "ended"}})
            logging.info(f"Election '{election.get('name', 'Unknown')}' marked as ended.")
            msg = Message("Election Ended Notification",
                          sender="your_email@example.com",
                          recipients=["admin_email@example.com"])  
            msg.body = f"The election '{election.get('name', 'Unknown')}' has ended."
            with app.app_context():
                mail.send(msg)
                logging.info("Sent email notification for ended election.")
    except Exception as e:
        logging.error(f"Error checking elections: {e}")



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI='mongodb://localhost:27017/voter_database',
        MAIL_SERVER='localhost',  # Configure your mail server
        MAIL_PORT=1025,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=False,
        MAIL_DEFAULT_SENDER='christianigwebuike30@gmail.com',
    )

    app.config['MAIL_SERVER'] = 'localhost'


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    mongo.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    app.register_blueprint(admin_bp) 
    app.register_blueprint(voters_bps)
 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: check_elections(app), trigger="interval", hours=1)
    scheduler.start()


    #@app.route('/')
    #def say_hello():
    #    return "Hello, World!"


    
    @app.route('/')
    def home():
        return render_template('home.html')

    #@app.route('/admins')
    #def admin_dashboard():
     #   return render_template('admin_dashboard.html')


    #@app.route('/voters/dashboard')
    #def voters_dashboard():
     #   return render_template('voter_dashboard.html')



    @app.route('/test_db')
    def test_db():
        try:
        # Use count() instead of count_documents()
            voter_count = mongo.db.voters.count()
            return f'Total registered voters: {voter_count}'
        except Exception as e:
            logging.error(f"Error retrieving voter count: {e}")
            return "An error occurred while retrieving voter count."

# Make sure to shut down the scheduler when exiting the app
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:  # Check if the scheduler is running before shutting down
            scheduler.shutdown()



    return app
