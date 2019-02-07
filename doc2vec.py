import pandas as pd 


df = pd.read_excel('dataframe_preprocessed.xlsx')
# print(df.head)

isi=df['content_stem'].values
# print(isi)
with open('stopwords-id.txt') as f: 
    list_stopword = f.readlines()
list_stopword = [x.strip() for x in list_stopword]


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = CountVectorizer(stop_words=list_stopword)
features = vectorizer.fit_transform(isi).todense()
print(vectorizer.vocabulary_)
