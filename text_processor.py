# python 3.x code
import re

def processor(text, stop_words):
	text = text.lower()
	newtext = ""
	regex = re.compile('[,":;?-]')
	regex2 = re.compile("['’]")
	text = regex.sub('', text)
	text = regex2.sub('', text)
	elements = text.split()
	for element in elements:
		if element not in stop_words:
			newtext = newtext + " " + element
	return newtext

if __name__=="__main__":
	raw_file_name = input("Enter name of raw file : ")
	stop_words_file_name = input("Enter name of file containing stop words : ")
	r_inp = open(raw_file_name, "r")
	s_inp = open(stop_words_file_name, "r")
	processed_text = processor(r_inp.read(), s_inp.read())
	pr_file_name = input("Enter name of output file : ")
	p_op = open(pr_file_name, "w")
	p_op.write(processed_text)


