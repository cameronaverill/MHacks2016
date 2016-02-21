from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
		# return "Welcome!"
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generateSkim():
	link = request.form['pdfLink']


if __name__ == "__main__":
    app.run(debug=True)