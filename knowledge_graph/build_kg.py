import pandas as pd
import queries as q


class BuildKG:
    def __init__(self, films):
        self.films = films

    def build(self):
        df_film = pd.DataFrame(self.films, columns=['films'])
        df_film['uri'] = df_film['films'].map(lambda x: q.uri(x))
        df_film['directors'], df_film['starring'], df_film['distributor'], df_film['editing'],\
            df_film['musiccomposer'], df_film['producer'] = zip(*df_film['uri'].map((lambda x: q.infos(x))))
        return df_film


if __name__ == '__main__':
    lista = ['The Matrix', 'Toy Story', 'Last Dance', 'Grease']
    kg = BuildKG(lista)
    df = kg.build()
    print(df)

