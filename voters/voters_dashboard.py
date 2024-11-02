from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash  # Import for password verification
from ..extensions import mongo 
from . import voters_bps

@voters_bps.route('/dashboard')
def dashboard():
    if 'voter_id' in session:  # Check if the user is logged in by voter ID
        voter_id = session['voter_id']
        voter = mongo.db.voters.find_one({'voter_id': voter_id})  # Fetch voter from MongoDB

        if voter:  # Render the dashboard if the voter is found
            return render_template('voter_dashboard.html', voter=voter)
        else:
            return redirect(url_for('voters.login_voter'))  # Redirect to login if voter not found
    else:
        return render_template('voter_dashboard_not_logged_in.html')  # Show a message if not logged in
