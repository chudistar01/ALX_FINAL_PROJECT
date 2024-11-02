from flask import render_template, request, flash, redirect, url_for, session
from bson.objectid import ObjectId  # Import ObjectId if using MongoDB's ObjectId for admin_id
from math import ceil  # Import ceil for pagination calculations
from . import admin_bp
from ..extensions import mongo

@admin_bp.route('/view_voters', methods=['GET'])
def view_voters():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('admin.login_admin'))  # Ensure correct URL for the login route

    # Fetch the admin's details from the session
    admin_id = session['admin_id']  # Assuming admin ID is stored in session
    admin_username = session.get('admin_username', 'Admin')  # Default to 'Admin' if not found

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of voters per page
    total_voters = mongo.db.voters.count()  # Use count() instead of count_documents()
    total_pages = ceil(total_voters / per_page)
    
    # Fetch voters for the current page
    voters = mongo.db.voters.find().skip((page - 1) * per_page).limit(per_page)

    # Load states for the filter dropdown
    states = mongo.db.states.find()

    return render_template('admin_dashboard.html', 
                           voters=voters, 
                           states=states, 
                           page=page, 
                           total_pages=total_pages, 
                           admin_id=admin_id, 
                           admin_username=admin_username)
