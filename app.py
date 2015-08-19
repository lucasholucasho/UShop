from __future__ import absolute_import

import json
import os
from urlparse import urlparse

from flask import Flask, render_template, request, redirect, session
from flask_sslify import SSLify
from rauth import OAuth2Service
import requests

app = Flask(__name__, static_folder='static', static_url_path='')
app.requests_session = requests.Session()
app.secret_key = os.urandom(24)

sslify = SSLify(app)

with open('config.json') as f:
    config = json.load(f)


def generate_oauth_service():
    return OAuth2Service(
        client_id=os.environ.get('UBER_CLIENT_ID'),
        client_secret=os.environ.get('UBER_CLIENT_SECRET'),
        name=config.get('name'),
        authorize_url=config.get('authorize_url'),
        access_token_url=config.get('access_token_url'),
        base_url=config.get('base_url'),
    )


def generate_ride_headers(token):
    return {
        'Authorization': 'bearer %s' % token,
        'Content-Type': 'application/json',
    }


@app.route('/health', methods=['GET'])
def health():
    return ';-)'

@app.route('/', methods=['GET'])
def signup():
    params = {
        'response_type': 'code',
        'redirect_uri': get_redirect_uri(request),
        'scope': ' '.join(config.get('scopes'))
    }
    url = generate_oauth_service().get_authorize_url(**params)
    return redirect(url)


@app.route('/submit', methods=['GET'])
def submit():
    params = {
        'redirect_uri': get_redirect_uri(request),
        'code': request.args.get('code'),
        'grant_type': 'authorization_code'
    }

    response = app.requests_session.post(
        config.get('access_token_url'),
        auth=(
            os.environ.get('UBER_CLIENT_ID'),
            os.environ.get('UBER_CLIENT_SECRET')
        ),
        data=params,
    )

    session['access_token'] = response.json().get('access_token')

    return render_template(
        'success.html',
        token=response.json().get('access_token')
    )


@app.route('/demo', methods=['GET'])
def demo():
    info_about_user = me()
    return render_template('demo.html', user_name = info_about_user["first_name"], token=session.get('access_token'))

@app.route('/shoppingsearch/<string:product>/<string:latitude>/<string:longitude>', methods=['GET'])
def shoppingSearch(product, latitude, longitude):
	url = config.get('base_retailigence_url') + 'products'
	params = {
		'apiKey': config.get('retailigence_api_key'),
		'requestorid': config.get('retailigence_requrestorid'),
		'userlocation': latitude + ',' + longitude,
		'keywords': product
	}
	response = app.requests_session.get(
		url,
		params=params
	)
	if response.status_code != 200:
		return 'There was an error', response.status_code
	results_to_show = None
	if "results" in response.json()["RetailigenceSearchResult"]:
		results_to_show =  response.json()["RetailigenceSearchResult"]["results"]
	return render_template(
		'shoppingProducts.html',
		results=results_to_show,
		product=product,
		latitude=latitude,
		longitude=longitude
	)

@app.route('/hailUber/<string:start_latitude>/<string:start_longitude>/<string:end_latitude>/<string:end_longitude>', methods=['GET'])
def hailUber(start_latitude, start_longitude, end_latitude, end_longitude, surge_confirmation_id=None):	
	url = config.get('base_uber_sandbox_url') + 'requests'
	params = {
		'product_id': config.get('uber_product_id'),
		'start_latitude': start_latitude,
		'start_longitude': start_longitude,
		'end_latitude': end_latitude,
		'end_longitude': end_longitude,
		'surge_confirmation_id': surge_confirmation_id
	}
	session['start_latitude'] = start_latitude
	session['start_longitude'] = start_longitude
	session['end_latitude'] = end_latitude
	session['end_longitude'] = end_longitude
	response = app.requests_session.post(
		url,
		headers=generate_ride_headers(session.get('access_token')),
		data=json.dumps(params)
	)
	json_of_response = response.json()
	if response.status_code == 202:
		return render_template(
			'calledUber.html',
			request_id = json_of_response["request_id"],
			eta = json_of_response["eta"]
		)
	if response.status_code == 409 and json_of_response["meta"] is not None:
		return redirect(json_of_response["meta"]["surge_confirmation"]["href"])

@app.route('/surge', methods=['GET'])
def surge():
	surge_confirmation_id = request.args.get('surge_confirmation_id')
	return hailUber(session['start_latitude'], session['start_longitude'], session['end_latitude'], session['end_longitude'], surge_confirmation_id)


@app.route('/me', methods=['GET'])
def me():
    url = config.get('base_uber_url') + 'me'
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
    )
    return response.json()


def get_redirect_uri(request):
    parsed_url = urlparse(request.url)
    if parsed_url.hostname == 'localhost':
        return 'http://{hostname}:{port}/submit'.format(
            hostname=parsed_url.hostname, port=parsed_url.port
        )
    return 'https://{hostname}/submit'.format(hostname=parsed_url.hostname)

if __name__ == '__main__':
    app.debug = os.environ.get('FLASK_DEBUG', True)
    app.run(port=7000)
