from flask import Flask, render_template, request, jsonify, abort, url_for
import threading
import subprocess
import uuid
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
mongo = PyMongo(app)
client = MongoClient()
db = client.test_database
entries = db.entries

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
  return render_template('index.html')

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


if __name__ == "__main__":
    app.run(debug=True)