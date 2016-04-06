import re
import pickle 
import math

def prob_calc(content, dictionary):
	total_pos = 0
	total_neg = 0
	total_total = 0
	lines = content.splitlines()
	for line in lines:
		total_total = total_total + 1
		words = line.split()
		if "pos" in words:
			total_pos = total_pos + 1
		elif "neg" in words:
			total_neg = total_neg + 1
	print("Total no of +ves : " + str(total_pos))
	print("Total no of -ves : " + str(total_neg))

	vocabs = dictionary.splitlines()
	model = {}
	for vocab in vocabs:
		word_pos = 0
		word_neg = 0
		word_total = 0
		for line in lines:
			if vocab in line:
				if "pos" in line:
					word_pos = word_pos + 1
				elif "neg" in line:
					word_neg = word_neg + 1
				word_total = word_total + 1
		model[vocab] = {"pos" : word_pos, "neg" : word_neg}
	return {"model" : model, "total_pos" : total_pos, "total_neg" : total_neg, "total_total" : total_total}

def word_class_counter(content):
	lines = content.splitlines()
	pos = 0
	neg = 0
	for line in lines:
		words = line.split()
		if "pos" in words:
			pos = pos + len(words) - 1
		elif "neg" in words:
			neg = neg + len(words) - 1
	print("No of words in +ve reviews : " + str(pos))
	print("No of words in -ve reviews : " + str(neg))
	return {"pos" : pos, "neg" : neg}

def smoother(model_and_total, pos_and_neg, content, vocabulary):
	vocabs = vocabulary.split()
	words = content.split()
	smooth_res = {}
	for word in words:
		if word != "pos" and word != "neg":
			if word in model_and_total["model"]:
				res_pos = (model_and_total["model"][word]["pos"] + 1)/(pos_and_neg["pos"] + len(vocabs))
				res_neg = (model_and_total["model"][word]["neg"] + 1)/(pos_and_neg["neg"] + len(vocabs))
			else:
				res_pos = 1/(pos_and_neg["pos"] + len(vocabs))
				res_neg = 1/(pos_and_neg["neg"] + len(vocabs))
			smooth_res[word] = {"pos" : res_pos, "neg" : res_neg}
	return smooth_res

def cond_prob(model_and_total, pos_and_neg, content, smooth_res):
	cond_prob_list = {}
	lines = content.splitlines()
	for line in lines:
		pos_cond = math.log((model_and_total["total_pos"]/model_and_total["total_total"])*list_mult(line, smooth_res, "+"), 2)
		neg_cond = math.log((model_and_total["total_neg"]/model_and_total["total_total"])*list_mult(line, smooth_res, "-"), 2)
		cond_prob_list[line] = {"pos_cond" : pos_cond, "neg_cond" : neg_cond}
	return cond_prob_list

def list_mult(line, smooth_res, arg):
	words = line.split()
	#print(words)
	result = 1
	if arg == "+":
		for word in words:
			if word != "pos" and word != "neg":
				result = result * smooth_res[word]["pos"]
	elif arg == "-":
		for word in words:
			if word != "neg" and word != "pos":
				result = result * smooth_res[word]["neg"]
	return result


def predictor(cond_model):
	pred = {}
	for line in cond_model:
		if cond_model[line]["pos_cond"]>cond_model[line]["neg_cond"]:
			pred[line] = "pos"
		else:
			pred[line] = "neg"
	return pred

def verifier(pred):
	tot_count = 0
	corr_count = 0
	for line in pred:
		words = line.split()
		if words[0] == pred[line]:
			corr_count = corr_count + 1
		tot_count = tot_count + 1
	print("% : " + str(corr_count/tot_count))


if __name__ == "__main__":
	fname = input("Enter name of file : ")
	f_obj = open(fname, "r")
	content = f_obj.read()
	dname = input("Enter name of dictionary : ")
	d_obj = open(dname, "r")
	dictionary = d_obj.read()
	model_and_total = prob_calc(content, dictionary)
	pos_and_neg = word_class_counter(content)
	#print(model_and_total)
	#print(pos_and_neg)
	smooth_result = smoother(model_and_total, pos_and_neg, content, dictionary)
	cond_model = cond_prob(model_and_total, pos_and_neg, content, smooth_result)
	prediction = predictor(cond_model)
	verifier(prediction)

	cond_model_pickled = pickle.dumps(cond_model)
	cond_model_fname = input("Enter filename to save model : ")
	c_obj = open(cond_model_fname, "w")
	c_obj.write(str(cond_model_pickled))
