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
import convertQA
from pymystem3 import Mystem

def load_data(filename='data.txt'):
    with open(filename, "r", encoding='utf-8') as file:
        data = file.read()


def data_proc(filename='data.txt'):
    with open(filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    count_messages = len(messages)
    print(count_messages)
    texts=[]
    for m in messages:
        text = m['text']
        texts.append(remove_all_mas(text))
    num = 0
    ltexts = d2lemmatize(texts)
    proc_messages = []
    for m in messages:
        line = {}
        line['date'] = m['date']
        text = m['text']
        line['text'] = text
        line['remove_all']  = texts[num]
        # print(str(texts[num]))
        # print(text)
        line['get_normal_form'] = ltexts[num]
        # line['get_normal_form'] = get_normal_form(remove_all(data))
        # line['Rake_Summarizer'] = Rake_Summarizer(data)
        # line['YakeSummarizer'] = YakeSummarizer(data)
        line['message_id'] = m['message_id']
        line['user_id'] = m['user_id']
        line['reply_message_id'] = m['reply_message_id']
        proc_messages.append(line)
        print(f"{num} / {count_messages}")
        num += 1
    
    jsonstring = json.dumps(proc_messages,ensure_ascii=False)
    # print(jsonstring)
    with open("proc_messages.json", "w", encoding="UTF8") as file:
        file.write(jsonstring)

def d2lemmatize(mas):
    crazdelitel = " cr "
    razdelitel = " br "
    rwords = ""
    row_num = 1;
    # for item in mas:
    #     # print(row_num)
    #     row_num+=1
    #     cwords = ""
    #     for word in item:
    #         if len(str(word)) > 3:
    #             cwords = cwords + str(word) + razdelitel
    #     if len(cwords)>1:
    #         rwords = rwords + cwords + сrazdelitel
    for item1 in mas:
        cwords = ""
        if type(item1) in (tuple, list):
            for item2 in item1:
                cwords = cwords + str(item2) + razdelitel
        else:
            item1 = item1.split()
            for item2 in item1:
                cwords = cwords + str(item2) + razdelitel
        # print(cwords)
        rwords = rwords + cwords + crazdelitel
    m = Mystem()
    # print(rwords)
    lmas = m.lemmatize(rwords)
    gmas = []
    tmpword = ""
    stroka = []
    for word in lmas:
        word = str(word)
        if word == str.strip(razdelitel):
            stroka.append(tmpword)
            tmpword = ""
        elif len(str(word)) > 3:
            tmpword = tmpword + " " + word
        elif word == str.strip(crazdelitel):
            gmas.append(stroka)
            stroka = []
    # print(gmas)
    return gmas


def d1lemmatize(mas):
    gmas = []
    razdelitel = " br "
    m = Mystem()
    lwords = ""
    for word in mas:
        if len(str(word)) > 3:
            lwords = lwords + word + razdelitel
    # print(lwords)
    # print(mas)
    lmas = m.lemmatize(lwords)
    # print(lmas)
    tmpword = []
    for word in lmas:
        if word == str.strip(razdelitel):
            gmas.append(tmpword)
            tmpword = []
        elif len(word) > 3:
            tmpword.append(word)
    # print(gmas)
    return 


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
    data = remove_short_words(data, length=3)
    data = remove_paragraf_to_lower(data)
    return data

def remove_all_mas(data):
    data = remove_digit(data)
    data = remove_punctuation(data)
    data = remove_stopwords(data)
    data = remove_short_words(data, length=3)
    data = remove_paragraf_to_lower(data)
    data = data.split()
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
    from summarizer import Summarizer
    body = ttext
    model = Summarizer()
    # result = model(body, ratio=0.2)  # Specified with ratio
    result = model(body, num_sentences=1)  # Will return 3 sentences
    result = remove_all(result)
    return result


# def TextRank_Summarizer(ttext):
#     # pip install gensim
#     return summarize(str(ttext))


def Rake_Summarizer(ttext):
    # !pip install nlp-rake
    # !pip install nltk
    from nlp_rake import Rake
    # import nltk
    # from nltk.corpus import stopwords
    # nltk.download ("stopwords")
    stops = list(set(stopwords.words("russian")))

    rake = Rake(stopwords=stops, max_words=3)
    return rake.apply(ttext)[:1][0][0]


def YakeSummarizer(ttext):
    # !pip install yake
    extractor = yake.KeywordExtractor(
        lan="ru",     # язык
        n=3,          # максимальное количество слов в фразе
        dedupLim=0.3,  # порог похожести слов
        top=1        # количество ключевых слов
    )
    l = list(extractor.extract_keywords(ttext))
    return l[0][0]


def get_normal_form(words):
    morph = pymorphy2.MorphAnalyzer()
    result = []
    for word in words.split():
        p = morph.parse(word)[0]
        result.append(p.normal_form)
    return result


if __name__ == '__main__':
    data = "«Два самых важных дня в твоей жизни: день, когда ты появился на свет, и день, когда ты понял зачем!». — Марк Твен"
    # t=remove_all_mas(data)
    # print(t)
        
    # t = remove_all(data)
    # print("remove_all")
    # print(t)
    # t = get_normal_form(remove_all(data))
    # print("norm")
    # print(t)
    # t = Rake_Summarizer(data)
    # print("Rake_Summarizer")
    # print(t)
    # # t = BERT_Summarizer(data)
    # # print("BERT_Summarizer")
    # # print(t)
    # t = YakeSummarizer(data)
    # print("YakeSummarizer")
    # print(t)
    data_proc("d:/ml/chat/andromedica.json")