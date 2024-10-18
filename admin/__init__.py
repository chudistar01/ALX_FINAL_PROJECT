from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import admin_login
from . import create_candidate
from . import create_voter
from . import register_admin_user