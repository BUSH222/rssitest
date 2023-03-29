import json, requests

a = requests.post("http://127.0.0.1:5000/analyse", data=json.dumps({"78:72:5d:ca:dd:f7": "-72", "78:72:5d:ca:dd:f3": "-75", "78:72:5d:ca:dd:f2": "-73", "78:72:5d:ca:dd:f0": "-74", "24:a4:3c:7d:fc:fc": "-51", "24:a4:3c:7d:f8:59": "-65", "78:72:5d:ca:dd:ff": "-78", "78:72:5d:ca:dd:fc": "-79", "78:72:5d:ca:dd:fd": "-78", "NUM": "2", "24:a4:3c:04:25:31": "-77", "BRUH":"-293"}))
print(a.content)