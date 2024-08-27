
## News and Books

### **High-Level Overview:**

This is a web application based on the current setup (Authentication [app - Keycloak - Microservice]), which allows users to log in via OpenID Connect (OIDC) authentication, interact with a backend service to fetch resources (like newspapers and books), and manage sessions with Keycloak, an open-source Identity and Access Management tool. The application distinguishes between "premium" and "limited" users, granting different levels of access based on their roles. Premium users can access both newspapers and books, while limited users can only access newspapers.

### **Components Involved**

1. **Frontend (HTML/Jinja2 Templates)**: Displays the resources (newspapers and books) to the user and allows interaction.
2. **Flask Application**: Handles user authentication, session management, and routing.
3. **Keycloak**: Manages user authentication, roles, and access tokens.
4. **Microservice**: A simple service that returns lists of resources (newspapers and books) based on the user's role.

#### **1. Building the Flask Application**

The Flask application serves as the bridge between the frontend and the backend services.

- **Explanation**: 
  - The application uses Flask for the web framework and Flask-OIDC for OpenID Connect authentication.
  - The `client_secrets.json` file contains the client configuration for interacting with Keycloak.

**The Login Route**
- **Explanation**: 
  - This route is used to initiate the login process. It redirects users to the Keycloak login page.

**The Home Route**
- **Explanation**: 
  - After logging in, users are redirected here. The route fetches user information and resources (if available) and passes them to the template for rendering.

**The Fetch Resources Route from the Microservice**
- **Explanation**:
  - This route sends a request to the microservice to fetch resources. The request includes an access token to authenticate the user. The response (list of resources) is stored in the session.

**The Sign-Out from Keycloak**
- **Explanation**:
  - This route logs the user out of both the Flask application and Keycloak, clearing the session.

#### **2. Building the Microservice**

This microservice provides the resources (newspapers and books) based on the user's role.

**Import Dependencies and Initialize Flask**
- **Explanation**:
  - This part of the code initializes the Flask app and sets up some sample data.

**Fetch the Public Key from Keycloak using the `get_keycloak_public_key` Function**
- **Explanation**:
  - This function fetches the JSON Web Key Set (JWKS) from Keycloak, which is used to validate the JWT tokens.

**Validate the JWT Token with the `validate_token` Function**
- **Explanation**:
  - This function decodes and validates the JWT token using the public key fetched from Keycloak.

**Define the API Endpoint to Fetch Resources**
- **Explanation**:
  - This endpoint returns a list of resources based on the user's role. If the user is "premium," they get both newspapers and books. Otherwise, they only get newspapers.

#### **3. Creating the HTML Template**

This template displays the resources to the user.
- **Explanation**:
  - The template uses Jinja2 syntax to dynamically display the user's resources. The style is optimized for a dark mode look.

#### **4. Running the Application**

1. **Start Keycloak**:
   - Run Keycloak using the command:
     ```sh
     bin/kc.sh start-dev
     ```

2. **Start the Microservice**:
   - Run the microservice on port 5001 with the command:
     ```bash
     python ms.py
     ```

3. **Start the Flask Application**:
   - Run the Flask application with the command:
     ```bash
     python app.py
     ```

4. **Access the Application**:
   - Go to `http://localhost:5000/`.
   - You’ll be redirected to the Keycloak login page. Log in with your credentials.

5. **Fetch and Display Resources**:
   - After logging in, you’ll be redirected to the home page where you can see the available resources.
   - Click on "Refresh Resources" to fetch the latest resources from the microservice.

6. **Sign Out**:
   - Use the "Sign Out" link to log out of both the Flask application and Keycloak.

### **Summary**

This guide provides a complete overview of building a full-stack web application with user authentication, role-based access control, and resource management. The integrated Flask app works with Keycloak for authentication, a microservice serves resources based on user roles, and a frontend displays the resources. 

**Current Status Outcome**
The application demonstrates handling JWT validation (in `ms.py`), session management, and user role-based access.

**Future Enhancements**
Later additions will expand the app to use a resource server.