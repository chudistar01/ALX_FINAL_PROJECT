from flask import render_template, request, session, flash, redirect, url_for
from . import voters_bps
from ..extensions import mongo
from datetime import datetime  # Make sure to import datetime

@voters_bps.route('/gubernatorial', methods=['GET', 'POST'])
def vote_gubernatorial():
    # Ensure the voter is logged in
    if 'voter_id' not in session:
        flash('Please log in to vote', 'error')
        return redirect(url_for('voters.login_voter'))

    # Get the voter's information
    voter = mongo.db.voters.find_one({"voter_id": session['voter_id']})
    if voter is None:
        flash('Voter not found', 'error')
        return redirect(url_for('voters.login_voter'))

    state_of_residence = voter['state_of_residence']

    # Retrieve gubernatorial candidates in the voter's state of residence
    candidates = list(mongo.db.candidates.find({
        "election_type": "gubernatorial",
        "state": state_of_residence
    }))

    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')

        # Check if the voter has already voted for this election type
        if mongo.db.votes.find_one({"voter_id": session['voter_id'], "election_type": "gubernatorial"}):
            flash('You have already voted in this election!', 'error')
            return redirect(url_for('voters.vote_gubernatorial'))

        # Record the vote
        mongo.db.votes.insert_one({
            "voter_id": session['voter_id'],
            "candidate_id": candidate_id,
            "election_type": "gubernatorial",
            "state": state_of_residence,
            "timestamp": datetime.utcnow()
        })

        flash('Your vote has been cast successfully!', 'success')
        return redirect(url_for('voters.vote_gubernatorial'))

    # Pass the voter object to the template
    return render_template('vote_gubernatorial.html', candidates=candidates, voter=voter)
