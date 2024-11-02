import os
from flask import render_template, request, flash, redirect, url_for, session, current_app
from . import admin_bp
from ..extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime
import json



def load_json(filename):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'instance', filename)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {filename}: {e}")
        flash(f"Error loading {filename}. Please check its format.", 'error')
        return {}





try:
    with open(os.path.join('instance', 'states.json')) as f:
        states_data = json.load(f)
except FileNotFoundError:
    states_data = []  # or handle it differently as per your needs
    print("Error: 'states.json' not found in instance folder.")

try:
    with open(os.path.join('instance', 'senatorial_district.json')) as f:
        senatorial_district_data = json.load(f)
except FileNotFoundError:
    senatorial_district_data = []
    print("Error: 'senatorial_district.json' not found in instance folder.")

try:
    with open(os.path.join('instance', 'federal_constituency.json')) as f:
        federal_constituency_data = json.load(f)
except FileNotFoundError:
    federal_constituency_data = []
    print("Error: 'federal_constituency.json' not found in instance folder.")


#Creates presidential elections
@admin_bp.route('/create_presidential_election', methods=['GET', 'POST'])
def create_presidential_election():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('admin.login_admin'))
    
    if request.method == 'POST':
        # Get election details
        election_date = request.form.get('election_date')
        
        # Check if date is provided
        if not election_date:
            flash('Election date is required!', 'error')
            return redirect(url_for('admin.create_presidential_election'))

        try:
            # Parse and validate the date
            election_date = datetime.strptime(election_date, "%Y-%m-%d")
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('admin.create_presidential_election'))
        
        # Retrieve all candidates with the position 'Presidential'
        presidential_candidates = list(mongo.db.candidates.find({"position": "Presidential"}))
        
        # Add a new election document to the elections collection
        election_data = {
            "type": "Presidential",
            "date": election_date,
            "candidates": presidential_candidates,
            "created_at": datetime.utcnow(),
            "status": "active"
        }
        mongo.db.elections.insert_one(election_data)
        
        flash('Presidential election created successfully!', 'success')
        return redirect(url_for('admin.create_presidential_election'))
    
    # Retrieve all presidential candidates to display in the form
    presidential_candidates = list(mongo.db.candidates.find({"position": "Presidential"}))
    
    return render_template('create_presidential_election.html', presidential_candidates=presidential_candidates)


#Gubernatorial elections
@admin_bp.route('/create_gubernatorial_election', methods=['GET', 'POST'])
def create_gubernatorial_election():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login_admin'))

    # Define the path to the states.json file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'states.json')
    
    try:
        with open(json_file_path) as f:
            data = json.load(f)
            # Extract states names for dropdown
            states_data = [state['name'] for state in data["states"]]
    except FileNotFoundError:
        flash('States data file not found!', 'error')
        return redirect(url_for('admin.admin_dashboard'))

    if request.method == 'POST':
        election_date = request.form.get('election_date')
        selected_state = request.form.get('state')  # Get the selected state

        # Validate inputs
        if not election_date or not selected_state:
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.create_gubernatorial_election'))

        # Parse and validate election date
        try:
            election_date = datetime.strptime(election_date, "%Y-%m-%d")
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('admin.create_gubernatorial_election'))

        # Find candidates for the selected state
        candidates = list(mongo.db.candidates.find({"position": "Gubernatorial", "state": selected_state}))

        election_data = {
            "type": "Gubernatorial",
            "date": election_date,
            "state": selected_state,
            "candidates": candidates,
            "created_at": datetime.utcnow(),
            "status": "active"
        }
        mongo.db.elections.insert_one(election_data)

        flash('Gubernatorial elections created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    # Render the template with the loaded states data
    return render_template('create_gubernatorial_election.html', states=states_data)


#Senatorial election
@admin_bp.route('/create_senatorial_election', methods=['GET', 'POST'])
def create_senatorial_election():
    # Load states data from JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'states.json')
    try:
        with open(json_file_path) as f:
            data = json.load(f)
            states_data = data["states"]
    except FileNotFoundError:
        flash('States data file not found!', 'error')
        return redirect(url_for('admin.admin_dashboard'))

    # Extract the names of senatorial districts for the dropdown
    senatorial_districts_data = [
        district["name"]
        for state in states_data
        for district in state["senatorial_districts"]
    ]

    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('admin.login_admin'))

    if request.method == 'POST':
        election_date = request.form.get('election_date')
        states = request.form.getlist('state')  # Get the list of selected states
        senatorial_districts = request.form.getlist('senatorial_district')  # Get selected senatorial districts

        if not election_date or not states or not senatorial_districts:
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.create_senatorial_election'))

        try:
            election_date = datetime.strptime(election_date, "%Y-%m-%d")
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('admin.create_senatorial_election'))

        # Loop through each selected state and senatorial district
        for state in states:
            for district in senatorial_districts:
                candidates_cursor = mongo.db.candidates.find({
                    "position": "Senatorial",
                    "state": state,
                    "senatorial_district": district
                })
                candidates = list(candidates_cursor)  # Convert cursor to a list

                election_data = {
                    "type": "Senatorial",
                    "date": election_date,
                    "state": state,
                    "senatorial_district": district,
                    "candidates": candidates,  # Now a list
                    "created_at": datetime.utcnow(),
                    "status": "active"
                }

                mongo.db.elections.insert_one(election_data)

        flash('Senatorial elections created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('create_senatorial_election.html', states=states_data, senatorial_districts=senatorial_districts_data)

#House Representatives

@admin_bp.route('/create_house_of_representative_election', methods=['GET', 'POST'])
def create_house_of_representative_election():
    # Load states data from JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'states.json')
    with open(json_file_path) as f:
        data = json.load(f)
        states_data = data["states"]

    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('admin.login_admin'))

    if request.method == 'POST':
        election_date = request.form.get('election_date')
        states = request.form.getlist('state')
        senatorial_districts = request.form.getlist('senatorial_district')
        federal_constituencies = request.form.getlist('federal_constituency')

        # Validate inputs
        if not election_date or not states or not senatorial_districts or not federal_constituencies:
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.create_house_of_representative_election'))

        try:
            election_date = datetime.strptime(election_date, "%Y-%m-%d")
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('admin.create_house_of_representative_election'))

        # Insert the election data into the database
        # (your insertion logic here...)

        flash('House of Representative elections created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('create_house_of_representative_election.html', states=states_data)
