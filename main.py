import cleaning as c
from lemming import lemmatizer
import roberta
import requests
import ast
import pickle


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
    model, tokenizer = roberta.load_roberta()
    url = "https://api.twitter.com/2/tweets/search/stream"
    payload = {}
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAA66iwEAAAAAbZtdwOgdYQCUNzPRVopb%2F15CnjQ%3D5iGK97uwYF461cOrCaNZ2tQqAHAHVLVeGBkvcsofaa4TSDKLtm',
        'Content-Type': 'application/json',
        'Cookie': 'guest_id=v1%3A166921382095182903'
    }
    with open('data/kg_dictionary.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)
    # response = requests.request("GET", url, headers=headers, data=payload)
    with requests.get(url, headers=headers, data=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                print(line)
                line = ast.literal_eval(line.decode('utf-8'))
                text = line['data']['text']
                matching_rule = line['matching_rules'][0]['id']
                text = processing_text(text)
                cl = roberta.classify(text, model, tokenizer)
                for k, v in loaded_dict.items():
                    if matching_rule in v['rule']:
                        v['positive'] = v['positive'] + cl['Positive']
                        v['negative'] = v['negative'] + cl['Negative']
                        v['neutral'] = v['neutral'] + cl['Neutral']
                with open('../data/kg_dictionary.pkl', 'wb') as f:
                    pickle.dump(loaded_dict, f)





