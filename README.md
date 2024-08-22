## News and Books
A basic app to interact with authendication service in a fullstack app with React JS and Flask, using PostreSQL as the database. This project is for learning path.


The `client_secrets.json` file contains configuration details for your OAuth 2.0 client.

`issuer`: The URL of the OpenID Connect provider. This is the base URL for the identity provider (Keycloak in this case).

`auth_uri`: The authorization endpoint URL where the client will redirect the user to authenticate and authorize the application.

`client_id`: The unique identifier for your client application registered with the OpenID Connect provider.

`client_secret`: The secret key associated with the client_id, used to authenticate the client application with the OpenID Connect provider.

`redirect_uris`: The list of URIs to which the OpenID Connect provider can redirect the user after authentication. These URIs must be registered with the provider.

`userinfo_uri`: The endpoint URL to fetch user information after obtaining an access token.

`token_uri`: The endpoint URL to exchange the authorization code for an access token.

`token_introspection_uri`: The endpoint URL to introspect the token, which allows the client to validate the token and retrieve its metadata.



