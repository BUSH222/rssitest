from flask import Flask, request, send_file
import json, os
app = Flask(__name__)

fundata = {}
def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

@app.route('/testdata', methods=['GET', 'POST'])
def testdata():
    global fundata
    fundata = json.loads(request.data)
    with open('savedposs.txt', 'a') as funfile:
        print(json.dumps(fundata), file=funfile)
    return 'received'

@app.route('/receive', methods=['GET'])
def receive():
    with open('savedposs.txt', 'r') as funfile:
        return funfile.read()
    
@app.route('/downloadapk')
def downloadFile ():
    path = os.getcwd() + "/Audioloc.apk"
    return send_file(path, as_attachment=True)

@app.route('/analyse', methods=['POST']) #10.0.2.2:22222
def analyse():
    global fundata
    with open('savedposs.txt', 'r') as funfile2:
        for s in funfile2.readlines():
            if len(s) != 0:
                a = json.loads(s.strip())
                number = a['NUM']
                a.pop('NUM')
                fundata[number] = a
    comp_to = json.loads(request.data)

    res_out = {"1":"venera.mp3", "2":"monalisa.mp3"}

    print(comp_to)

    probs = dict(zip(fundata, len(fundata)*[0]))
    for num, d in fundata.items():
        for b, r in d.items():
            if b in comp_to.keys():
                er = abs(abs(int(r))-abs(int(comp_to[b])))
                if er < 10:
                    probs[num] += 100/len(d)*(1-er/10)
    maxv = sorted(probs.items(), key=lambda x: x[1], reverse=True)[0]
    print(probs)

    return res_out[maxv[0]]



@app.route('/')
def index():
  return "<html><body><h1>Welcome. Website is running.</h1></body></html>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=22222)