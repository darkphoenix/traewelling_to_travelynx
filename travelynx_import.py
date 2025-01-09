import json
import requests
import time
from pprint import pprint
from dateutil.parser import parse

first_load = True

def get_all_statuses_from_traewelling(token):
	statuses = []
	url = "https://traewelling.de/api/v1/user/darkphoenix/statuses"
	while url is not None:
		r = requests.get(url, headers={"Authorization": "Bearer %s" % token}).json()
		print("Fetching statuses from page", r['meta']['current_page'])
		url = r['links']['next']
		time.sleep(1)
		for status in r['data']:
			print("Getting stopovers for", status['train']['lineName'])
			status['stops'] = get_stopovers_from_traewelling(token, status)
			statuses.append(status)
			time.sleep(1)

	return statuses

def get_stopovers_from_traewelling(token, status):
	r = requests.get("https://traewelling.de/api/v1/trains/trip", params={
		"hafasTripId": status['train']['hafasId'],
		"lineName": status['train']['lineName'],
		"start": status['train']['origin']['id'],
	}, headers={"Authorization": "Bearer %s" % token}).json()
	started = False
	stops = []
	for stop in r['data']['stopovers']:
		if stop['id'] == status['train']['destination']['id']:
			print(stops)
			return stops
		if started:
			stops.append(stop['name'])
		if stop['id'] == status['train']['origin']['id']:
			started = True


def post_to_travelynx(token, status):
	if check_is_not_on_travelynx(None, None):
		r = requests.post("https://travelynx.de/api/v1/import", json={
			"token": token,
			"train": {
				"type": status['train']['lineName'].split()[0],
				"line": status['train']['lineName'].split()[1],
				"no": status['train']['journeyNumber'] if status['train']['journeyNumber'] is not None else status['train']['lineName'].split()[1],
			},
			"fromStation": {
				"name": status['train']['origin']['name'],
				"scheduledTime": time.mktime(parse(status['train']['origin']['departurePlanned']).timetuple()),
				"realTime": time.mktime(parse(status['train']['origin']['departure']).timetuple()),
			},
			"toStation": {
				"name": status['train']['destination']['name'],
				"scheduledTime": time.mktime(parse(status['train']['destination']['arrivalPlanned']).timetuple()),
				"realTime": time.mktime(parse(status['train']['destination']['arrival']).timetuple()),
			},
			"intermediateStops": status['stops'],
		})
		pprint(json.loads(r.request.body))
		pprint(r.json())

def check_is_not_on_travelynx(ts, number):
	return True

if first_load:
	token = open("token.secret", "r").read()
	traewelling_statuses = get_all_statuses_from_traewelling(token)
	with open('traewelling.json', 'w') as f:
		json.dump(traewelling_statuses, f)
else:
	with open('traewelling.json', 'r') as f:
		traewelling_statuses = json.load(f)


token = open("travelynx.secret", "r").read()
post_to_travelynx(token, traewelling_statuses[-1])