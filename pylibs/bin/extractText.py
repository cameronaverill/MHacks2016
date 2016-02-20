import subprocess;
from sys import argv
import urllib2

script, pages, pdfLink = argv;

pdfFileName = "temp.pdf"

pdfFile = urllib2.urlopen(pdfLink)
file = open(pdfFileName, 'wb')
file.write(pdfFile.read())
file.close()

subprocess.call(["pdf2txt.py", "-o", "myfile.html", "-t", "html", "-p", pages, pdfFileName])

subprocess.call(["rm", pdfFileName])
