import logging
import requests
from flask import Flask, redirect, url_for, session, render_template, jsonify
from flask_oidc import OpenIDConnect
import urllib.parse

# Configure logging to output debug information
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.debug = True

# Flask app configuration
app.config.update({
    'SECRET_KEY': 'SomethingNotEntireSecret',  # Secret key for session management
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',  # OIDC client configuration file
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,  # Insecure cookie for development (not recommended in production)
    'OIDC_SCOPES': ['openid', 'email', 'profile'],  # Scopes requested during authentication
    'OIDC_USER_INFO_ENABLED': True,  # Enable user info endpoint access
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'  # Auth method for token introspection
})

# Initialize the OIDC extension with the Flask app
oidc = OpenIDConnect(app)

@app.route('/login')
@oidc.require_login
def login():
    # Redirect to home after successful login
    return redirect(url_for('home'))

@app.route('/')
@oidc.require_login
def home():
    # Get user information from the OIDC provider
    user_info = oidc.user_getinfo(['sub', 'email', 'given_name', 'family_name'])

    # Get resources from session if available, otherwise initialize as empty
    resources = session.get('resources', {'newspapers': [], 'books': []})

    # Render the home template with user info and resources
    return render_template('home.html', user_info=user_info, resources=resources)

@app.route('/fetch_resources')
@oidc.require_login
def fetch_resources():
    # Obtain the access token for authenticated API requests
    access_token = oidc.get_access_token()

    # Fetch resources from an external microservice using the access token
    response = requests.get(
        "http://localhost:5001/api/fetch_res",
        headers={'Authorization': f'Bearer {access_token}'}
    )

    # Check if the API request was successful
    if response.status_code == 200:
        # Parse and store the resources in the session
        resources = response.json()
        session['resources'] = resources
    else:
        # If the API call fails, initialize resources as empty
        resources = {'newspapers': [], 'books': []}

    # Redirect back to the home page to display the resources
    return redirect(url_for('home'))

@app.route('/signout')
def signout():
    # Get the ID token from the session for logout
    id_token = session.get('oidc_id_token')

    # Base URL for Keycloak logout
    keycloak_base_logout_url = "http://localhost:8080/realms/news_books_realm/protocol/openid-connect/logout"

    if id_token:
        # If ID token is present, construct logout URL with token hint
        keycloak_logout_url = (
            f"{keycloak_base_logout_url}?id_token_hint={id_token}"
            f"&post_logout_redirect_uri={urllib.parse.quote('http://localhost:5000', safe='')}"
        )
    else:
        # If ID token is not present, construct a basic logout URL
        keycloak_logout_url = (
            f"{keycloak_base_logout_url}?client_id=news_books_client"
            f"&post_logout_redirect_uri={urllib.parse.quote('http://localhost:5000', safe='')}"
        )

    # Clear the session to log out locally
    session.clear()

    # Redirect to the Keycloak logout URL
    return redirect(keycloak_logout_url)

@app.route('/logout')
def logout():
    # Clear the session and redirect to the home page
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Start the Flask application in debug mode
    app.run(debug=True)
