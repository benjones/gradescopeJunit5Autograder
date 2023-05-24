#!/usr/bin/env python3

import json

res = {}
res['score'] = 0
res['output'] = "Failed to compile: " + open('compileLog.txt', encoding='utf-8').read()

f = open('/autograder/results/results.json', 'w', encoding="utf-8")
f.write(json.dumps(res))
