
import requests
import ast
import json

import authhelper
import secrets
import quizletsets

from flask import request, redirect, make_response
import app
import httplib, urllib

@app.route("/quizletauth")
def auth1():
	clientID = 'ZsDq2bcC9e'
	randomStateString = "quiwas"
	redirectUrl = "https://quizlet.com/authorize?response_type=code&client_id=" + clientId + "&scope=read+write_set+write_group&state=" + randomStateString	
	authorizeUrl = "https://quizlet.com/authorize?client_id=" + clientID + "&response_type=code&scope=read+write_set"
	url = authorizeUrl + "&state=" + randomStateString + "&redirect_uri=" + redirectUrl
	return redirect(url)


@app.route("/quizletauthstep2")
def authparam():

	tokenUrl = "https://api.quizlet.com/oauth/token"
	randomStateString = "quiwas"
	clientID = 'ZsDq2bcC9e'
	keySecret = '123'

	state = request.args.get('state')
	if state != randomStateString:
		return "Didn't receive correct state"

	code = request.args.get('code')
	grant_type = "authorization_code"
	redirect_uri = "https://quizlet.com/authorize?response_type=code&client_id=" + clientId + "&scope=read+write_set+write_group&state=" + randomStateString
	payload = {'code' : code, 'grant_type' : grant_type, 'redirect_uri' : redirect_uri}

	req = requests.post(tokenUrl, data=payload, auth=(clientID, keySecret))
	if req.status_code != 200 :
		return "Bad Request"
	else :
		receivedPayload = ast.literal_eval(req.text)
		accessToken = receivedPayload['access_token']
		userId = receivedPayload['user_id']
		jsonData = {}
		jsonData['id'] = userId
		jsonData['token'] = accessToken
		apiUrl = 'https://api.quizlet.com/2.0/users/cameronaverill?whitespace=1'

		
