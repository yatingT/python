import os
import math

#These first two functions require os operations and so are completed for you
#Completed for you
def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

#Completed for you
def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r',encoding="utf-8") as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

#The rest of the functions need modifications ------------------------------
#Needs modifications
def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    with open(filepath,encoding="utf-8") as doc:
        for word in doc:
            word = word.strip()
            if word not in vocab:
                if None not in bow: 
                    bow[None]=1
                else:
                    bow[None] +=1
            if not word in bow and word in vocab:
                bow[word] = 1
            elif word in vocab:
                bow[word] += 1
    return bow

#Needs modifications
def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """
    smooth = 1 # smoothing factor
    logprob = {}
    count={}
    for i in label_list:
        count[i]=0
    for doc in training_data:
        if doc["label"] == label_list[0]:
            count[label_list[0]]+=1
        else:
            count[label_list[1]]+=1
    total=0
    for i in count:
        total+=count[i]
    for i in count:
        logprob[i]=math.log((count[i]+smooth)/(total+2))

    return logprob

# def prior(training_data, label_list):
#     """ return the prior probability of the label in the training set
#         => frequency of DOCUMENTS
#     """
#     smooth = 1 # smoothing factor
#     logprob = {}
#     count={"2016":0,"2020":0}
#     for doc in training_data:
#         if doc["label"]== "2016":
#             count["2016"]+=1
#         else:
#             count["2020"]+=1
#     total= count["2016"]+count["2020"]
#     for i in count:
#         logprob[i]=ln((count[i]+smooth)/(total+2))

#     return logprob

#Needs modifications
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """
    smooth = 1 # smoothing factor
    word_prob = {}
    for i in vocab: 
        word_prob[i]=0
    total=0
    word_prob[None]=0
    for i in training_data:
        if i["label"]== label:
            for word in i["bow"]:
                total+=i["bow"][word]
                if word in vocab:
                    word_prob[word] += i["bow"][word]
                else:
                    word_prob[None]+=i["bow"][word]
    for i in word_prob:
        word_prob[i]=math.log((word_prob[i]+smooth)/(total+len(vocab)+1))
    return word_prob


##################################################################################
#Needs modifications
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = os.listdir(training_directory)
    vocab=create_vocabulary(training_directory, cutoff)
    training_data=load_training_data(vocab, training_directory)
    retval['vocabulary']=vocab
    retval['log prior']=prior(training_data,label_list)
    retval['p(w|y=2016)']= p_word_given_label(vocab, training_data, '2016')
    retval['p(w|y=2020)']= p_word_given_label(vocab, training_data, '2020')
    return retval

#Needs modifications
def classify(model, filepath):
    retval = {}
    year2016=model["log prior"]["2016"]
    year2020=model["log prior"]["2020"]
    bow = create_bow(model["vocabulary"], filepath)
    for i in bow:
        year2016+=model["p(w|y=2016)"][i]*bow[i]
        year2020+=model["p(w|y=2020)"][i]*bow[i]
    retval["log p(y=2016|x)"]=year2016
    retval["log p(y=2020|x)"]=year2020
    if max(year2016,year2020)==year2016:
        retval['predicted y']="2016"
    else:
        retval['predicted y']="2020"
    return retval
