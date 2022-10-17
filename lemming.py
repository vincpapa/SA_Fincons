import spacy

# prova
def lemmatizer(text):
    """Applying lemmitizer to text"""
    nlp = spacy.load("en_core_web_sm")
    sentence = nlp(text)
    new_sentence = ''
    for token in sentence:
        new_sentence = new_sentence + ' ' + token.lemma_
    return new_sentence
