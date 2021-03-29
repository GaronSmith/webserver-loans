from flask import jsonify

def make_error(status_code, message):
    response = jsonify({
        "status": status_code,
        "message": message
    })
    response.status_code = status_code
    return response


def check_types(payload):
    errors = [f'Loan {key} must be a number' for key in payload if not isinstance(payload[key], (int, float))]
    if(errors):
        return make_error(400, ", ".join(errors))
    else:
        return None