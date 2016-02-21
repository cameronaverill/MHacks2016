from app import db

class Term(db.Document):
	term = db.StringField(required=True)
	definition = db.StringField(required=True)

