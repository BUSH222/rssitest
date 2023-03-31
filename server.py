from flask import Flask, request, redirect
import json, os
app = Flask(__name__)

fundata = {}

def checksavedposs(threshold=-80):
    orfile = open('savedposs.txt', 'r').readlines()
    tempc = []
    for i, s in enumerate(orfile):
        g = json.loads(s)
        tempc.append(dict())
        for key, value in g.items():
            if key in ['NUM', 'FNAME']:
                tempc[i][key] = value
            elif int(value) > threshold:
                tempc[i][key] = value
    print(tempc)
    tempc = list(filter(lambda x: len(x) > 2, tempc))

    with open('savedposs.txt', 'w') as file1:
        for k in tempc:
            print(json.dumps(k), file=file1)




@app.route('/testdata', methods=['GET', 'POST'])
def testdata():
    global fundata
    fundata = json.loads(request.data)
    with open('savedposs.txt', 'a') as funfile:
        print(json.dumps(fundata), file=funfile)
    return 'received'
    
@app.route('/downloadapk')
def downloadFile():
    return redirect("https://github.com/BUSH222/Audioloc/releases/tag/v0.1", code=302)

@app.route('/analyse', methods=['POST']) #10.0.2.2:22222
def analyse():
    global fundata

    res_out = {}
    with open('savedposs.txt', 'r') as funfile2:
        for s in funfile2.readlines():
            if len(s) != 0:
                a = json.loads(s.strip())
                assert 'NUM' in a.keys()
                assert 'FNAME' in a.keys()
                number = a['NUM']
                filename = a['FNAME']
                res_out[number] = filename
                a.pop('FNAME')
                a.pop('NUM')
                fundata[number] = a
    
    comp_to = json.loads(request.data)

    probs = dict(zip(fundata, len(fundata)*[0])) #magic, no clue how any of this works
    for num, d in fundata.items():
        for b, r in d.items():
            if b in comp_to.keys():
                er = abs(abs(int(r))-abs(int(comp_to[b])))
                if er < 10:
                    probs[num] += 100/len(d)*(1-er/10)
    maxv = sorted(probs.items(), key=lambda x: x[1], reverse=True)[0]

    return res_out[maxv[0]]



@app.route('/')
def index():
  return "<html><body><h1>Welcome. Website is running.</h1></body></html>"


if __name__ == "__main__":
    checksavedposs()
    print('Check complete')
    app.run(host='0.0.0.0', port=22222)