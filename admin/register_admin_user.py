from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash  # Import the hashing function
from . import admin_bp
from .. import mongo

@admin_bp.route('/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        # Get form data
        admin_id = request.form.get('admin_id')
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the data (basic example)
        if not admin_id or not username or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('admin_bp.register_admin'))

        # Check if admin ID already exists
        existing_admin = mongo.db.admins.find_one({'admin_id': admin_id})
        if existing_admin:
            flash('Admin ID already exists!', 'error')
            return redirect(url_for('admin_bp.register_admin'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new admin document
        admin_data = {
            'admin_id': admin_id,
            'username': username,
            'password': hashed_password  # Store hashed password for security
        }

        # Insert the admin document into the MongoDB collection
        try:
            mongo.db.admins.insert_one(admin_data)
        except Exception as e:
            flash('An error occurred while creating the admin user: {}'.format(e), 'error')
            return redirect(url_for('admin_bp.register_admin'))

        # Flash a success message
        flash('Admin user created successfully!', 'success')
        #look later xxxxxxxx return redirect(url_for('admin_bp.some_other_route'))  # Change to a relevant route

    return render_template('register_admin.html')  # Render form template
