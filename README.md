# datathon2020
This repository storing all the works for data analysis in the DOSM Virtual Datathon 2020

## Dataset
The dataset was provided by DOSM (Department of Statistics Malaysia). The raw data is a collection of 7 `.csv` files, which contained the records of online sales in some e-commerce platforms in the second half-year of 2019. The raw data consist of 10 columns, which specified in the metadata:

No.   | Variable name         | Description
------|-----------------------|------------------------------------------------------------------------------------------
1     | dates                 | Refer to date of the data crawled
2     | month                 | Refer to month of the data
3     | item_category_detail  | Refer to the detail of the product category, from main category until the lowest category
4     | item_category         | Refer to the item category for the product
5     | title                 | Refer to the title of the product in the online platform
6     | description           | Refer to the detail description of the product
7     | price_ori             | Refer to the original price of the product as per date crawled
8     | price_actual          | Refer to the actual price to be paid (include discounted price) for the product as per date crawled
9     | sellerID              | Refer to the seller name/company
10    | seller_rating         | Refer to the rating of the seller  

The usage of this dataset is specifically for Datathon only. As we agreed in the term and conditions, this dataset will not be shared in any form (including the GitHub Repository) and will be removed in the local at the end of this Datathon.

## Objective & Result
This project aimed to build an [interactive dashboard](https://rexpert.shinyapps.io/datathon2020/) that helps to provide information about the current market trend in the online shopping platform. Based on the most popular products, we found their optimal discount rate and the most suitable price, also retrieved the most important keywords in the product titles. 

## Deployment
If you are interested to run the scripts, you'll need to `git clone` this repository:
```
git clone https://github.com/Rexpert/datathon2020.git
```
Please install the required packages via `conda` accordingly:
```
cd datathon2020
conda env create --file environment.yml
```

## Outsourcing
However, due to the limitation of my PC's hardware, I've outsourced several jobs to the external environment:
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
   - strategy: split the job into several parts and execute parallelly on different PCs (although I've realized it could run parallelly in the same PC with multiple Python instance processes)
   
2. [NLP.ipynb](https://colab.research.google.com/drive/1e8F8YUH3f4-7rpJ8Xk__cUIjXfpJH1yD):
   - sklearn's tfidfvectorizer need atleast 10 GB RAM to process the large dataframe
   - Slow process to run the iterations, which requires faster cpu (higher frequency cpu) to run the process in a shorter duration.
   - Strategy: import and run the code in [Google Colab](https://colab.research.google.com/), which offer free 12GB RAM and Faster CPU & GPU

## License
GNU GPL-V3 © 2020 KL<sup>2</sup> 