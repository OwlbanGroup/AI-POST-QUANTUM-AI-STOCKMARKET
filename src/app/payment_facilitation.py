from flask import jsonify

class PaymentFacilitator:
    def __init__(self):
        self.transactions = []

    def process_payment(self, amount, payment_method):
        # Logic to process payment
        transaction = {
            "amount": amount,
            "payment_method": payment_method
        }
        self.transactions.append(transaction)
        return jsonify({"message": f"Processed payment of {amount} using {payment_method}."})
