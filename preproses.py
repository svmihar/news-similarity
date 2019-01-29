import similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd 

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ---Preprocess 
kompas=pd.read_csv(r'./csv/kompas.csv')
kompas_content = kompas['content'].values
print(f'length of kompas\' document: {len(kompas_content)}')
kompas_judul = kompas['title'].values

bisnis = pd.read_csv(r'./csv/bisnis.csv')
bisnis_content = bisnis['content'].values
bisnis_judul=bisnis['title'].values
 
kontan = pd.read_csv(r'./csv/kontan.csv')
kontan_content = kontan['content'].values
kontan_judul=kontan['title'].values

def stemisasi(str):
    return stemmer.stem(str)

kumpulan_berita = [kompas,bisnis,kontan]
# for berita in kumpulan_berita:
#     print(berita['content'].notnull())
#     berita.dropna(inplace=True)
#     berita['judul_stem'] = [stemisasi(kata) for kata in berita['title'].values]
#     berita['content_stem'] = [stemisasi(kata) for kata in berita['content'].values]
#     print(berita)
# def ke_csv(dataframe,name='test.csv'):
#     dataframe.to_csv(name)

# for index, item in enumerate(kumpulan_berita):
#     ke_csv(item,name='csvke{}.csv'.format(index))


"""NGRAM METHOD [BERHASIL]  """

from similarity.ngram import NGram
jum_gram = 2
batas = 0.5 #threshold
gram = NGram(jum_gram)

for index_kompas, judul_kompas in enumerate(kontan_judul):
    for index_bisnis,judul_bisnis in enumerate(bisnis_judul): 
        jarak = gram.distance(stemmer.stem(judul_kompas),stemmer.stem(judul_bisnis))
        if batas>jarak:
            # print(judul)
            print(f'jarak antar berita dengan judul \'{judul_kompas}\' dengan berita di bisnis dengan judul \'{judul_bisnis}\' adalah: \n{jarak}')
