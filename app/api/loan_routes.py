from flask import Blueprint, request
from app.models import Loan, db
import json

loan_routes = Blueprint("loan", __name__)

@loan_routes.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def loans(id):
    loan = Loan.query.filter(Loan.id == id).first()
    if request.method == "PUT":
        pass
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
