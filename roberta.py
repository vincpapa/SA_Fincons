from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax


def load_roberta():
    # prova
    # LINK DI RIFERIMENTO:
    # https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base
    # roberta = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    # tokenizer.save_pretrained("roberta/twitter-xlm-roberta-base-sentiment")
    # model.save_pretrained("roberta/twitter-xlm-roberta-base-sentiment")
    roberta = "roberta/twitter-xlm-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    return model, tokenizer


def classify(text, model, tokenizer):
    labels = ['Negative', 'Neutral', 'Positive']
    diz = {}
    encoded_tweet = tokenizer(text, return_tensors='pt')
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    for i in range(len(scores)):
        diz[labels[i]] = scores[i]
        # l = labels[i]
        # s = scores[i]
    return diz
