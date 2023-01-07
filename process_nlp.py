import string
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2
import json
# from gensim.summarization import summarize
from summarizer import Summarizer
from rake_nltk import Metric, Rake
import yake


def load_data(self, filename='data.txt'):
    with open(filename, "r", encoding='utf-8') as file:
        data = file.read()


def remove_digit(data):
    str2 = ''
    for c in data:
        if c not in ('0', "1", '2', '3', '4', '5', '6', '7', '8', '9', '«', '»', '–', "\""):
            str2 = str2 + c
    data = str2
    return data


def remove_punctuation(data):
    str2 = ''
    pattern = string.punctuation
    for c in data:
        if c not in pattern:
            str2 = str2 + c
        else:
            str2 = str2 + ""
    data = str2
    return data


def remove_stopwords(data):
    str2 = ''
    russian_stopwords = stopwords.words("russian")
    for word in data.split():
        if word not in (russian_stopwords):
            str2 = str2 + " " + word
    data = str2
    return data


def remove_short_words(data, length=1):
    str2 = ''
    for line in data.split("\n"):
        str3 = ""
        for word in line.split():
            if len(word) > length:
                str3 += " " + word
        str2 = str2 + "\n" + str3
    data = str2
    return data


def remove_paragraf_to_lower(data):
    data = data.lower()
    data = data.replace('\n', ' ')
    return data


def remove_all(data):
    data = remove_digit(data)
    data = remove_punctuation(data)
    data = remove_stopwords(data)
    data = remove_short_words(data, length=1)
    data = remove_paragraf_to_lower(data)
    return data


def print_TFIDF(self, records_count=10):
    tfIdfTransformer = TfidfVectorizer(ngram_range=(
        1, 4), use_idf=True, max_features=records_count)
    countVectorizer = CountVectorizer(
        ngram_range=(1, 4), max_features=records_count)
    wordCount = countVectorizer.fit_transform([data])
    TfIdf = tfIdfTransformer.fit_transform([data])
    names = countVectorizer.get_feature_names()

    df = pd.DataFrame(list(names), columns=['names'])
    df = df.assign(Word_Count=wordCount.T.todense())
    df = df.assign(TF_IDF=TfIdf.T.todense())
    df = df.sort_values('TF_IDF', ascending=False)
    print(df)

def BERT_Summarizer(ttext):
    # https: // github.com / dmmiller612 / bert - extractive - summarizer
    # pip install bert-extractive-summarizer
    # pip install ...etc
    # model = Summarizer()
    # result = model(ttext, min_length=1)
    # full = ''.join(result)
    # return full
    from summarizer import Summarizer
    body = ttext
    model = Summarizer()
    # result = model(body, ratio=0.2)  # Specified with ratio
    result = model(body, num_sentences=1)  # Will return 3 sentences 
    return result


# def TextRank_Summarizer(ttext):
#     # pip install gensim
#     return summarize(str(ttext))


def Rake_Summarizer(ttext):
    r = Rake(language="russian")
    r.extract_keywords_from_text(ttext)
    mas = r.get_ranked_phrases()
    set2 = set()
    for item in mas:
        if not "nan" in str(item).replace(" nan ", " "):
            set2.add(str(item).replace(" nan ", " "))
    mas = list(set2)
    return str(mas)

def YakeSummarizer(ttext):
    # !pip install yake
    extractor = yake.KeywordExtractor (
        lan = "ru",     # язык
        n = 3,          # максимальное количество слов в фразе
        dedupLim = 0.3, # порог похожести слов
        top = 1        # количество ключевых слов
    )
    l = list(extractor.extract_keywords(ttext))
    return l[0][0]
 

if __name__ == '__main__':
    data = "«Два самых важных дня в твоей жизни: день, когда ты появился на свет, и день, когда ты понял зачем!». — Марк Твен"
    t = remove_all(data)
    print(t)
    t = Rake_Summarizer(data)
    print(t)    
    t = BERT_Summarizer(data)
    print(t)
    t = YakeSummarizer(data)
    print(t)

