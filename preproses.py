import similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd 
from pandas import ExcelWriter
from pandas import ExcelFile

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

 
df = pd.read_excel('dataframe.xlsx')
# print(df.columns)
isi = df['content'].values
judul = df['title'].values

hasil_isi = []
hasil_judul = []


for berita,titel in zip(isi,judul):
    # hasil_isi.append(stemmer.stem(berita))
    try:
        x = stemmer.stem(berita)
        y = stemmer.stem(titel)
        hasil_judul.append(y)
        hasil_isi.append(x)
        print(f'stemming \n{titel} to \n{y}')
        print(f'stemming \n{berita} to \n{x}')
    except: 
        print('gagal')

df['titel_stem'] = hasil_judul
df['content_stem'] = hasil_isi

df.to_excel('dataframe_preprocessed.xlsx')



# NGRAM METHOD BERHASIL
# from similarity.ngram import NGram
""" from similarity.ngram import NGram
jum_gram = 2
batas = 0.5 #threshold
gram = NGram(jum_gram)

for index_kompas, judul_kompas in enumerate(kompas_judul):
    for index_bisnis,judul_bisnis in enumerate(kontan_judul): 
        jarak = gram.distance(judul_kompas,judul_bisnis)
        if batas>jarak:
            # print(judul)
            print(f'jarak antar berita dengan judul \'{judul_kompas}\' dengan berita di bisnis dengan judul \'{judul_bisnis}\' adalah: \n{jarak}')
 """