from flask import Flask, render_template, request, jsonify, abort, url_for
import threading
import subprocess
import uuid

app = Flask(__name__)

background_scripts = {}

def run_script(id, pages, link):
	subprocess.call(["python", "extractText.py", pages, link], shell=False)
	background_scripts[id] = True

@app.route("/")
def main():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def generate():

	link = request.form['pdfLink']
	pages = request.form['pages']
	id = str(uuid.uuid4())
	background_scripts[id] = False
	threading.Thread(target=lambda: run_script(id, pages, link)).start()
	return render_template('test.html', id=id)




if __name__ == "__main__":
    app.run(debug=True)