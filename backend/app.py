# imports
import logging
import jwt
from flask import Flask, redirect, url_for, session, render_template, jsonify
from flask_oidc import OpenIDConnect
import urllib.parse
import requests

logging.basicConfig(level=logging.DEBUG)

# Flask app configuration
app = Flask(__name__)
app.debug = True
app.config.update({
    'SECRET_KEY': 'SomethingNotEntireSecret',
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

oidc = OpenIDConnect(app)

@app.route('/login')
@oidc.require_login
def login():
    return redirect(url_for('home'))

@app.route('/')
def home():
    if oidc.user_loggedin:
        access_token = oidc.get_access_token()
        logging.debug(f"Access Token: {access_token}")

        try:
            decoded_token = jwt.decode(access_token, options={"verify_signature": False}, algorithms=["RS256"])
            logging.debug(f"Decoded Token: {decoded_token}")

            realm_access = decoded_token.get('realm_access', {})
            roles = realm_access.get('roles', [])
            logging.debug(f"User Roles: {roles}")

            return render_template('home.html', user_info=decoded_token, roles=roles)

        except jwt.DecodeError as e:
            logging.error(f"Failed to decode JWT: {e}")
            return "Invalid token", 400
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return "An error occurred", 500
    else:
        return redirect(url_for('login'))

@app.route('/fetch_resources', methods=['POST'])
@oidc.require_login
def fetch_resources():
    access_token = oidc.get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}

    newspapers_response = requests.get("http://localhost:5001/api/newspapers", headers=headers)
    books_response = requests.get("http://localhost:5001/api/books", headers=headers)

    newspapers = newspapers_response.json() if newspapers_response.status_code == 200 else {}
    books = books_response.json() if books_response.status_code == 200 else {}

    decoded_token = jwt.decode(access_token, options={"verify_signature": False}, algorithms=["RS256"])
    realm_access = decoded_token.get('realm_access', {})
    roles = realm_access.get('roles', [])

    # Render the home template with the fetched resources
    return render_template('home.html', user_info=decoded_token, roles=roles, newspapers=newspapers, books=books)


@app.route('/signout')
def signout():
    # Retrieve the ID token from the session
    id_token = session.get('oidc_id_token')  # Ensure this is the correct key for the ID token

    # Define the base Keycloak logout URL
    keycloak_base_logout_url = "http://localhost:8080/realms/news_books_realm/protocol/openid-connect/logout"

    if id_token:
        # Keycloak logout URL with id_token_hint
        keycloak_logout_url = (
            f"{keycloak_base_logout_url}?id_token_hint={id_token}"
            f"&post_logout_redirect_uri={urllib.parse.quote('http://localhost:5000', safe='')}"
        )
    else:
        # Keycloak logout URL with client_id if id_token_hint is missing
        keycloak_logout_url = (
            f"{keycloak_base_logout_url}?client_id=news_books_client"
            f"&post_logout_redirect_uri={urllib.parse.quote('http://localhost:5000', safe='')}"
        )

    # Clear the session
    session.clear()

    # Redirect to Keycloak for logging out
    return redirect(keycloak_logout_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
