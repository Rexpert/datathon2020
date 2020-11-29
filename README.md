# datathon2020
This repository storing all the works for data analysis in the DOSM Virtual Datathon 2020

Outsourcing Process:
1. [share.py](https://github.com/Rexpert/datathon2020/blob/main/share.py), requirement:
   - python 3.x
   - [miniconda](https://docs.conda.io/en/latest/miniconda.html)
   - [googletrans 3.0.0](https://pypi.org/project/googletrans/)
2. [NLP.ipynb](https://colab.research.google.com/drive/1e8F8YUH3f4-7rpJ8Xk__cUIjXfpJH1yD), requirement:
   - python 3.x
   - [token_list](https://github.com/Rexpert/datathon2020/blob/main/output/colab/token_list.pkl) in your google drive
   - [pandas 1.1.4](https://pandas.pydata.org/docs/)*
   - [spacy 2.3.2](https://spacy.io/)*
   - [scikit-learn 0.23.2](https://scikit-learn.org/stable/)*  
   (* pre-installed in google colab library)

Reason to outsource:
1. [share.py](https://github.com/Rexpert/datathon2020/blob/main/share.py):
   - googletrans was too slow to process the language detection
   - strategy: split the job into several parts and execute on different pc to prevent being block by IP
   
2. [NLP.ipynb](https://colab.research.google.com/drive/1e8F8YUH3f4-7rpJ8Xk__cUIjXfpJH1yD):
   - sklearn's tfidfvectorizer need atleast 10 GB RAM to process the large dataframe
   - Slow process to run the loop, requires faster cpu (higher frequency cpu) to run the process
   - Strategy: import the code into [Google Colab](https://colab.research.google.com/), which offer free 12GB RAM & Faster CPU & GPU
