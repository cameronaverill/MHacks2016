import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag

class Term:
	#the term constructor
	def __init__(self, name, defns, score):
		self.name = name
		self.bullets = defns
		self.importance = score

	
