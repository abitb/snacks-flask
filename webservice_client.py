import requests

APIKEY = "a1bacf53-c847-4b5d-81fa-822b8138ecda"
SNACK_URL = "https://api-snacks.nerderylabs.com/v1/snacks/"

test1 = [{
u'id': 1000,
u'lastPurchaseDate': u'1/22/2018',
u'name': u'Ramen',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'Whole Foods'},
{u'id': 1001,
u'lastPurchaseDate': u'12/28/2017',
u'name': u'Pop Tarts',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'Cub Foods'},
{u'id': 1002,
u'lastPurchaseDate': u'12/28/2017',
u'name': u'Corn Nuts',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'Cub Foods'},
{u'id': 1003,
u'lastPurchaseDate': u'1/15/2018',
u'name': u'Bagels',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'Cub Foods'},
{u'id': 1004,
u'lastPurchaseDate': u'1/15/2018',
u'name': u'Wasabi Peas',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'CVS'},
{u'id': 1005,
u'lastPurchaseDate': u'1/8/2018',
u'name': u'Mixed Nuts',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'CVS'},
{u'id': 1006,
u'lastPurchaseDate': u'1/12/2018',
u'name': u'Bananas',
u'optional': False,
u'purchaseCount': 1,
u'purchaseLocations': u'Whole Foods'}
,
{u'id': 1007,
u'lastPurchaseDate': u'1/12/2018',
u'name': u'Test snack 2',
u'optional': True,
u'purchaseCount': 1,
u'purchaseLocations': u'test location'}
]

def get_snacks_from_web_service():
    """
    get current list of snack foods from Nerdery web service
    :returns: list of dicts, of snack info (in unicode)
    :returns: False if web service is not working
    """
    # payload = {"ApiKey": APIKEY}
    # resp = requests.get(SNACK_URL, params=payload)

    # if resp.status_code == 200:
    # # [{id, lastPurchaseDate, name, optional, purchaseCount, purchaseLocations},..]
    #     return resp.json()
    # else:
    #     return False
    return test1

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
    # headers = {"content-type":"application/json"}
    # payload = {"ApiKey": APIKEY}
    # data = json.dumps({"name":name, "location":location})
    # resp = requests.post("https://api-snacks.nerderylabs.com/v1/snacks/", params=payload, data=data, headers=headers)

    # if resp.status_code == 200:
    #     return 200
    # elif resp.status_code == 409:
    #     return 409
    # else:
    #     return False

    # test1.append({'id':testid,'lastPurchaseDate': '','name': name,'optional': True,'purchaseCount': 1,'purchaseLocations': location})
    return 200