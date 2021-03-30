from flask import jsonify

def make_error(status_code, message):
    response = jsonify({
        "status": status_code,
        "message": message
    })
    response.status_code = status_code
    return response


def check_types(payload):
    errors = [f'Loan {key} must be a number' for key in payload if not isinstance(
        payload[key], (int, float))]
    if(errors):
        return make_error(400, ", ".join(errors))
    else:
        return None

def check_types_with_none(payload):
    keys = set("amount loan_length monthly_payment interest_rate".split())
    errors = []
    for key in payload:
        if(key not in keys ):
            return make_error(400, f'Key: <{key}> is not valid')
        elif not isinstance(payload[key], (int,float)) and payload[key] is not None:
            errors.append(f'Loan {key} must be a number')
    if(errors):
        return make_error(400, ", ".join(errors))
    else:
        return None

