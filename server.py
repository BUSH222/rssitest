from flask import Flask, request, redirect, send_from_directory, render_template
import json
import os
app = Flask(__name__)


def check_saved_poss(threshold=-80):
    orfile = json.load(open('savedposs.json'))
    tempc = []

    for i, s in enumerate(orfile):
        tempc.append(dict())
        for key, value in s.items():
            if key in ['NUM', 'FNAME']:
                tempc[i][key] = value
            elif int(value) > threshold:
                tempc[i][key] = value

    tempc = list(filter(lambda x: len(x) > 2, tempc))
    tempc = [{key:d[key] for key in sorted(d.keys(), key=len)} for d in tempc]

    with open('savedposs.json', 'w') as f:
        json.dump(tempc, f, ensure_ascii=False, indent=4)


@app.route('/testdata', methods=['GET', 'POST'])
def test_data():
    data = json.loads(request.data)
    todump = json.load(open('savedposs.json')).append(data)
    with open('savedposs.json', 'w') as f:
        json.dump(todump, f, ensure_ascii=False, indent=4)
    return 'received'


@app.route('/downloadapk')
def download_file():
    return redirect("https://github.com/BUSH222/Audioloc/releases/latest", code=302)


@app.route('/mobileinfo')
def mobile_info():
    return render_template('instructions.html')


@app.route('/analyse', methods=['POST'])  # 10.0.2.2:22222
def analyse():
    data = {}

    res_out = {}
    with open('savedposs.json') as f:
        poss = json.load(f)
        for s in poss:
            if len(s) != 0:
                a = json.loads(s.strip())
                assert 'NUM' in a.keys()
                assert 'FNAME' in a.keys()
                number = a['NUM']
                filename = a['FNAME']
                res_out[number] = filename
                a.pop('FNAME')
                a.pop('NUM')
                data[number] = a

    comp_to = json.loads(request.data)

    # magic, no clue how any of this works
    probs = dict(zip(data, len(data)*[0]))
    for num, d in data.items():
        for b, r in d.items():
            if b in comp_to.keys():
                er = abs(abs(int(r))-abs(int(comp_to[b])))
                if er < 10:
                    probs[num] += 100/len(d)*(1-er/10)
    maxv = sorted(probs.items(), key=lambda x: x[1], reverse=True)[0]

    return res_out[maxv[0]]

@app.route('/getaudio/<fname>', methods=['GET'])
def get_audio(fname):
    audio_folder = 'audiofiles'
    if fname and os.path.exists(os.path.join(audio_folder, fname)):
        return send_from_directory(audio_folder, fname)
    else:
        return send_from_directory(audio_folder, 'nothing.mp3')

@app.route('/')
def index():
    return render_template('homepage.html')


if __name__ == "__main__":
    check_saved_poss()
    app.run(host='0.0.0.0', port=22222)
