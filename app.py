from flask import Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import requests
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = 'din_hemmelige_nøkkel'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app = Flask(__name__)

@app.route('/authorize')
def authorize():
    params = {
        'client_id': '96',
        'redirect_uri': 'http://127.0.0.1:5000/callback',
        'response_type': 'code',
        'scope': ' '.join([
            'clients-readwrite',
            'journals-readwrite',
            'journal-files-read',
            'calendars-readwrite',
            'invoices-readwrite',
            'bookings-readwrite'
        ])
    }
    url = f'https://system.easypractice.net/oauth/authorize?{urlencode(params)}'
    print(f'Redirecting to URL: {url}')  # Logg den faktiske URL-en
    return redirect(url)


@app.route('/callback')
def callback():
    print("Full request URL:", request.url)  # Logg hele URL-en for å sjekke parametere
    print("Request args:", request.args)  # Dette vil vise alle query-parametere
    code = request.args.get('code')
    if code:
        try:
            access_token = get_access_token(code)
            return f'Tilgangstoken mottatt: {access_token}'
        except Exception as e:
            return f'En feil oppstod under henting av tilgangstoken: {str(e)}', 500
    else:
        return 'Autorisasjon feilet, ingen kode mottatt', 400



def get_access_token(code):
    data = {
        'grant_type': 'authorization_code',
        'client_id': '96',
        'client_secret': 'mWPJVInmG7l0frWQ3sCwMzjNdYRo5o2mxZXhfu7r',
        'redirect_uri': 'http://127.0.0.1:5000/callback',
        'code': code
    }
    response = requests.post('https://system.easypractice.net/oauth/token', data=data)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
