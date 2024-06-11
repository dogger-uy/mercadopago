from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import mercadopago 

# Credenciales de MercadoPago
YOUR_PUBLIC_KEY = "APP_USR-3f9b570c-0a48-427b-a9bd-f82cc714d9e7"
YOUR_ACCESS_TOKEN = "APP_USR-6830449923842012-051321-4794b782a5fe37b99163a88cb9bb11af-171201186"

app = Flask(_name_)
CORS(app)  # Habilitar CORS para todas las rutas
sdk = mercadopago.SDK(YOUR_ACCESS_TOKEN)

@app.route('/')
def home():
    return render_template('index.html', public_key=YOUR_PUBLIC_KEY)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    request_values = request.get_json()
    
    payment_data = {
        "transaction_amount": float(request_values["transaction_amount"]),
        "token": request_values["token"],
        "installments": int(request_values["installments"]),
        "payment_method_id": request_values["payment_method_id"],
        "issuer_id": request_values.get("issuer_id"),
        "payer": {
            "email": request_values["payer"]["email"],
            "identification": {
                "type": request_values["payer"]["identification"]["type"], 
                "number": request_values["payer"]["identification"]["number"]
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    return jsonify(payment), payment_response["status"]

if _name_ == '_main_':
    app.run(debug=True)