from flask import Flask, jsonify, request
import jwt
import requests

app = Flask(__name__)

# Sample data representing newspapers and books
newspapers = {
    '1': 'News of the World',
    '2': 'Today\'s News'
}
books = {
    '1': 'Life on Mars',
    '2': 'Think Fast or Slow'
}

# Function to fetch the public key(s) from Keycloak's JWKS (JSON Web Key Set) endpoint
def get_keycloak_public_key():
    # URL to fetch the JWKS from Keycloak
    jwks_url = "http://localhost:8080/realms/news_books_realm/protocol/openid-connect/certs"
    
    # Fetch and parse the JWKS JSON response
    jwks = requests.get(jwks_url).json()
    
    # Create a dictionary mapping key IDs (kid) to their corresponding RSA public keys
    keys = jwks['keys']
    return {key['kid']: jwt.algorithms.RSAAlgorithm.from_jwk(key) for key in keys}

# Function to validate the JWT (JSON Web Token)
def validate_token(token):
    try:
        # Extract the 'kid' (Key ID) from the token header without validating the signature yet
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get('kid')
        if not kid:
            raise ValueError("Missing 'kid' in token header")

        # Fetch the public key corresponding to the 'kid'
        key_map = get_keycloak_public_key()
        public_key = key_map.get(kid)
        
        if not public_key:
            raise ValueError(f"No public key found for kid: {kid}")

        # Decode the token using the fetched public key
        decoded_token = jwt.decode(token, key=public_key, algorithms=["RS256"], audience='account')
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Handle the case where the token has expired
        return "Token expired", 401
    except jwt.InvalidTokenError as e:
        # Handle other token validation errors
        return f"Invalid token: {str(e)}", 401
    except Exception as e:
        # Handle any other errors that occur during validation
        return f"Token validation error: {str(e)}", 401

# API endpoint to fetch resources (newspapers and books)
@app.route('/api/fetch_res', methods=['GET'])
def get_res():
    # Extract the authorization header from the request
    auth_header = request.headers.get('Authorization')
    
    if auth_header and auth_header.startswith('Bearer '):
        # Extract the token from the Bearer authorization header
        token = auth_header.split(' ')[1]
        print('Token:', token)
        
        # Validate the token and retrieve the decoded token
        decoded_token = validate_token(token)
        
        # Extract user roles from the decoded token
        roles = decoded_token.get("realm_access", {}).get("roles", [])
        
        # Initialize the resources dictionary with empty lists
        resources = {'newspapers': [], 'books': []}
        
        # All users get access to newspapers
        resources['newspapers'].extend(newspapers.values())
        
        # Only users with the 'premium' role get access to books
        if 'premium' in roles:
            resources['books'].extend(books.values())
        
        # Return the resources as a JSON response
        return jsonify(resources)
    
    # If no valid token is provided, return an unauthorized response
    return jsonify({'newspapers': [], 'books': []}), 401

# Entry point to run the Flask app
if __name__ == '__main__':
    # Run the Flask app on port 5001 with debug mode enabled
    app.run(port=5001, debug=True)
