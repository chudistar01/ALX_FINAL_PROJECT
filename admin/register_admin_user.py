from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from . import admin_bp
from ..extensions import mongo
from bson.objectid import ObjectId  # Import ObjectId if using MongoDB's ObjectId for admin_id

MAX_ADMINS = 5

@admin_bp.route('/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        # Check the current count of admins
        current_admin_count = mongo.db.admins.find().count()

        if current_admin_count >= MAX_ADMINS:
            flash('Maximum number of admin users reached. Cannot add more.', 'error')
            return redirect(url_for('admin.register_admin'))

        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the data
        if not username or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.register_admin'))

        # Check if the username already exists
        existing_admin = mongo.db.admins.find_one({'username': username})
        if existing_admin:
            flash('Username already exists!', 'error')
            return redirect(url_for('admin.register_admin'))

        # Generate a unique admin ID if required
        admin_id = str(ObjectId())  # Generate an ObjectId as a unique identifier

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new admin document
        admin_data = {
            'admin_id': admin_id,
            'username': username,
            'password': hashed_password
        }

        # Insert the admin document into the MongoDB collection
        try:
            mongo.db.admins.insert_one(admin_data)
            flash('Admin user created successfully!', 'success')
            return redirect(url_for('admin.login_admin')) 
        except Exception as e:
            flash(f'An error occurred while creating the admin user: {e}', 'error')
            return redirect(url_for('admin.register_admin'))

    return render_template('register_admin.html')  # Render the form template
