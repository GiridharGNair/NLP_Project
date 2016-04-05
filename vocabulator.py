# python 3 code

def vocabulator(text):
	init_vocab = {}
	final_vocab = ""
	words = text.split()
	for word in words:
		print(word)
		if not (word == "pos" or word == "neg"):
			if (word not in init_vocab):
				init_vocab[word] = 1
			else:
				init_vocab[word] = init_vocab[word] + 1
	for word in init_vocab:
		if init_vocab[word] >= 2:
			final_vocab = final_vocab+word+"\n"
	return final_vocab



if __name__ == "__main__":
	fname = input("Enter name of data file : ")
	inp_file_obj = open(fname, "r")
	vocab = vocabulator(inp_file_obj.read())
	fname = input("Enter file to save vocabulary to : ")
	op_file_obj = open(fname, "w")
	op_file_obj.write(vocab)