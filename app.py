from flask import Flask, render_template, request, jsonify, abort, url_for, session, redirect
import threading
import requests
import subprocess
import uuid
from flask_oauth import OAuth
from oauth import OmnAuth

app = Flask(__name__)

oauth = OmnAuth()

background_scripts = {}

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
		'redirect_uri': "http://localhost:5027/auth2"
		}
	req = requests.post('https://api.quizlet.com/oauth/token', data=data, auth=(myClientId, mySecret))
	if req.status_code != 200:
		return "bad request"
	else:
		return "good"

if __name__ == "__main__":
    app.run(debug=True, port=5027)
