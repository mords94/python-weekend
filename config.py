TARIFS_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/tariffs'
ROUTE_URL = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"
LOCATIONS_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
SINGLE_ROUTE_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/routes/:id/simple'
RATES_URL = 'https://api.skypicker.com/rates'


CREDS = {
    'user': 'balazs_dravai', 'pass': '683a2f23d6de47deabd82fadf681aaa3',
}

DATABASE_URL = f"postgresql://{CREDS['user']}:{CREDS['pass']}@sql.pythonweekend.skypicker.com/pythonweekend?application_name={CREDS['user']}_local_dev"
