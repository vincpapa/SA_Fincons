import pandas as pd
import queries as q
import pickle
import numpy as np


class BuildKG:
    def __init__(self, films):
        self.films = films

    def build(self):
        df_film = pd.DataFrame(self.films, columns=['films'])
        df_film['uri'] = df_film['films'].map(lambda x: q.uri(x))
        df_film['directors'], df_film['starring'], df_film['distributor'], df_film['editing'],\
            df_film['musiccomposer'], df_film['producer'] = zip(*df_film['uri'].map((lambda x: q.infos(x))))
        df_film['rule'] = np.full((df_film.shape[0]), '')
        df_film['positive'] = np.full((df_film.shape[0]), 0)
        df_film['neutral'] = np.full((df_film.shape[0]), 0)
        df_film['negative'] = np.full((df_film.shape[0]), 0)
        df_film.set_index('films', inplace=True)
        df_dict = df_film.to_dict('index')
        return df_dict


if __name__ == '__main__':
    lista = ['The Matrix', 'Toy Story', 'Last Dance', 'Grease']
    kg = BuildKG(lista)
    df_dict = kg.build()
    # df.to_csv('../data/kg.tsv', sep='\t', index=False)
    with open('../data/kg_dictionary.pkl', 'wb') as f:
        pickle.dump(df_dict, f)

