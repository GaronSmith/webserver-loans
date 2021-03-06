from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import json

from app.models import Loan, db
from app.utils.error_handling import make_error, check_types, check_types_with_none


loan_routes = Blueprint("loan", __name__)


@loan_routes.route("/<int:id>", methods=["GET"])
def get_loan(id):
    try:
        loan = Loan.query.get(id)
        if loan :
            return loan.to_dict(), 200
        else:
            return make_error(400, "Loan Not Found")      
    except SQLAlchemyError as e:
        return make_error(500, f'Internal Server Error: {repr(e)}')


@loan_routes.route("/<int:id>", methods=["PUT"])
def update_loan(id):
    try:
        loan = Loan.query.get(id)
        payload = json.loads(request.data)
        error = check_types_with_none(payload)
        if(error): return error
        loan.amount = payload["amount"] if "amount" in payload else loan.amount
        loan.interest_rate = payload["interest_rate"] if "interest_rate" in payload else loan.interest_rate
        loan.loan_length = payload["loan_length"] if "loan_length" in payload else loan.loan_length
        loan.monthly_payment = payload["monthly_payment"] if "monthly_payment" in payload else loan.monthly_payment
        db.session.commit()
        return {"message": "Loan updated",
                "loan": loan.to_dict()}, 200
    except (ValueError, KeyError, TypeError) as e:
        db.session.rollback()
        return make_error(400, f'JSON Format Error: {repr(e)}')
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_error(500, f'Internal Server Error: {repr(e)}')


@loan_routes.route("/<int:id>", methods=["DELETE"])
def delete_loan(id):
    try:
        loan = Loan.query.get(id)
        if loan :
            db.session.delete(loan)
            db.session.commit()
            return {"message": "Delete Successful."}, 200
        else:
            db.session.rollback()
            return make_error(400, "Loan not found")
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_error(500, f'Internal Server Error: {repr(e)}')


@loan_routes.route("/", methods=["GET"])
def get_loans():
    try:
        loans = Loan.query.all()
        if loans:
            return {loan.id: loan.to_dict() for loan in loans}, 200 
        else:
            return make_error(400, "Loans not found")
    except SQLAlchemyError as e:
        return make_error(500, f'Internal Server Error: {repr(e)}'),

@loan_routes.route("/", methods=[ "POST"])
def create_loan():
    try:
        payload = json.loads(request.data)
        error = check_types(payload)
        if(error): return error
        new_loan = Loan(
                    amount=payload["amount"],
                    interest_rate=payload["interest_rate"],
                    loan_length=payload["loan_length"],
                    monthly_payment=payload["monthly_payment"],
                    )
        db.session.add(new_loan)
        db.session.commit()
        return {"message": "Loan Created",
                "loan": new_loan.to_dict()}, 201
    except (ValueError, KeyError, TypeError) as e:
        db.session.rollback()
        return make_error(400, f'JSON Format Error: {repr(e)}')
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_error(500, f'Internal Server Error: {repr(e)}')
