from flask import Flask, render_template, request, jsonify, abort, url_for, session, redirect
import threading
import requests
import subprocess
import uuid
from flask_oauth import OAuth
from oauth import OmnAuth
import ast
import pycurl, json
from StringIO import StringIO

app = Flask(__name__)

oauth = OmnAuth()

background_scripts = {}

o = StringIO()
h = StringIO()

def run_script(id, pages, link):
	subprocess.call("extractText.py", pages, link)
	background_scripts[id] = True

@app.route("/")
def main():
	pdfLink=""
	pages =""
	return render_template('index.html', pdfLink, pages)

@app.route('/', methods=['POST'])
def generate():

	link = request.form['pdfLink']
	pages = request.form['pages']
	id = str(uuid.uuid4())
	background_scripts[id] = False
	threading.Thread(target=lambda: run_script(id, pdfLink, pages)).start()
	return render_template('test.html', id=id)

@app.route('/auth1')
def auth1():
	return redirect(oauth.redirect_user())

@app.route('/auth2', methods=['GET', 'POST'])
def auth2():
	code = request.args.get('code')
	myClientId = 'ZsDq2bcC9e'
	mySecret = 'dEHBPDNqyWt8wtcA7VcdeK'
	data = {'grant_type': 'authorization_code',
		'code': code, 
		'redirect_uri': "http://localhost:5032/auth2"
		}
	req = requests.post('https://api.quizlet.com/oauth/token', data=data, auth=(myClientId, mySecret))
	if req.status_code != 200:
		return "bad request"
	receivedPayload = ast.literal_eval(req.text)
	print receivedPayload
	terms = request.form.getlist(('terms[]'))
	token = receivedPayload['access_token']
	headers = {"Authorization": token}
	post_url = "https://api.quizlet.com/2.0/sets"
	data = json.dumps({'title': 'turtle',
	'terms': ['dog', 'cat'], 
	'definitions': ['roof', 'meow'],
	'lang_terms': 'en',
	'lang_definitions': 'en'})
	c = pycurl.Curl()
	c.setopt(pycurl.URL, post_url)
	c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer ' + token])
	c.setopt(pycurl.POSTFIELDS, data)
	c.perform()
	
	return redirect("http://quizlet.com" + "/122703621/turtle-flash-cards/")

if __name__ == "__main__":
    app.run(debug=True, port=5032)
