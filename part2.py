import pickle
import math

def unigram_vocab_gen(processed_data):
	unigram_initial_list = {}
	unigram_vocab = []
	unigram_count = 0
	lines = processed_data.splitlines()
	for line in lines:
		words = line.split()
		for word in words:
			if word != "pos" and word != "neg":
				if word not in unigram_initial_list:
					unigram_initial_list[word] = 1
				else:
					unigram_initial_list[word] += 1
	for unigram in unigram_initial_list:
		if unigram_initial_list[unigram] >= 2:
			unigram_vocab.append(unigram)
			unigram_count += 1
	return unigram_vocab, unigram_count


def unigram_stats_gen(processed_data, unigram_vocab):
	unigram_stats = {}
	unigram_total_pos = 0
	unigram_total_neg = 0
	lines = processed_data.splitlines()
	for line in lines:
		words = line.split()
		for word in words:
			if word in unigram_vocab:
				if words[0] == "pos":
					if word != "pos" and word != "neg":
						if word not in unigram_stats:
							unigram_stats[word] = {"pos" : 1, "neg" : 0}
							unigram_total_pos += 1
						else:
							unigram_stats[word]["pos"] += 1
				if words[0] == "neg":
					if word != "pos" and word != "neg":
						if word not in unigram_stats:
							unigram_stats[word] = {"pos" : 0, "neg" : 1}
							unigram_total_neg += 1
						else:
							unigram_stats[word]["neg"] += 1
	return unigram_stats, unigram_total_pos, unigram_total_neg


def bigram_vocab_gen(processed_data):
	bigram_initial_list = {}
	bigram_vocab = []
	bigram_count = 0
	lines = processed_data.splitlines()
	for line in lines:
		words = line.split()
		for i in range(1, len(words) - 2):
			bigram = words[i] + " " + words[i + 1]
			if bigram not in bigram_initial_list:
				bigram_initial_list[bigram] = 1
			else:
				bigram_initial_list[bigram] += 1
	for bigram in bigram_initial_list:
		if bigram_initial_list[bigram] >= 2:
			bigram_vocab.append(bigram)
			bigram_count += 1
	return bigram_vocab, bigram_count


def bigram_stats_gen(processed_data, bigram_vocab, unigram_stats, unigram_total_pos, unigram_total_neg):
	bigram_stats = {}
	bigram_total_pos = 0
	bigram_total_neg = 0
	lines = processed_data.splitlines()
	for line in lines:
		words = line.split()
		for i in range(1, len(words) - 2):
			bigram = words[i] + " " + words[i + 1]
			if bigram in bigram_vocab:
				if words[0] == "pos":
					if bigram not in bigram_stats:
						bigram_stats[bigram] = {"pos" : 1, "neg" : 0}
						bigram_total_pos += 1
					else:
						bigram_stats[bigram]["pos"] += 1
					if i == 1:
						if words[i] in unigram_stats:
							unigram_stats[words[i]]["pos"] -= 1
							unigram_total_pos -= 1
					if words[i + 1] in unigram_stats:
						unigram_stats[words[i + 1]]["pos"] -= 1
						unigram_total_pos -= 1
				elif words[0] == "neg":
						if bigram not in bigram_stats:
							bigram_stats[bigram] = {"pos" : 0, "neg" : 1}
							bigram_total_neg += 1
						else:
							bigram_stats[bigram]["neg"] += 1
						if i == 1:
							if words[i] in unigram_stats:
								unigram_stats[words[i]]["neg"] -= 1
								unigram_total_neg -= 1
						if words[i + 1] in unigram_stats:
							unigram_stats[words[i + 1]]["neg"] -= 1
							unigram_total_neg -= 1
	return bigram_stats, bigram_total_pos, bigram_total_neg, unigram_stats, unigram_total_pos, unigram_total_neg


def predictor(test_contents, bigram_stats, bigram_total_pos, bigram_total_neg, unigram_stats, unigram_total_pos, unigram_total_neg, bigram_vocab, unigram_vocab, unigram_count):
	lines = test_contents.splitlines()
	line_probs = {}
	predictions = {}
	correct = 0
	total = 0
	for line in lines:
		words = line.split()
		line_prob_pos = 1
		line_prob_neg = 1
		for i in range(0, len(words) - 1):
			temp_bigram = words[i] + " " + words[i + 1]
			if temp_bigram in bigram_vocab:
				line_prob_pos = line_prob_pos * (bigram_stats[temp_bigram]["pos"] / bigram_total_pos)
				line_prob_neg = line_prob_neg * (bigram_stats[temp_bigram]["neg"] / bigram_total_neg)
				i += 1
			elif words[i] in unigram_vocab:
				line_prob_pos = line_prob_pos * ((unigram_stats[words[i]]["pos"] + 1) / (unigram_total_pos + unigram_count))
				line_prob_neg = line_prob_neg * ((unigram_stats[words[i]]["neg"] + 1)/ (unigram_total_neg + unigram_count))
			else:
				line_prob_pos = line_prob_pos * (1/unigram_count)
				line_prob_neg = line_prob_neg * (1/unigram_count)
		line_probs[line] = {"pos" : line_prob_pos, "neg" : line_prob_neg}
	for line in line_probs:
		if line_probs[line]["pos"] > line_probs[line]["neg"]:
			predictions[line] = "pos"
		else:
			predictions[line] = "neg"
	# print(predictions)
	for line in lines:
		words = line.split()
		if words[0] == predictions[line]:
			correct += 1
		total += 1
	return correct/total


if __name__ == "__main__":
	fname = input("Enter name of data file (processed) : ")
	fd = open(fname, "r")
	processed_data = fd.read()
	fd.close()
	unigram_vocab, unigram_count = unigram_vocab_gen(processed_data)
	unigram_stats, unigram_total_pos, unigram_total_neg = unigram_stats_gen(processed_data, unigram_vocab)
	# print(unigram_vocab)
	# print(unigram_count)
	# print(unigram_stats)
	# print(unigram_total_pos)
	# print(unigram_total_neg)
	unigram_model = pickle.dumps({"vocab" : unigram_vocab, "count" : unigram_count, "total_pos" : unigram_total_pos, "total_neg" : unigram_total_neg})
	bigram_vocab, bigram_count = bigram_vocab_gen(processed_data)
	# print(bigram_vocab)
	# print(bigram_count)
	bigram_stats, bigram_total_pos, bigram_total_neg, unigram_stats, unigram_total_pos, unigram_total_neg = bigram_stats_gen(processed_data, bigram_vocab, unigram_stats, unigram_total_pos, unigram_total_neg)
	# print(bigram_stats)
	# print(unigram_stats)
	# print(bigram_total_pos)
	# print(bigram_count)
	# print(unigram_total_pos)
	# print(unigram_total_neg)
	total_vocab_size = bigram_count + unigram_count
	# print(total_vocab_size)
	sec_fname = input("Enter name of test set : ")
	sec_fd = open(sec_fname, "r")
	test_contents = sec_fd.read()
	accuracy = predictor(test_contents, bigram_stats, bigram_total_pos, bigram_total_neg, unigram_stats, unigram_total_pos, unigram_total_neg, bigram_vocab, unigram_vocab, unigram_count)
	print(accuracy)