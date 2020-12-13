import re
import os
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

TEST = False
data_path = r'data/Price Intelligence/'
output_path = r'output/'
wd = r'D:\UNIVERSITY UTARA MALAYSIA\Datathon 2020 - Documents\datathon2020'
os.chdir(wd)

keyword_path = os.path.join(output_path, 'colab', 'keywords.csv')
en_path = [os.path.exists(os.path.join(
    output_path, 'wip_output', 'en_{}.txt'.format(i))) for i in range(10)]

if not os.path.exists(keyword_path):
    if not all(en_path):
        rx_csv = re.compile(r'.*\.csv$')

        filenames = os.listdir(data_path)
        filenames = [os.path.join(wd, data_path, name)
                     for name in filenames if rx_csv.match(name)]
        pi_all = pd.DataFrame()

        for file in filenames:
            pi = pd.read_csv(file)
            if TEST:
                if file == filenames[0]:
                    pi_all = pi.iloc[:1000, [2, 4]]
                    break
            else:
                # Concatenate all files HERE
                pi_all = pi_all.append(pi.iloc[:, [2, 4]])
        rx_cat = re.compile(r'.*/{}/.*'.format(r'mother & baby'))
        titles = pi_all.loc[pi_all.item_category_detail.str.contains(
            rx_cat), 'title']

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        # Devide into 10 Tasks
        lst = list(chunks(titles.to_list(), 20800))
        for i, l in enumerate(lst):
            with open(os.path.join(output_path, 'wip', '{}.txt'.format(i)), 'w+', encoding='utf-8') as f:
                for s in l:
                    f.write(s + '\n')
        # Run share.py
        os.system('python share.py')
    else:
        # # -----------------------------------------------
        # # Copy the en_0.txt - en_9.txt to gdrive
        # # Run these commented codes in Google Colab
        # # https://colab.research.google.com/drive/1e8F8YUH3f4-7rpJ8Xk__cUIjXfpJH1yD?usp=sharing
        # # -----------------------------------------------
        # import re
        # import os
        # import pandas as pd
        # import spacy
        # from google.colab import drive
        # from google.colab import files
        # from sklearn.feature_extraction.text import TfidfVectorizer
        # drive.mount("/content/gdrive")

        # output_path = '/content/gdrive/My Drive/datathon 2020/output'
        # en = []
        # other = []
        # for i in range(10):
        #     with open(os.path.join(output_path, 'wip_output', 'en_{}.txt'.format(i)), 'r+', encoding='utf-8') as f:
        #         en.extend([line.rstrip('\n') for line in f])
        #     with open(os.path.join(output_path, 'wip_output', 'other_{}.txt'.format(i)), 'r+', encoding='utf-8') as f:
        #         other.extend([line.rstrip('\n') for line in f])

        # def get_token_list(title, i=-1):
        #     '''
        #     Filter:
        #     1. Not Stop word
        #     2. only atleast 3 alphabets above
        #     '''
        #     print(i) if i != -1 else None
        #     doc = nlp(title)
        #     token_list = []
        #     rx_alpha = re.compile(r'^[a-zA-Z]{3,}$')
        #     for token in doc:
        #         lexeme = nlp.vocab[token.text]
        #         conditions = not lexeme.is_stop and \
        #             rx_alpha.match(token.text)
        #         if conditions:
        #             # lemmatization
        #             token_list.append(token.lemma_)
        #     return token_list

        # nlp = spacy.load('en_core_web_sm')
        # token_list = [get_token_list(title, i) for i, title in enumerate(en)]
        # del en

        # tfidf = TfidfVectorizer(analyzer=lambda x:[w for w in x])
        # tfidf_vectors = tfidf.fit_transform(token_list)
        # vc = tfidf_vectors.todense()
        # del token_list

        # s = vc.sum(axis=0)
        # voc = tfidf.vocabulary_
        # keywords = pd.DataFrame(s, columns=voc).transpose()
        # keywords.columns = ['sum_tfidf']

        # keywords.to_csv('keywords.csv')
        # files.download('keywords.csv')
        print('Run Google Colab to obtain keywords.csv')
else:
    # Read output from Google Colab
    keywords = pd.read_csv(os.path.join(output_path, 'colab', 'keywords.csv'))

    # Cleaning Data Frame
    keywords.columns = ['keyword', 'sum_tfidf']
    keywords_list = keywords.apply(lambda r: (
        r.keyword, round(r.sum_tfidf, 2)), axis=1).to_list()

    c = (
        WordCloud()
        .add("", keywords_list, word_size_range=[20, 100], shape=SymbolType.ARROW)
        .set_global_opts(title_opts=opts.TitleOpts(title='Keywords for Mother & Baby category'))
        .render(os.path.join(output_path, 'html_files', 'wordcloud.html'))
    )
