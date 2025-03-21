from flask import Flask, render_template, request
from natural_resources_management import NaturalResourcesManagement
from src.ai_model.predictive_model import PredictiveModel

app = Flask(__name__)
manager = NaturalResourcesManagement()
predictive_model = PredictiveModel()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_resource', methods=['POST'])
def add_resource():
    resource_name = request.form['resource_name']
    quantity = request.form['quantity']
    forecasted_needs = request.form.get('forecasted_needs')
    response = manager.add_resource(resource_name, quantity, forecasted_needs)
    return response

@app.route('/generate_report', methods=['GET'])
def generate_report():
    report = manager.generate_report(predictive_model=predictive_model)
    return render_template('report.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)
