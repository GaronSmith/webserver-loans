from flask import Blueprint, request
from app.models import Loan, db
import json

loan_routes = Blueprint("loan", __name__)

@loan_routes.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def loans(id):
    loan = Loan.query.get(id)
    if request.method == "PUT":
        payload = json.loads(request.data)
        print("******", "amount" in payload)
        loan.amount = payload["amount"] if "amount" in payload else loan.amount
        loan.interest_rate = payload["interest_rate"] if "interest_rate" in payload else loan.interest_rate
        loan.loan_length = payload["loan_length"] if "loan_length" in payload else loan.loan_length
        loan.monthly_payment = payload["monthly_payment"] if "monthly_payment" in payload else loan.monthly_payment
        db.session.commit()
        return {"message": "Loan updated", 
        "loan": loan.to_dict()}
    elif request.method == "DELETE":
        db.session.delete(loan)
        db.session.commit()
        return {"message": "Delete Successful."}
    return {loan.id: loan.to_dict()}


@loan_routes.route("/", methods=["GET", "POST"])
def create_loan():
    if request.method == "GET":
        loans = Loan.query.all()
        return {loan.id: loan.to_dict() for loan in loans}
    
    elif request.method == "POST":
        payload = json.loads(request.data)
        new_loan = Loan(
            amount = payload["amount"],
            interest_rate = payload["interest_rate"],
            loan_length = payload["loan_length"],
            monthly_payment = payload["monthly_payment"]
        )
        db.session.add(new_loan)
        db.session.commit()
        return {"message": "Loan Created", 
                "loan": new_loan.to_dict()}
