from bs4 import BeautifulSoup
import os 

file_names = []
for (root, dirs, f) in os.walk('myoutput'):
	for file in f:
		with open(os.path.join(root, file), 'r') as myfile:
			data = myfile.read()
			file_names.append(data)

for f in file_names:
	soup = BeautifulSoup(f, 'html.parser')
	print(soup.prettify())

