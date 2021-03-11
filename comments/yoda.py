import json
import urllib.parse
import urllib.request
import time

def talk(text):
    str = urllib.parse.quote(text)
    attempts = 0
    while attempts < 2:
        try:
            attempts += 1
            with urllib.request.urlopen('http://yoda-api.appspot.com/api/v1/yodish?text=' + str) as response:
                json_content = response.read()
                phrase = json.loads(json_content)['yodish']
                return phrase
        except Exception as e:
            print(e)
            print("for comment: "+str)
            time.sleep(5)
    return False

if __name__ == "__main__":
    print(talk("I Love movies, so what"))