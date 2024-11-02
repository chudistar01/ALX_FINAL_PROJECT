from flask import render_template, request, session, flash, redirect, url_for
from ..extensions  import mongo
from . import voters_bps 
from datetime import datetime

@voters_bps.route('/vote_house_of_reps', methods=['GET', 'POST'])
def vote_house_of_reps():
    # Ensure the voter is logged in
    if 'voter_id' not in session:
        flash('Please log in to vote', 'error')
        return redirect(url_for('voters.login_voter'))

    # Retrieve the voter's information from the database
    voter = mongo.db.voters.find_one({"voter_id": session['voter_id']})
    if not voter:
        flash('Voter not found', 'error')
        return redirect(url_for('voters.login_voter'))
    
    # Extract voter's location details from the database
    voter_state = voter.get('state_of_residence')
    voter_senatorial_district = voter.get('senatorial_district')
    voter_federal_constituency = voter.get('federal_constituency')

    # Retrieve House of Representatives candidates specific to the voter's area
    candidates = mongo.db.candidates.find({
        "election_type": "house_of_reps",
        "state": voter_state,
        "senatorial_district": voter_senatorial_district,
        "federal_constituency": voter_federal_constituency
    })

    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        
        # Check if a candidate was selected
        if not candidate_id:
            flash('Please select a candidate to vote for!', 'error')
            return redirect(url_for('voters.vote_house_of_reps'))

        # Check if the voter has already voted
        existing_vote = mongo.db.votes.find_one({
            "voter_id": session['voter_id'],
            "election_type": "house_of_reps",
            "state": voter_state,
            "senatorial_district": voter_senatorial_district,
            "federal_constituency": voter_federal_constituency
        })
        if existing_vote:
            flash('You have already voted in the House of Representatives election!', 'error')
            return redirect(url_for('voters.vote_house_of_reps'))

        # Record the vote
        mongo.db.votes.insert_one({
            "voter_id": session['voter_id'],
            "candidate_id": candidate_id,
            "election_type": "house_of_reps",
            "state": voter_state,
            "senatorial_district": voter_senatorial_district,
            "federal_constituency": voter_federal_constituency,
            "timestamp": datetime.utcnow()
        })

        flash('Your vote has been cast successfully!', 'success')
        return redirect(url_for('voters.dashboard'))  # Redirect to dashboard after voting

    return render_template('vote_house_of_reps.html', candidates=candidates)
