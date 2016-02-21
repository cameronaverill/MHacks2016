from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import Term

terms = Blueprint('terms', __name__, template_folder='templates')

class listView(MethodView):

	def get(self):
		terms = Term.objects.all()
		return render_template('terms/list.html', terms=terms)

terms.add_url_rule('/', view_func=ListVIew.as_view('list'))