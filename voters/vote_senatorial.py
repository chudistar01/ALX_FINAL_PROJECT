from flask import render_template, request, flash, redirect, url_for, session
from ..extensions  import mongo
from . import voters_bps

@voters_bps.route('/senatorial', methods=['GET', 'POST'])
def vote_senatorial():
    if 'voter_id' not in session:  # Check if the user is logged in
        flash('Please log in to vote.', 'error')
        return redirect(url_for('voters.login_voter'))  # Redirect to login if not logged in

    voter_id = session['voter_id']
    voter = mongo.db.voters.find_one({'voter_id': voter_id})

    if request.method == 'POST':
        # Retrieve selected candidate from form
        candidate = request.form.get('candidate')
        
        if not candidate:
            flash('Please select a candidate to vote for!', 'error')
            return redirect(url_for('voters.vote_senatorial'))

        # Record the vote in MongoDB
        mongo.db.votes.insert_one({
            'voter_id': voter_id,
            'election_type': 'senatorial',
            'candidate': candidate
        })
        
        flash('Your senatorial vote has been recorded!', 'success')
        return redirect(url_for('voters.dashboard'))  # Redirect to dashboard after voting

    return render_template('vote_senatorial.html', voter=voter)  # Render the voting form