from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200
    

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match any of the search parameters
    """
    # Initialize the results with the entire USERS list
    results = USERS

    # Check if any parameters are provided for ID, Name, Age, or Occupation
    if any(param in args for param in ['id', 'name', 'age', 'occupation']):
        user_id = args.get('id')
        user_name = args.get('name', '').lower()
        user_age = args.get('age')
        user_occupation = args.get('occupation', '').lower()

        results = [
            user for user in results
            if (user_id and user['id'] == user_id) or
               (user_name and user_name in user['name'].lower()) or
               (user_age and int(user_age) - 1 <= user['age'] <= int(user_age) + 1) or
               (user_occupation and user_occupation in user['occupation'].lower())
        ]

    # Deduplicate the results
    results = list({user['id']: user for user in results}.values())

    # Generate search suggestions based on available data
    if not results:
        suggestions = generate_search_suggestions(USERS)
        suggestions_message = "\n".join(f"- {suggestion}" for suggestion in suggestions)
        return f"No results found. Consider trying:\n{suggestions_message}"

    return results

#Generate search suggestions based on available user data
def generate_search_suggestions(users):
    """Generate search suggestions based on available user data"""
    name_suggestions = set(user['name'].split()[0].lower() for user in users)
    age_suggestions = set(str(user['age']) for user in users)
    occupation_suggestions = set(word.lower() for user in users for word in user['occupation'].split())

    return list(name_suggestions.union(age_suggestions, occupation_suggestions))
