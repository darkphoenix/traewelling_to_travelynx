import json
import requests
import time

first_load = True

def get_all_statuses_from_traewelling(token):
	url = "https://traewelling.de/api/v1/user/darkphoenix/statuses"
	while url is not None:
		r = requests.get(url, headers={"Authorization": "Bearer %s" % token}).json()
		print("Fetching statuses from page", r['meta']['current_page'])
		url = r['links']['next']
		time.sleep(1)

def get_stopovers_from_traewelling():
	pass

def post_to_travelynx(status):
	if check_is_not_on_travelynx(date, number):
		pass

def check_is_not_on_travelynx(date, number):
	pass

if first_load:
	token = open("token.secret", "r").read()
	traewelling_statuses = get_all_statuses_from_traewelling(token)
	with open('traewelling.json', 'w') as f:
		json.dump(traewelling_statuses, f)
else:
	with open('traewelling.json', 'r') as f:
		traewelling_statuses = json.load(f)