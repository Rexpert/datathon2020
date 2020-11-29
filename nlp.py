import re
import os
import spacy
import pickle
import pandas as pd

from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

TEST = False
data_path = r'data/Price Intelligence/'
output_path = r'output/'
wd = r'D:\UNIVERSITY UTARA MALAYSIA\Datathon 2020 - Documents\datathon2020'
en = []
other = []
os.chdir(wd)

# ---------------------------------------------

rx_csv = re.compile(r'.*\.csv$')

filenames = os.listdir(data_path)
filenames = [os.path.join(wd, data_path, name)
             for name in filenames if rx_csv.match(name)]

pi_all = pd.DataFrame()

for file in filenames:
    pi = pd.read_csv(file)
    if TEST:
        if file == filenames[0]:
            pi_all = pi.head(1000).iloc[:, [2, 4]]
            break
    else:
        # Concatenate all files HERE
        pi_all = pi_all.append(pi.iloc[:, [2, 4]])

rx_cat = re.compile(r'.*/{}/.*'.format(r'mother & baby'))
titles = pi_all.loc[pi_all.item_category_detail.str.contains(rx_cat), 'title']

# ------------------------
# split jobs
# ------------------------
# def chunks(lst, n):
#     """Yield successive n-sized chunks from lst."""
#     for i in range(0, len(lst), n):
#         yield lst[i:i + n]


# lst = list(chunks(titles.to_list(), 20800))

# SAVE = True
# for i, l in enumerate(lst):
#     if SAVE:
#         with open(os.path.join(output_path, wip_output, '{}.txt'.format(i)), 'w+', encoding='utf-8') as f:
#             for s in l:
#                 f.write(s + '\n')
# print('done')

limit = len(titles) / 2
counter = 0
translator = Translator()
for i, title in enumerate(titles):
    while True:
        try:
            lang = translator.detect(title).lang
        except:
            print('retrying' + str(i))
            translator = Translator()
            if counter > limit:
                break
            counter += 1
            continue
        break
    if lang == 'en':
        en.append(title)
    else:
        other.append(title)


if TEST:
    with open(os.path.join(output_path, 'nlp_en_list.txt'), 'w+', encoding='utf-8') as f:
        for s in en:
            f.write(s + '\n')
    with open(os.path.join(output_path, 'nlp_other_list.txt'), 'w+', encoding='utf-8') as f:
        for s in other:
            f.write(s + '\n')
else:
    en = []
    other = []
    for i in range(10):
        with open(os.path.join(output_path, 'wip_output', 'en_{}.txt'.format(i)), 'r+', encoding='utf-8') as f:
            en.extend([line.rstrip('\n') for line in f])
        with open(os.path.join(output_path, 'wip_output', 'other_{}.txt'.format(i)), 'r+', encoding='utf-8') as f:
            other.extend([line.rstrip('\n') for line in f])

nlp = spacy.load('en_core_web_sm')


def get_token_list(title, i=-1):
    '''
    Filter:
    1. Not Stop word
    2. only atleast 3 alphabets above
    '''
    print(i) if i != -1 else None
    doc = nlp(title)
    token_list = []
    rx_alpha = re.compile(r'^[a-zA-Z]{3,}$')
    for token in doc:
        lexeme = nlp.vocab[token.text]
        conditions = not lexeme.is_stop and \
            rx_alpha.match(token.text)
        if conditions:
            # lemmatization
            token_list.append(token.lemma_)
    return token_list


token_list = [get_token_list(title, i) for i, title in enumerate(en)]

# tfidf = TfidfVectorizer(analyzer=lambda x:[w for w in x])
# tfidf_vectors = tfidf.fit_transform(token_list)
# pd.DataFrame(tfidf_vectors.todense(), columns=tfidf.vocabulary_).sum(axis=0)

# https://colab.research.google.com/drive/1e8F8YUH3f4-7rpJ8Xk__cUIjXfpJH1yD?usp=sharing
with open(os.path.join(output_path, 'colab', 'token_list.pkl'), 'wb+') as output:
    pickle.dump(token_list, output, pickle.HIGHEST_PROTOCOL)

# ---------------------------------------------------------------------

keywords = pd.read_csv(os.path.join(output_path, 'colab', 'keywords.csv'))
keywords.columns = ['keyword', 'sum_tfidf']

keywords_list = keywords.apply(lambda r: (
    r.keyword, round(r.sum_tfidf, 2)), axis=1).to_list()

c = (
    WordCloud()
    .add("", keywords_list, word_size_range=[20, 100], shape=SymbolType.ARROW)
    .set_global_opts(title_opts=opts.TitleOpts(title='Keywords for Mother & Baby category'))
    .render(os.path.join(output_path, 'html_files', 'wordcloud.html'))
)
