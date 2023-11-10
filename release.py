#!/usr/bin/env python3

info = '''
Usually when building an autograder, you need to put it in a project with your own solution
to run and test it and make sure everything compiles, etc.

The script takes a JSON description of your project (see the sample included for info)
the copies appropriate files into the right spot for the autograder

fills in a run_autograder template script

and zips everything you need up

It will assume you're in the top level of your project, so it will automatically prepend 'src/'
when looking for files to zip

It will look for the specified jar files in the PWD

'''

import sys

if(len(sys.argv) != 2):
    print(info)
    print("Usage: release.py <json assignment description>")
    sys.exit(1)

import json

config = json.load(open(sys.argv[1]))

print(json.dumps(config))

from string import Template
run_autograder_template = Template('''#!/usr/bin/env bash

cd /autograder/source

mkdir -p out
mkdir -p $studentPackage 
cp $studentFiles $studentPackage

mkdir -p /autograder/results

# compile everything
javac -d out -cp out:$jarList $allJavaFiles >>compileLog.txt 2>&1

if [ $$? -ne 0 ]; then #compile failed
    echo "compile failed"
    cat compileLog.txt
    python3 compileFail.py
    exit
fi

java -jar junit-platform-console-standalone-1.9.1.jar --class-path out:$jarList --scan-class-path
''')

from glob import glob
import itertools


allJavaFiles = list(itertools.chain(map( lambda x: config['studentPackage'] + "/" + x,
                                         config['studentFiles']),
                                    config["autograderFiles"]))

substitutions = {
    "studentPackage" : config['studentPackage'],
    "studentFiles" : " ".join(map(lambda x : "/autograder/submission/" + x, config['studentFiles'])),
    "jarList" : ":".join(config['jars']),
    "allJavaFiles" : " ".join(allJavaFiles)
}

runAutograderContents = run_autograder_template.substitute(substitutions)


compileFailContents = '''#!/usr/bin/env python3

import json

res = {}
res['score'] = 0
res['output'] = "Failed to compile: " + open('compileLog.txt', encoding='utf-8').read()

f = open('/autograder/results/results.json', 'w', encoding="utf-8")
f.write(json.dumps(res))
'''

setupShContents = '''#!/usr/bin/env bash

# autograder uses gson and the junit 5 runner
# nothing to do...
'''

from zipfile import ZipFile

output = ZipFile(config['studentPackage'] + "_autograder.zip", 'w')
for path, contents in {"run_autograder" : runAutograderContents,
                  "compileFail.py" : compileFailContents,
                  "setup.sh" : setupShContents}.items():
    output.writestr(path, contents)


for jar in config['jars']:
    output.write(jar, jar)

for f in config['autograderFiles']:
    output.write("src/" + f, f)

