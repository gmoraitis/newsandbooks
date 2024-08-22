# imports
import logging
import jwt
from flask import Flask, redirect, url_for, session, render_template
from flask_oidc import OpenIDConnect
import urllib.parse

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

# Data sample definitions, will be moved on models
newspapers = {
    '1': 'News of the World',
    '2': 'Today\'s News'
}
books = {
    '1': 'Life on Mars',
    '2': 'Think Fast'
}


@app.route('/login')
@oidc.require_login # send user to auth_url based on the client_secrets.json
def login():
    # This route triggers the OAuth 2.0 authorization request on 
    return redirect(url_for('home'))


@app.route('/')
def home():
    if oidc.user_loggedin:
        # User is logged in, get the access token
        access_token = oidc.get_access_token()
        logging.debug(f"Access Token: {access_token}")  # Log the access token

        try:
            # Decode the JWT access token
            decoded_token = jwt.decode(access_token, options={"verify_signature": False}, algorithms=["RS256"])
            logging.debug(f"Decoded Token: {decoded_token}")  # Log the decoded token

            # Extract roles from the token
            realm_access = decoded_token.get('realm_access', {})
            roles = realm_access.get('roles', [])
            logging.debug(f"User Roles: {roles}")

              # Pass the roles and other information to the template
            return render_template('home.html', newspapers=newspapers, books=books, user_info=decoded_token, roles=roles)

            # # Check for 'premium' role in news_books_client resource roles
            # if 'premium' in roles:
            #     logging.debug("User has premium role")
            #     return render_template('home.html', newspapers=newspapers, books=books, user_info=decoded_token)
            # else:
            #     logging.debug("User does not have premium role")
            #     return render_template('home.html', newspapers=newspapers, user_info=decoded_token)

        except jwt.DecodeError as e:
            logging.error(f"Failed to decode JWT: {e}")
            return "Invalid token", 400
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return "An error occurred", 500
    else:
        return redirect(url_for('login'))


        
@app.route('/signout')
def signout():
    # Retrieve the ID token from the session
    id_token = session.get('oidc_auth_token', {}).get('id_token')
    

    
    # Keycloak logout URL
    keycloak_logout_url = (
        "http://localhost:8080/realms/news_books_realm/protocol/openid-connect/logout"
        f"?id_token_hint={id_token}&post_logout_redirect_uri={urllib.parse.quote('http://localhost:5000', safe='')}"
    )
    
    session.clear()

    # Redirect to Keycloak for logging out
    return redirect(keycloak_logout_url)

# Optionally, clear the session after logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)




/////


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
</head>
<body>
    <h1>Welcome {{ user_info.preferred_username }} to News and Books</h1>
    {% if user_info %}

        <h2>Newspapers</h2>
        <ul>
            {% for id, name in newspapers.items() %}
                <li>{{ name }}</li>
            {% endfor %}
        </ul>

        {% if 'premium' in roles %}
            <h2>Books</h2>
            <ul>
                {% for id, name in books.items() %}
                    <li>{{ name }}</li>
                {% endfor %}
            </ul>
        {% endif %}

        <a href="{{ url_for('signout') }}">Logout</a>
    {% else %}
        <a href="{{ url_for('login') }}">Login</a>
    {% endif %}
</body>
</html>
