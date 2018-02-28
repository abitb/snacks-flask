import requests

ApiKey = "a1bacf53-c847-4b5d-81fa-822b8138ecda"

def get_snacks_from_web_service():
	"""
	get current list of snack foods from Nerdery web service
	:returns: list of dicts, of snack info (in unicode)
	:returns: False if web service is not working
	"""
	payload = {"ApiKey": ApiKey}
	resp = requests.get("https://api-snacks.nerderylabs.com/v1/snacks/", params=payload)

	if resp.status_code == 200:
	# {id, lastPurchaseDate, name, optional, purchaseCount, purchaseLocations}
		return resp.json()
	else:
		return False

def separate_optional_snacks(snacks_from_ws):
	"""
	take response from webservice and return 2 lists depending on if
	the snack is optional
	:param snacks_from_ws: list of dicts, data structure returned from nerdery webservice
	:returns: tuple of 2 lists -- always_purchased and suggested_so_far
	"""
	always_purchased = []
	suggested_so_far = []
	for snack in snacks_from_ws:
	    if snack["optional"] == False:
	        always_purchased.append(snack)
	    else:
	        suggested_so_far.append(snack)
	return (always_purchased, suggested_so_far)

# lastPurchaseDate maybe empty