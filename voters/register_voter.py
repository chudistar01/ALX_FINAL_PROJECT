from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash  # Import for password hashing
from ..extensions import mongo
import uuid  # Don't forget to import uuid
from . import voters_bps

@voters_bps.route('/registers_voters', methods=['GET', 'POST'])
def registers_voters():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')  # Corrected indentation

        if not username or not password:
            flash('Both username and password are required!', 'error')
            return redirect(url_for('voters.registers_votersters'))

        # Check if the username already exists
        existing_voter = mongo.db.voters.find_one({'username': username})
        if existing_voter:
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('voters.registers_voters'))


        # Generate a unique voter ID using UUID
        voter_id = str(uuid.uuid4())

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)

        # Store the new voter in the database
        mongo.db.voters.insert_one({
            'voter_id': voter_id,
            'username': username,
            'password': hashed_password
        })

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('voters.login_voter'))

    return render_template('register_voter.html')
