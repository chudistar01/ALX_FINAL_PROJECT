from flask import render_template, request, flash, redirect, url_for, session
from ..extensions import mongo
from . import voters_bps

@voters_bps.route('/vote_presidential', methods=['GET', 'POST'])
def vote_presidential():
    if 'voter_id' not in session:  # Check if the user is logged in
        flash('Please log in to vote.', 'error')
        return redirect(url_for('voters.login_voter'))  # Redirect to login if not logged in

    voter_id = session['voter_id']
    voter = mongo.db.voters.find_one({'voter_id': voter_id})

    # Fetch presidential candidates added by the admin
    candidates = list(mongo.db.candidates.find({'election_type': 'presidential'}))

    if request.method == 'POST':
        # Retrieve selected candidate from form
        candidate_id = request.form.get('candidate_id')
        
        if not candidate_id:
            flash('Please select a candidate to vote for!', 'error')
            return redirect(url_for('voters.vote_presidential'))

        # Record the vote in MongoDB
        mongo.db.votes.insert_one({
            'voter_id': voter_id,
            'election_type': 'presidential',
            'candidate_id': candidate_id
        })
        
        flash('Your presidential vote has been recorded!', 'success')
        return redirect(url_for('voters.dashboard'))  # Redirect to dashboard after voting

    return render_template('vote_presidential.html', voter=voter, candidates=candidates)  # Pass candidates to the template
