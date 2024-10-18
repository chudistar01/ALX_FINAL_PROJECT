from flask import render_template, request, flash, redirect, url_for, session
from . import admin_bp
from .. import mongo

@admin_bp.route('/admin/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        # Get form data
        admin_id = request.form.get('admin_id')
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the data (basic example)
        if not admin_id or not username or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register_admin'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new admin document
        admin_data = {
            'admin_id': admin_id,
            'username': username,
            'password': hashed_password  # Store hashed password for security
        }

        # Insert the admin document into the MongoDB collection
        mongo.db.admins.insert_one(admin_data)

        # Flash a success message
        flash('Admin user created successfully!', 'success')
        return redirect(url_for('register_admin'))  # Redirect after POST

    return render_template('register_admin.html')  # Render form template

# Example route for testing MongoDB connection
