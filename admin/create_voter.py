from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from . import admin_bp
from ..extensions import mongo
from .. import mail
from flask_mail import Message
import uuid
import json
import os

# Load the states and local governments from the JSON file
def load_states_and_lgas():
    file_path = os.path.join(os.path.dirname(__file__), '../instance/states_and_lgas.json')
    with open(file_path, 'r') as file:
        states_and_lgas = json.load(file)
    return states_and_lgas


@admin_bp.route('/create_voter', methods=['GET', 'POST'])
def create_voter():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('admin.login_admin'))

    # Load states and LGAs to pass to the template
    states_and_lgas = load_states_and_lgas()

    if request.method == 'POST':
        # Generate a unique voter_id
        voter_id = str(uuid.uuid4())

        # Get form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        sex = request.form.get('gender')
        state_of_origin = request.form.get('state_of_origin')
        local_government_of_origin = request.form.get('local_government_of_origin')
        state_of_residence = request.form.get('state_of_residence')
        local_government_of_residence = request.form.get('local_government_of_residence')
        date_of_birth = request.form.get('DOB')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate the data
        if not all([first_name, middle_name, last_name, sex, state_of_origin, 
                    local_government_of_origin, state_of_residence,
                    local_government_of_residence, date_of_birth, email, 
                    password, confirm_password]):
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.create_voter'))

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('admin.create_voter'))

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Create a new voter document
        voter_data = {
            'voter_id': voter_id,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'sex': sex,
            'state_of_origin': state_of_origin,
            'local_government_of_origin': local_government_of_origin,
            'state_of_residence': state_of_residence,
            'local_government_of_residence': local_government_of_residence,
            'date_of_birth': date_of_birth,
            'email': email,
            'password': hashed_password  # Store hashed password
        }

        # Insert the voter document into the MongoDB collection
        mongo.db.voters.insert_one(voter_data)

        # Send confirmation email
        msg = Message('Voter Registration Successful',
                      sender='christianigwebuike30@gmail.com',
                      recipients=[email])
        msg.body = f"Thank you for registering! Your Voter ID is: {voter_id}"
        mail.send(msg)

        # Flash a success message
        flash('Voter created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))  # Redirect after POST

    return render_template('create_voter.html', states_and_lgas=states_and_lgas)  # Render form template
