from flask import Blueprint, request
from app.models import Loan

loan_routes = Blueprint("loan", __name__)

@loan_routes.route("/", methods=["GET"])
def get_loans():
    loans = Loan.query.all()

    return {loan.id: loan.to_dict() for loan in loans}
