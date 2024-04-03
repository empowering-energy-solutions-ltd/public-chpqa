CHPQA
==============================

Documentation available at https://solid-adventure-93zpj3m.pages.github.io/

To run the streamlit app with functional user authentication follow the following steps.
1. Set up an account at https://auth0.com/
2. Go to `Applications` > `APIs` > `+ Create API`
3. Give it a name and end point, the end point can be anything, e.g 'https://test-endpoint/'. Leave the signing key as RS256.
4. Go into your newly created API. Go to settings and scroll to 'RBAC Settings' and enable RBAC and Add Permissions in the Access Token.
5. Now go to `User Management` > `Users` > `+ Create User`, fill in the details and leave connection as `Username-Password-Authentication`.
6. Time to fill the project `.env` file, use the list below to fill the values. 

<b> NOTE: </b> the first 3 environment variables DO NOT require '' in the .env. The last 3 do require them.

- `AUTH0_DOMAIN` - Go to `Application` > `Applications` > `Auth0 Account Management API Management Client` > `Settings` copy and paste the domain value. It should end in `us.auth0.com`.
- `AUTH0_API_AUDIENCE` - The endpoint name we set for the API if you copied the above example your audience would be `https://test-endpoint/`
- `AUTH0_ISSUER` - Same as AUTH0_DOMAIN but ends with `us.auth0.com/`. Ensure you add the forward slash.
- `AUTH0_DOMAIN_QUOTED` - Same as `AUTH0_DOMAIN` but within quotations '' and remove the `https://` portion of the URL.
- `AUTH0_CLIENT_ID` - Go to `Application` > `Applications` > `Auth0 Account Management API Management Client` > `Settings`, beneath Domain copy the Client ID and paste it to this value.
- `AUTH0_CLIENT_SECRET` - Go to `Application` > `Applications` > `Auth0 Account Management API Management Client` > `Settings`, beneath Client ID copy the Client Secret and paste it to this value.

Once these values are set, save the .env file and open two command lines and run each of the following lines,
<pre>
<code>
uvicorn src.backend.fast_api_app:app --reload --port 8000
</code>
</pre>
then in the second terminal run,
<pre>
<code>
streamlit run src/frontend/streamlit_app.py
</code>
</pre>

------------

Important folders
------------

<b>app_services</b> - Holds the code for both the frontend streamlit app and the backend FastAPI user authentication.


<b>src</b> - Contains all the functions responsible for generating the CHPQA reporting statistics.


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── notebooks          <- Jupyter notebooks. Contains demo notebook.
    │   │
    │   ├── example_chp_data.csv    <- Dummy CHP data for running the demo notebook
    │   │   
    │   └── demo_notebook.ipynb    <- Demo notebook showing how to use CHPQA, showing how the code can be used in a more complex system.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- specifies the python version used
    │
    │    
    ├── src                <- Source code used for CHPQA calculations.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── common         <- Holds the enums.py file used by other src files.
    │   │   │
    │   │   └── enums.py   <- Contains the enums classes for the different objects required in the project.
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   │
    │   │   ├── import_data.py <- Cleaning/manipulating functions to import data in correct format
    │   │   │
    │   │   ├── metering.py <- MeterReader + Sensor object (for future advanced CHPQA reporting)
    │   │   │
    │   │   ├── schema.py <- Naming schemas for the project
    │   │   │
    │   │   ├── source.py <- Holds the data manager object
    │   │   │
    │   │   └── x_y_coeff_vals - Sheet1.csv <- X & Y values needed for calculating Quality index for different system sizes
    │   │
    │   ├── backend        <- Contains the FastAPI app for user authentication with Auth0
    │   │   ├── __init__.py       <- Makes backend a Python module
    │   │   │
    │   │   ├── config.py         <- Retrieves the necessary variables from the .env file
    │   │   │
    │   │   ├── fast_api_app.py   <- File to run FastAPI app & contains router functions.
    │   │   │
    │   │   ├── requirements.txt  <- Package requirements for if app is deployed as a web service.
    │   │   │
    │   │   └── verification.py   <- Contains the verification code to ensure user has access + permissions.
    │   │
    │   ├── frontend       <- Contains the Streamlit app used for UI.
    │   │   │
    │   │   ├── __init__.py       <- Makes backend a Python module
    │   │   │
    │   │   ├── example data      <- Folder containing example data that can be uploaded to streamlit for demo.
    │   │   │
    │   │   ├── requirements.txt  <- Package requirements for if app is deployed as a web service.
    │   │   │
    │   │   ├── streamlit_app.py  <- File containing the main function. This is the run file to generate the streamlit app.
    │   │   │
    │   │   ├── streamlit_content.py  <- Contains functions to create the CHPQA report and generate the needed plots.
    │   │   │
    │   │   ├── streamlit_objs.py   <- Generates the different sections and content of the app.
    │   │   │
    │   │   └── utils.py   <- Holds the function to verify login, data prep functions and schemas for the app.
    │   │
    │   └── models         <- Scripts to train models and then use trained models to make
    │       │                 predictions
    │       ├── report.py
    │       │
    │       └── technology.py
    │
    ├── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
    │
    ├── poetry.loc <- .loc file generated by poetry after calling `poetry lock`
    │
    └── pyproject.toml <- .toml file generated by poetry for dependancy management.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
