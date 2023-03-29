import json

thing2 = [{}, {}]

with open('savedposs.txt', 'r') as funfile:
    cnt = 0
    for s in funfile.readlines():
        
        g = json.loads(s)
        for key, value in g.items():
            if int(value) > -80:
                thing2[cnt][key] = value
        cnt += 1

print(thing2[0])
print()
print(thing2[1])