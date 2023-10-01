from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

# Replace these with your Twilio credentials
#TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
#TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'

# Phone Validator API
api_key = 'f88a38b4-bccd-4740-a318-363c6d5f8478'

# Handle incoming Twilio webhook
@app.route('/voice', methods=['POST'])
def voice():
    # Get the caller's phone number from the incoming request
    caller_number = request.form.get('From')

    url = f'https://api.phonevalidator.com/api/v3/phonesearch?apikey=f88a38b4-bccd-4740-a318-363c6d5f8478&type=basic&phone={caller_number}'

    headers = {
    'Authorization': f'Bearer {api_key}'
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        PhoneBasic = data['PhoneBasic']
        LineType = PhoneBasic['LineType']

        # Determine the forwarding number based on caller type
        if LineType in ['CELL PHONE', 'LANDLINE']:
            forwarding_number = '+18668080437'
        else:
            forwarding_number = '+12138143160'

       # Create TwiML response to forward the call
        twiml = f"""
            <Response>
                <Dial>{forwarding_number}</Dial>
            </Response>
        """
        return Response(twiml, mimetype='text/xml')
    else:
        return 'Phone validation failed', 400

if __name__ == '__main__':
    app.run(debug=True)
