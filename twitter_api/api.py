import requests
import json
import pickle


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

    def delete_rules(self, ids):
        payload = self.payload.copy()
        payload["delete"] = {}
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

    def _build_rule(self):
        with open(self.path, 'rb') as f:
            loaded_dict = pickle.load(f)
        elements = []
        for k, v in loaded_dict.items():
            temp = []
            temp.append(k)
            # elements.append(k)
            for n, m in v.items():
                if n != 'uri':
                    temp.extend(m)
                    # elements.extend(m)
            elements.append(temp)
        rules = []
        for element in elements:
            rule = '('
            for entity in element:
                base = f"entity:{entity}"
                rule = rule + base + ' OR '
            rule = rule[:-4] + ') lang:en'
            rules.append(rule)
        return rules








if __name__ == '__main__':
    api = Twitter_APIs('../data/kg_dictionary.pkl')
    api.see_rules()
    # api.delete_rules(["1596191955171655683"])
    # api.add_rule()
