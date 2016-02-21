from bs4 import BeautifulSoup
import subprocess
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
import os
from term import Term
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from app import db


#generate a beautiful soup file for each fil ein the myoutput directory
file_names = []
for (root, dirs, f) in os.walk('myoutput'):
	for file in f:
		with open(os.path.join(root, file), 'r') as myfile:
			data = myfile.read()
			file_names.append(data)

#generates the divs of all paragraphs containing any term
bold_term_tags = []
bold_term_text = []
parent_tags = []
paragraphs = []
term_and_def = {}

for f in file_names:
	soup = BeautifulSoup(f, 'html.parser')
	for t in soup.findAll("span", attrs={'style': 'font-family: OTQPIH+StoneSerif-Bold; font-size:9px'}):
		bold_term_tags.append(t)
		text = t.get_text()
		bold_term_text.append(text)
		parent_tags.append(t.parent)
		paragraphs.append(t.parent.get_text())
		term_and_def[text] = []
		sents = sent_tokenize(t.parent.get_text())
		# print sents
		for s in sents:
			if text in s:
				tdef = term_and_def[text]
				tdef.append(s.replace('\n', ' ').replace('- ', ''))
				term_and_def[text] = tdef

terms = []
for t in bold_term_text:
	terms.append(Term(t, term_and_def[t], 0))
	entry = {"term" : terms[len(terms) - 1].name,
					 "definition" : terms[len(terms) - 1].bullets}
	entry_id = db.entries.insert_one(entry).inserted_id

	# print db.collection.find_one({"_id": entry_id})

	# print terms[len(terms) - 1].name
	# print terms[len(terms) - 1].bullets


subprocess.call(["rm", "-rf", "myoutput"])

