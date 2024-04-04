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
    todump = json.load(open('savedposs.json'))
    todump.append(data)
    with open('savedposs.json', 'w') as f:
        json.dump(todump, f, ensure_ascii=False, indent=4)
    return 'received'


@app.route('/downloadapk')
def download_file():
    return redirect(apk_release_link, code=302)


@app.route('/mobileinfo')
def mobile_info():
    return render_template('instructions.html')


@app.route('/analyse', methods=['POST'])  # 10.0.2.2:22222
def analyse():
    data = {}

    res_out = {}
    with open('savedposs.json') as f:
        poss = json.load(f)
        for a in poss:
            if len(a) != 0:
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
                if er < allowed_error_in_algorithm:
                    probs[num] += 100/len(d)*(1-er/allowed_error_in_algorithm)
    maxv = sorted(probs.items(), key=lambda x: x[1], reverse=True)[0]

    return res_out[maxv[0]]

@app.route('/getaudio/<fname>', methods=['GET'])
def get_audio(fname):
    audio_folder = 'audiofiles'
    if fname and os.path.exists(os.path.join(audio_folder, fname)):
        return send_from_directory(audio_folder, fname)
    else:
        return send_from_directory(audio_folder, default_nothing)

@app.route('/')
def index():
    return render_template('homepage.html')


if __name__ == "__main__":
    parameters = json.load(open('parameters.json'))

    savedposs_clear_limit = parameters["savedposs_clear_limit"]  
    #any rssi values below that number are cleared for being too inaccurate, default is -80
    allowed_error_in_algorithm = parameters["allowed_error_in_algorithm"]
    #error margin for the detection algorithm, default is 10
    default_nothing = parameters["default_nothing"]
    #default mp3 file of norhing
    apk_release_link = parameters["apk_release_link"]
    #release link to the apk
    test_port = parameters["test_port"]
    #port thie app is hosted on for testing purposes, default is 22222
    
    check_saved_poss(threshold=savedposs_clear_limit)
    app.run(host='0.0.0.0', port=test_port)
