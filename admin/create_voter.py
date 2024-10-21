from flask import render_template, request, flash, redirect, url_for, session
from . import admin_bp
from .. import mongo

@admin_bp.route('/create_voter', methods=['GET', 'POST'])
def create_voter():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login_admin'))

    if request.method == 'POST':
        # Get form data
        voter_id = request.form.get('voter_id')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')  # Password for the voter

        # Validate the data
        if not voter_id or not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('create_voter'))

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Create a new voter document
        voter_data = {
            'voter_id': voter_id,
            'name': name,
            'email': email,
            'password': hashed_password  # Store hashed password
        }

        # Insert the voter document into the MongoDB collection
        mongo.db.voters.insert_one(voter_data)

        # Flash a success message
        flash('Voter created successfully!', 'success')
        return redirect(url_for('create_voter'))  # Redirect after POST

    return render_template('create_voter.html')  # Render form template
