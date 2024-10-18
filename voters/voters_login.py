from flask import render_template, request, flash, redirect, url_for, session
from . import voter_bp
from .. import mongo

@voter_bp.route('/login', methods=['GET', 'POST'])
def login_voter():
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        password = request.form.get('password')

        if not voter_id or not password:
            flash('Both Voter ID and Password are required!', 'error')
            return redirect(url_for('login_voter'))

        voter = mongo.db.voters.find_one({'voter_id': voter_id})

        if voter and check_password_hash(voter['password'], password):
            session['name'] = voter.get('name')

            flash('Login successful!', 'success')
            return redirect(url_for('voter_dashboard'))  
        else:
            flash('Invalid Voter ID or password!', 'error')

    return render_template('login_voter.html')  
