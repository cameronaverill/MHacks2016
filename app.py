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
import sys
from io import BytesIO

from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
mongo = PyMongo(app)
client = MongoClient()
db = client.test_database
entries = db.entries

oauth = OmnAuth()

background_scripts = {}

class FuncThread(threading.Thread):
	def __init__(self, target, *args):
		self._target = target
		self._args = args
		threading.Thread.__init__(self)

	def run(self):
		self._target(*self._args)

def run_script(id, pages, link):
	subprocess.call(["python", "extractText.py", pages, link], shell=False)
	background_scripts[id] = True

@app.route("/")
def main():
	pdfLink=""
	pages =""
	return render_template('index.html', pdfLink, pages)

@app.route("/process", methods=['POST'])
def generate():
	db.entries.delete_many({})
	link = request.form['pdfLink']
	pages = request.form['pages']
	id = str(uuid.uuid4())
	background_scripts[id] = False

	t = FuncThread(run_script, id, pages, link)
	t.start()
	t.join()
	print entries.find
	return render_template('test.html', entries=entries)

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
		'redirect_uri': "http://localhost:5033/auth2"
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
	buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, post_url)
	c.setopt(c.WRITEDATA, buffer)
	c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer ' + token])
	c.setopt(pycurl.POSTFIELDS, data)
	c.perform()
	c.close()
	body = buffer.getvalue()
	strstart = body.find('url')
	slashStart = body.find('/\"')
	strDesired = body[strstart + 6: slashStart]
	return redirect("http://quizlet.com" + strdesired)



if __name__ == "__main__":
    app.run(debug=True, port=5033)
