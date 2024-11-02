from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from .admin_login import login_admin
from .create_candidate import register_candidate
from .create_voter import create_voter
from .register_admin_user import register_admin
from .view_voters import view_voters
from .create_elections import create_presidential_election
from .create_elections import create_gubernatorial_election
from .create_elections import create_senatorial_election
from .create_elections import create_house_of_representative_election