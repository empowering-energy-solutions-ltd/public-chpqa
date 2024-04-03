#How to guide

A streamlet app is used for the front end of the tool. 

To run the streamlit app with functional user authentication follow the following steps.

- Set up an account at https://auth0.com/
- Go to Applications > APIs > + Create API
- Give it a name and end point, the end point can be anything, e.g 'https://test-endpoint/'. Leave the signing key as RS256.
- Go into your newly created API. Go to settings and scroll to 'RBAC Settings' and enable RBAC and Add Permissions in the Access Token.
- Now go to User Management > Users > + Create User, fill in the details and leave connection as Username-Password-Authentication.
- Time to fill the project .env file, use the list below to fill the values.

NOTE: the first 3 environment variables DO NOT require '' in the .env. The last 3 do require them.

- AUTH0_DOMAIN - Go to Application > Applications > Auth0 Account Management API Management Client > Settings copy and paste the domain value. It should end in us.auth0.com.
- AUTH0_API_AUDIENCE - The endpoint name we set for the API if you copied the above example your audience would be https://test-endpoint/
- AUTH0_ISSUER - Same as AUTH0_DOMAIN but ends with us.auth0.com/. Ensure you add the forward slash.
- AUTH0_DOMAIN_QUOTED - Same as AUTH0_DOMAIN but within quotations '' and remove the https:// portion of the URL.
- AUTH0_CLIENT_ID - Go to Application > Applications > Auth0 Account Management API Management Client > Settings, beneath Domain copy the Client ID and paste it to this value.
- AUTH0_CLIENT_SECRET - Go to Application > Applications > Auth0 Account Management API Management Client > Settings, beneath Client ID copy the Client Secret and paste it to this value.
- Once these values are set, save the .env file and open two command lines and run each of the following lines,

uvicorn src.backend.fast_api_app:app --reload --port 8000

- then in the second terminal run,

streamlit run src/frontend/streamlit_app.py

There is an example notebook with dummy data available as well?