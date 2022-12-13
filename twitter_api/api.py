import requests
import json
import pickle
import ast

class Twitter_APIs:
    def __init__(self, path):
        self.endpoint_stream = "https://api.twitter.com/2/tweets/search/stream"
        self.endpoint_rules = "https://api.twitter.com/2/tweets/search/stream/rules"
        self.header = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAA66iwEAAAAAbZtdwOgdYQCUNzPRVopb%2F15CnjQ%3D5iGK97uwYF461cOrCaNZ2tQqAHAHVLVeGBkvcsofaa4TSDKLtm',
            'Cookie': 'guest_id=v1%3A166936720752585669'
        }
        self.payload = {}
        self.path = path

    def see_rules(self):
        response = requests.request("GET", self.endpoint_rules, headers=self.header, data=self.payload)
        print(response.text)
        return response.json()

    def delete_rules(self, flag=True, ids=None):
        payload = self.payload.copy()
        payload["delete"] = {}
        if flag:
            response = self.see_rules()
            ids = []
            for el in response['data']:
                ids.append(el['id'])
        payload["delete"]["ids"] = ids
        header = self.header.copy()
        header["Content-Type"] = 'application/json'
        response = requests.request("POST", self.endpoint_rules, headers=header, data=json.dumps(payload))
        print(response.text)

    def add_rule(self):
        rules = self._build_rule()
        payload = self.payload.copy()
        payload["add"] = []
        for rule in rules:
            payload["add"].append({"value": rule})
        header = self.header.copy()
        header["Content-Type"] = 'application/json'
        response = requests.request("POST", self.endpoint_rules, headers=header, data=json.dumps(payload))
        print(response.text)
        with open(self.path, 'rb') as f:
            loaded_dict = pickle.load(f)
        for k, v in loaded_dict.items():
            v['rule'] = []
        for el in response.json()['data']:
            entities = ast.literal_eval(
                el['value'].replace('entity:', '').replace(' lang:en', '').replace(' OR ', '", "').replace('(',
                                                                                                           '["').replace(
                    ')', '"]'))
            for k, v in loaded_dict.items():
                temp = []
                temp.append(k)
                for n, m in v.items():
                    if n != 'uri' and n != 'positive' and n != 'negative' and n != 'neutral' and n != 'rule':
                        temp.extend(m)
                for entity in entities:
                    if entity in temp:
                        if el['id'] not in v['rule']:
                            v['rule'].append(el['id'])
        with open('../data/kg_dictionary.pkl', 'wb') as f:
            pickle.dump(loaded_dict, f)


    def _build_rule(self):
        with open(self.path, 'rb') as f:
            loaded_dict = pickle.load(f)
        elements = []
        for k, v in loaded_dict.items():
            temp = []
            temp.append(k)
            # elements.append(k)
            for n, m in v.items():
                if n != 'uri' and n!= 'positive' and n!= 'negative' and n!= 'neutral' and n!= 'rule':
                    temp.extend(m)
                    # elements.extend(m)
            elements.append(temp)
        flat_elements = [item for sublist in elements for item in sublist]
        flat_elements = list(set(flat_elements))
        rules = []
        rule = '() lang:en'
        flag = True
        for element in flat_elements:
            if flag:
                base = f"entity:{element}"
                flag = False
            else:
                base = f" OR entity:{element}"
            if len(rule[:-9] + base + rule[-9:]) <= 512:
                rule = rule[:-9] + base + rule[-9:]
            else:
                rules.append(rule)
                rule = '() lang:en'
                flag = True
        '''
        for element in elements:
            rule = '('
            for entity in element:
                base = f"entity:{entity}"
                rule = rule + base + ' OR '
            rule = rule[:-4] + ') lang:en'
            rules.append(rule)
        '''
        return rules


if __name__ == '__main__':
    api = Twitter_APIs('../data/kg_dictionary.pkl')
    # api.see_rules()
    # api.delete_rules()
    # api.see_rules()
    api.add_rule()
    # api.see_rules()

