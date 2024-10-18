from flask import Blueprint

voter_bp = Blueprint('voter', __name__, url_prefix='/voter')

from . import voters_login