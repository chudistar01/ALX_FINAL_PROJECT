import os
import json
from flask import render_template, request, flash, redirect, url_for, session
from . import admin_bp
from ..extensions import mongo
from bson.objectid import ObjectId

# Load JSON data from the instance folder
def load_json(filename):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'instance', filename)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {filename}: {e}")
        flash(f"Error loading {filename}. Please check its format.", 'error')
        return {}

@admin_bp.route('/register_candidate', methods=['GET', 'POST'])
def register_candidate():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login_admin'))

    # Load geographical data
    geographical_data = load_json('geographical_data.json')
    states = geographical_data['geographical_data']['states']

    parties = ["APC", "PDP", "LABOUR", "APGA"]
    positions = ["Presidential", "Gubernatorial", "Senatorial", "House of Rep"]

    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        surname = request.form.get('surname')
        party = request.form.get('party')
        position = request.form.get('position')
        state = request.form.get('state')
        senatorial_district = request.form.get('senatorial_district')
        federal_constituency = request.form.get('federal_constituency')

        # Validate the data
        if not first_name or not surname or not party or not position:
            flash('First name, surname, party, and position fields are required!', 'error')
            return redirect(url_for('admin.register_candidate'))

        # Dynamically generate a unique candidate_id
        candidate_id = str(ObjectId())

        # Create a new candidate document
        candidate_data = {
            'candidate_id': candidate_id,
            'first_name': first_name,
            'middle_name': middle_name,
            'surname': surname,
            'party': party,
            'position': position,
            'state': state,
            'senatorial_district': senatorial_district,
            'federal_constituency': federal_constituency
        }

        # Insert the candidate document into MongoDB
        mongo.db.candidates.insert_one(candidate_data)

        # Flash success message
        flash('Candidate registered successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    # Pass states to the template
    return render_template('register_candidate.html', states=states, parties=parties, positions=positions)

