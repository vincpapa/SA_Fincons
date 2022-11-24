import cleaning as c
from lemming import lemmatizer
import roberta as r


def processing_text(text):
    text = c.emoji(text)
    text = c.remove_users(text)
    text = c.remove_links(text)
    text = c.clean_html(text)
    text = c.non_ascii(text)
    text = c.lower(text)
    text = c.email_address(text)
    text = c.punct(text)
    # text = c.removeStopWords(text)
    text = c.remove(text)
    text = lemmatizer(text)
    return text


if __name__ == '__main__':
    model, tokenizer = r.load_roberta()
    #
    tweet = 'ZOMBIE CONTRO ZOMBIE (2017) di Shinichiro Ueda, da ieri su #MUBI, è un film da vedere assolutamente. Geniale nella sua costruzione, i primi 40 minuti sono un lunghissimo piano sequenza, dopo il quale partono i titoli di coda. Finito direte? Macché, è solo l inizio.'
    tweet = processing_text(tweet)
    cl = r.classify(tweet, model, tokenizer)
    print(cl)




