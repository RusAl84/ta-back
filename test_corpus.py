# List with 2 sentences
from pprint import pprint

from gensim import corpora
from gensim.utils import simple_preprocess

my_docs = ["Who let the dogs out?",
           "Who? Who? Who? Who?"]
# Tokenize the docs
tokenized_list = [simple_preprocess(doc) for doc in my_docs]
print(tokenized_list)
# Create the Corpus
mydict = corpora.Dictionary()
mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list]
pprint(mycorpus)
#> [[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)], [(4, 4)]]