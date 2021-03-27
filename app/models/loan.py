from .db import db

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable = False)
    interest_rate = db.Column(db.Float, nullable=False)
    loan_length = db.Column(db.Integer, nullable=False)
    monthly_payment = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "loan_length": self.loan_length,
            "monthly_payment": self.monthly_payment,
        }
