from flask import Blueprint

voters_bps = Blueprint('voters', __name__, url_prefix='/voter')


print("Initializing voters module")
from .voters_login import login_voter
from .register_voter import registers_voters
from .vote_presidential import vote_presidential
from .vote_house_of_reps import vote_house_of_reps
from .vote_gubernatorial import vote_gubernatorial
from .voters_dashboard import dashboard