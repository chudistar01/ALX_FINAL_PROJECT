from flask import render_template, request, flash, redirect, url_for, session
from . import admin_bp
from .. import mongo

@admin_bp.route('/register_candidate', methods=['GET', 'POST'])
def register_candidate():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login_admin'))

    if request.method == 'POST':
        # Get form data
        candidate_id = request.form.get('candidate_id')
        name = request.form.get('name')
        party = request.form.get('party')
        position = request.form.get('position')

        # Validate the data
        if not candidate_id or not name or not party or not position:
            flash('All fields are required!', 'error')
            return redirect(url_for('register_candidate'))

        # Create a new candidate document
        candidate_data = {
            'candidate_id': candidate_id,
            'name': name,
            'party': party,
            'position': position
        }

        # Insert the candidate document into the MongoDB collection
        mongo.db.candidates.insert_one(candidate_data)

        # Flash a success message
        flash('Candidate registered successfully!', 'success')
        return redirect(url_for('register_candidate'))  # Redirect after successful registration

    return render_template('register_candidate.html')  # Render form template for registration
