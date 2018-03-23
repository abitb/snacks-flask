import requests

APIKEY = "a1bacf53-c847-4b5d-81fa-822b8138ecda"
SNACK_URL = "https://api-snacks.nerderylabs.com/v1/snacks/"


def get_snacks_from_web_service():
    """
    get current list of snack foods from Nerdery web service
    :returns: list of dicts, of snack info (in unicode)
    :returns: False if web service is not working
    """
    payload = {"ApiKey": APIKEY}
    resp = requests.get(SNACK_URL, params=payload)

    if resp.status_code == 200:
    # [{id, lastPurchaseDate, name, optional, purchaseCount, purchaseLocations},..]
        return resp.json()
    else:
        return False


def separate_optional_snacks(snacks_from_ws):
    """
    take response from webservice and return 2 lists depending on if
    the snack is optional
    :param snacks_from_ws: list of dicts, data structure returned from nerdery webservice
    :returns: tuple of 2 lists -- always_purchased and optional_snacks
    """
    always_purchased = []
    optional_snacks = []
    for snack in snacks_from_ws:
        if snack["optional"] == False:
            always_purchased.append(snack)
        else:
            optional_snacks.append(snack)
    return (always_purchased, optional_snacks)

def post_snack_to_web_service(name, location):
    """
    get a snack suggestion to Nerdery web service
    :param
    :returns: 200 when suggestion is made successfully
    :returns: 409 when suggestion already exists
    :returns: False in other situations
    """
    headers = {"content-type":"application/json"}
    payload = {"ApiKey": APIKEY}
    data = json.dumps({"name":name, "location":location})
    resp = requests.post("https://api-snacks.nerderylabs.com/v1/snacks/", params=payload, data=data, headers=headers)

    if resp.status_code == 200:
        return 200
    elif resp.status_code == 409:
        return 409
    else:
        return False