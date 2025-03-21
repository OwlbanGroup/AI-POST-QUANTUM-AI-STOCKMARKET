from flask import render_template, request
from app.payment_facilitation import PaymentFacilitator
from app.gold_token import GoldToken

# Initialize payment facilitator
payment_facilitator = PaymentFacilitator()

def display_home():
    return render_template('home.html')

def handle_payment():
    amount = request.form.get('amount')
    payment_method = request.form.get('payment_method')
    response = payment_facilitator.process_payment(amount, payment_method)
    return response
