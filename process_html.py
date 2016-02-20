from bs4 import BeautifulSoup
import os 

#generate a beautiful soup file for each fil ein the myoutput directory
file_names = []
for (root, dirs, f) in os.walk('myoutput'):
	for file in f:
		with open(os.path.join(root, file), 'r') as myfile:
			data = myfile.read()
			file_names.append(data)

#generates the divs of all paragraphs containing any term
for f in file_names:
	soup = BeautifulSoup(f, 'html.parser')
	bold_term_tags = soup.findAll("span", attrs={'style': 'font-family: HIEILF+StoneSerif-Bold-20-0; font-size:9px'})
	parent_tags = []
	for t in bold_term_tags:
		parent_tags.append(t.parent)
		print parent_tags[len(parent_tags) - 1].get_text()
