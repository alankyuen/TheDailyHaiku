import numpy as np
import kenlm
import pyphen
import random
import boto3
import json
import grammar_check
from hyphen import Hyphenator

tool = grammar_check.LanguageTool('en-US')
h_en = Hyphenator('en_US')
s3 = boto3.resource('s3')
polly = boto3.client('polly')

SCORE_MULTIPLIER = 1
VOCAB_THRESHOLD = 750 #choose from the top n words
NUM_WORDS = 9

SEED_PATH = "/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/college_seed.txt"
MODEL_PATH = "/Users/alanyuen/.virtualenvs/SBHacks/kenlm/cbt.klm"#gutenberg100.klm
VOCAB_PATH = "/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/Vocab/oxford3000.txt"#""
COMMON_PATH = "/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/Vocab/count_1w100k.txt"

model = kenlm.LanguageModel(MODEL_PATH)

with open(COMMON_PATH, 'r') as f:
    #common = f.readline().split("|")#words_copy_unique.txt
    #common = [line.rstrip().lower() for line in common]
    common = f.readlines()[:50]
    common = [line.rstrip().lower() for line in common]
with open(VOCAB_PATH, 'r') as f:
    vocab = f.readlines()[:1000]
    vocab = [line.rstrip().lower() for line in vocab]
with open(SEED_PATH, 'r') as f:
    seed = f.readlines()
    seed = [line.rstrip() for line in seed]


#######################################################################################


def complete_ngram(vocab, model, context, index, insert = True, top_ = VOCAB_THRESHOLD):
    scores = [0]*len(vocab)

    if(insert):
        context.insert(index,"")

    for i in range(len(vocab)):
        context[index] = vocab[i]
        sentence = " ".join(context)
        scores[i] = -model.score(sentence)

    vocab = np.array(vocab)
    scores = np.array(scores)
    inds = scores.argsort()
    vocab = vocab[inds]

    scores = [i*SCORE_MULTIPLIER for i in reversed(range(top_))]
    s = sum(scores)
    scores = [float(i)/s for i in scores]
    #print(zip(vocab[:top_],scores[:top_]))
    choice_list = np.random.choice(vocab[:top_], 1, replace=True, p=scores[:top_])
    context[index] = choice_list[0]
    return context


def forward_pass(vocab, model, sentence, pass_range = [], skip_index = []):
    #revision
    if(len(pass_range) == 0):
        pass_range = [0, len(sentence)]
    elif(len(pass_range) == 1):
        pass_range.append(len(sentence))
    for i in range(pass_range[0],pass_range[1]):
        if(i not in skip_index):
            sentence = complete_ngram(vocab, model, sentence, i, insert = False)
    return sentence


def backward_pass(vocab, model, sentence, pass_range = [], skip_index = []):
    if(len(pass_range) == 0):
        pass_range = [0, len(sentence)]
    elif(len(pass_range) == 1):
        pass_range.append(len(sentence)-1)
    for i in reversed(range(pass_range[0],pass_range[1])):
        if(i not in skip_index):
            sentence = complete_ngram(vocab, model, sentence, i, insert = False)
    return sentence


def generate_sentence(vocab, model, common, seed, seed_index = 2, num_words = NUM_WORDS):
    sentence = [random.choice(common)] #or common noun?
    for i in range(num_words-1):
        #if(i == seed_index):
            #sentence = complete_ngram(seed, model, sentence, 1, i+1)
        #else:
        sentence = complete_ngram(vocab, model, sentence, 1, i+1)

    return sentence


def nsyl(word):
   return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]


def total_syllables(words):
    sum_syl = 0
    dic = pyphen.Pyphen(lang='nl_NL')
    for w in words:
        sum_syl += len(h_en.syllables(unicode(w)))#len(dic.inserted(w).split("-"))
    return sum_syl


#######################################################################################


for run in range(10):

    haiku = []

    for syls in [5,7,5]:
        found_line = False

        while(not found_line):

            grammar_flag = False
            seed_index = random.randint(0,NUM_WORDS)#seed
            sentence = generate_sentence(vocab, model, common, seed, seed_index)

            for i in range(len(sentence)-1):
                text = " ".join(sentence[i:i+1])
                matches = tool.check(text)
                if(len(matches) > 0):
                    grammar_flag = True
                    break
            if(grammar_flag):
                continue

            possible_lines = []
            for i in range(len(sentence)):
                for j in range(i):
                    if(total_syllables(sentence[j:j+len(sentence)-i]) == syls):
                        possible_lines.append(sentence[j:j+len(sentence)-i])

            if(len(possible_lines) == 0):
                if(VOCAB_THRESHOLD/1.25 > 10):
                    VOCAB_THRESHOLD = int(VOCAB_THRESHOLD/1.25)
                else:
                    VOCAB_THRESHOLD = 10
                forward_pass(vocab,model,sentence,pass_range=[1])
                #backward_pass(vocab,model,sentence,pass_range=[0])
            else:
                score_lines = [model.score(" ".join(line)) for line in possible_lines]
                score_lines.sort()
                sentence = possible_lines[score_lines.index(max(score_lines))]
                found_line = True

        haiku += [" ".join(sentence)]

    haiku_text_formatted = "\n\t".join(haiku)
    haiku_text = ",".join(haiku)
    print ("#" + str(run+1) +":"+haiku_text_formatted)
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=haiku_text,
        VoiceId='Nicole'
    )
    with open(haiku_text+'.mp3','wb') as f:#with open(haiku_text+'.mp3','wb') as f:
        f.write(response['AudioStream'].read())
        f.close()
