import time
from flask import Blueprint

from .data.match_data import MATCHES


bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("<int:match_id>")
def match(match_id):
    if not 0 <= match_id < len(MATCHES):
        return "Invalid match id", 404

    start_time = time.time()
    matched_elements = find_matching_elements(*MATCHES[match_id])
    end_time = time.time()
# Define if there is a match number and show the matching numbers
    if matched_elements:
        response_data = {"Status": "Match found"}
    else:
        response_data = {"Status": "No match"}

    elapsed_time = end_time - start_time

    return {"response": response_data, "elapsedTime": elapsed_time}, 200

def find_matching_elements(fave_numbers_1, fave_numbers_2):
    # Input the lists to set for efficient element operation
    set_1 = set(fave_numbers_1)
    set_2 = set(fave_numbers_2)

    # Return the set of matched numbers directly
    return set_1.intersection(set_2)
