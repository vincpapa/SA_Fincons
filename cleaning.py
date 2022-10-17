from emot.emo_unicode import UNICODE_EMOJI
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('stopwords')
# prova

def emoji(text):
    """Translation of emoji"""
    for emot in UNICODE_EMOJI:
        if text is None:
            text = text
    else:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()))
    return text


def remove_users(text):
    """Takes a string and removes retweet and @user information"""
    text = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', text)
    # remove tweeted at
    return text


def remove_links(text):
    """Takes a string and removes web links from it"""
    text = re.sub(r'http\S+', '', text)  # remove http links
    text = re.sub(r'bit.ly/\S+', '', text) # remove bitly links
    text = text.strip('[link]')  # remove [links]
    return text


def clean_html(text):
    """Takes a string and removes html"""
    html = re.compile('<.*?>')  # regex
    return html.sub(r'', text)


def non_ascii(text):
    """Takes a string and remove non ascii characters"""
    return "".join(i for i in text if ord(i) < 128)


def lower(text):
    """Lower case of a string"""
    return text.lower()


def email_address(text):
    """Takes a string and remove email address"""
    email = re.compile(r'[\w\.-]+@[\w\.-]+')
    return email.sub(r'', text)


def punct(text):
    """Takes a string and remove punctuation"""
    token = RegexpTokenizer(r'\w+')  # regex
    text = token.tokenize(text)
    text = " ".join(text)
    return text


# remove stopwords
def removeStopWords(text):
    """Takes a string and remove stop words"""
    # select english stopwords
    cachedStopWords = set(stopwords.words("english"))  # https://wellsr.com/python/remove-stop-words-with-python-nltk/
    # add custom words
    # cachedStopWords.update(('and','I','A','http','And','So','arnt','This','When','It','many','Many','so','cant','Yes','yes','No','no','These','these','mailto','regards','ayanna','like','email'))
    # remove stop words
    new_str = ' '.join([word for word in text.split() if word not in cachedStopWords])
    return new_str


def remove(text):
    """Takes a string and remove special characters"""
    text = re.sub('([_]+)', "", text)
    return text
