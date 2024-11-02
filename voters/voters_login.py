from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from ..extensions import mongo
from . import voters_bps


@voters_bps.route('/login', methods=['GET', 'POST'])
def login_voter():
    print("Loading voters_login")
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        password = request.form.get('password')

        # Check if both Voter ID and Password fields are filled
        if not voter_id or not password:
            flash('Both Voter ID and Password are required!', 'error')
            return redirect(url_for('voters.login_voter'))

        # Fetch voter details from the database using the Voter ID
        voter = mongo.db.voters.find_one({'voter_id': voter_id})

        # Check if voter exists and password is correct
        if voter and check_password_hash(voter['password'], password):
            # Store voter ID in session for future authentication checks
            session['voter_id'] = voter['voter_id']

            flash('Login successful!', 'success')
            return redirect(url_for('voters.dashboard'))  # Redirect to the voters' dashboard
        else:
            flash('Invalid Voter ID or password!', 'error')

    return render_template('login_voter.html')
