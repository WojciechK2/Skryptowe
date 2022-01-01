from nltk.book import *

wall_street = text7.tokens

import re

tokens = wall_street

def cleanup():
	compiled_pattern = re.compile("^[a-zA-Z0-9.!?]")
	clean = list(filter(compiled_pattern.match,tokens))
	return clean

tokens = cleanup()

def build_ngrams():
	ngrams = []
	for i in range(len(tokens)-N+1):
		ngrams.append(tokens[i:i+N])
	#print(ngrams)
	return ngrams

def ngram_freqs(ngrams):
    counts = {}

    for ngram in ngrams:
        token_seq  = SEP.join(ngram[:-1])
        last_token = ngram[-1]

        if token_seq not in counts:
            counts[token_seq] = {}

        if last_token not in counts[token_seq]:
            counts[token_seq][last_token] = 0

        counts[token_seq][last_token] += 1;

    return counts;
    
def next_word(text, N, counts):

	token_seq = SEP.join(text.split()[-(N-1):])
	choices = counts[token_seq].items()
	
	total = sum(weight for choice, weight in choices)
	r = random.uniform(0, total)
	upto = 0
	
	for choice, weight in choices:
		upto += weight
		if upto > r: return choice
	assert False

def clean_generated(generated):
	
	return_string = ""
	sentence_list = generated.split('.')
	
	for s in sentence_list:
	
		if len(s) > 0:
			return_string += s[0].upper()
			return_string += s[1:]
			return_string = return_string[0:-1]+'.'
		elif len(s) == 1:
			return_string += s

	return return_string

import random

N=5 # fix it for other value of N

SEP=" "

sentence_count=5

ngrams = build_ngrams()
start_seq="Was named a nonexecutive"

counts = ngram_freqs(ngrams)

if start_seq is None: start_seq = random.choice(list(counts.keys()))
generated = start_seq.lower();

sentences = 0
while sentences < sentence_count:
    generated += SEP + next_word(generated, N, counts)
    sentences += 1 if generated.endswith(('.','!', '?')) else 0

print(clean_generated(generated))
