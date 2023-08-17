import requests
import time
import random
import hashlib
import json
import sys

key, secret = "", ""
with open("secret", "r") as f:
    key, secret = f.read().split()

class Asker:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def ask_method(self, method: str, params={}):
    
        params_arr = []
        for key in params.keys():
            params_arr += [(key, params[key])]
        params_arr.append(("apiKey", self.key))
        params_arr.append(("time", str(int(time.time()))))
        params_arr.sort()
        
        apiSig = str(random.randint(10**5, 10**6 - 1))
        h = apiSig + '/' + method + '?'
        for param in params_arr:
            h += param[0] + '=' + str(param[1]) + '&'
        h = h[:-1]
        h += '#' + self.secret
    
        params_arr = []
        for key in params.keys():
            params_arr += [(key, params[key])]
        params_arr.append(("apiKey", self.key))
        params_arr.append(("time", str(int(time.time()))))
        params_arr.append(("apiSig", apiSig))

        par = "?"
        for param in params_arr:
            par += param[0] + '=' + str(param[1]) + '&'
        par = par[:-1]
        
        h = hashlib.sha512(str.encode(h)).hexdigest()
        req = 'http://codeforces.com/api/{}{}{}'.format(method, par, h)
        return requests.get(req)

    def get_submits(self, handle: str):
        result = json.loads(self.ask_method("user.status", {"handle": "Leha123"}).text)
        print(result['status'])
        return result["result"]

    def get_tasks(self, handles: list):
        probs = []
        for handle in handles:
            time.sleep(3)
            subs = self.get_submits(handle)
            for sub in subs:
                probs += [(sub["contestId"], sub["problem"]["index"])]
        probs = list(set(probs))
        
        return probs

    def generate_css(self, tasks: list, name: str, background_color="#f40afc73"):
        with open(name, "w") as f:
            for t in tasks:
                f.write('a[href*="{}"]'.format(str(t[0]) + '/' + str(t[1])))
                f.write('{')
                f.write("background-color: {};".format(background_color))
                f.write('}')


if __name__ == "__main__":
    accounts = ["Lehatr", "you_will_never_know", "Leha123", "MichaelKab", "ulianaeskova", "Androsov",
                            "mihaikn", "Dmitriy040155", "Pavtiger", "mashapervak"]
    if len(sys.argv) != 1:
        accounts = sys.argv[1:]
    
    print(accounts)
    asker = Asker(key, secret)
    tasks = asker.get_tasks()
    asker.generate_css(tasks, "extension/marker.css")
