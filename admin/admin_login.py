from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from . import admin_bp
from ..extensions import mongo

@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        admin_id = session['admin_id']
        admin_username = session['admin_username']
        return render_template('admin_dashboard.html', admin_id=admin_id, admin_username=admin_username)
    else:
        flash('You must log in to access the dashboard.', 'warning')
        return redirect(url_for('admin_bp.login_admin'))  # Redirect to login if not logged in

@admin_bp.route('/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        # Get login credentials from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if all fields are filled
        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect(url_for('admin.login_admin'))

        # Find the admin user in MongoDB by username
        admin = mongo.db.admins.find_one({'username': username})

        # Verify the password
        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['admin_id']
            session['admin_username'] = admin['username']
            flash('Login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))  # Redirect to the dashboard

        # If the login fails, show an error message
        flash('Invalid username or password!', 'error')
        return redirect(url_for('admin.login_admin'))

    # Render the login form template for GET requests
    return render_template('login_admin.html')

@admin_bp.route('/logout')
def logout_admin():
    session.pop('admin_id', None)  # Clear the admin ID from the session
    session.pop('admin_username', None)  # Also clear the username
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin.login_admin'))  # Redirect to login after logout
