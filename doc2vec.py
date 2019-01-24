from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd 

data = pd.read_csv("csvke0.csv",index_col=0)
content = list(data['content_stem'].values)
print(type(content))
tagged_data = [TaggedDocument(words=word_tokenize(item.lower()), tags =[str(i)]) for i, item in enumerate(content)]

# max_epoch = 100
# vec_Size = 200
# alpha = 0.025
# print('this is the tagged data: ',tagged_data)
# model = Doc2Vec(size=vec_Size,alpha=alpha, min_alpha=0.00025, min_count = 1, dm=1)
# model.build_vocab(tagged_data)
# for epoch in range(max_epoch):
#     print(f'iteration {epoch}')
#     model.train(tagged_data,total_examples=model.corpus_count, epochs=model.iter)

#     #decrease learning rate 
#     model.alpha-=0.00002
#     #fix learning rate so no decay 
#     model.min_alpha=model.alpha
# model.save("testd2v.mode")
# print('done')

model= Doc2Vec.load("testd2v.model")
print(model.docvecs.count)
print(model.most_similar('kompas'))