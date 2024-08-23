from flask import Flask, jsonify, request
import jwt

app = Flask(__name__)

# Data (move from the client app to here)
newspapers = {
    '1': 'News of the World',
    '2': 'Today\'s News'
}
books = {
    '1': 'Life on Mars',
    '2': 'Think Fast'
}

# Helper function to validate token
def validate_token(token):
    try:
        # Decode the token (in a real scenario, you'd verify it with Keycloak's public key)
        decoded_token = jwt.decode(token, options={"verify_signature": False}, algorithms=["RS256"])
        return decoded_token
    except Exception as e:
        return None

# Endpoints for fetching data
@app.route('/api/newspapers', methods=['GET'])
def get_newspapers():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        decoded_token = validate_token(token)
        if decoded_token:
            return jsonify(newspapers)
    return "Unauthorized", 401

@app.route('/api/books', methods=['GET'])
def get_books():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        decoded_token = validate_token(token)
        if decoded_token:
            roles = decoded_token.get('realm_access', {}).get('roles', [])
            if 'premium' in roles:
                return jsonify(books)
    return "Unauthorized", 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
