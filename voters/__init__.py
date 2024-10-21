from flask import Blueprint

voters_bp = Blueprint('voters', __name__, url_prefix='/voter')

from . import voters_login