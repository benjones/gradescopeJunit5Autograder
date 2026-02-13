#!/usr/bin/env python3

info = '''
Usually when building an autograder, you need to put it in a project with your own solution
to run and test it and make sure everything compiles, etc.

The script takes a JSON description of your project (see the sample included for info)
the copies appropriate files into the right spot for the autograder

fills in a run_autograder template script, or if run_autograder exists in the working directory, uses that

and zips everything you need up

It will assume you're in the top level of your project, so it will automatically prepend 'src/'
when looking for files to zip

It will look for the extra files and specified jar files in the PWD

If you want want to compile all provided student files (ie something like `javac studentPackage/*.java`), leave the `studentFiles` field blank.  Note that this will probably break if there are multiple `main` methods

the signatureChecks field takes a list of classes, with their list of method signatures (name, return type, arg types).
The example below just has a single class with 4 methods to check

"signatureChecks" : [{"className" : "assign06.Word",
    "methods":  [
      {"name": "countOccurrences", "returnType": "int", "args" : ["char"]},
      {"name": "reverse", "returnType" : "class assign06.Word", "args": []},
      {"name": "capitalizeLastOccurrence", "returnType": "void", "args": ["char"]},
      {"name": "toString", "returnType": "class java.lang.String", "args": []}
    ]}]

'''

import sys

if(len(sys.argv) != 2):
    print(info)
    print("Usage: release.py <json assignment description>")
    sys.exit(1)

import json

config = json.load(open(sys.argv[1]))

print(json.dumps(config))

# command or onFail should write to /autograder/results/results.json
def tryOrFail(command, onFail = ""):
    return '''
    {0}
    exit_status=$?
    if [ $exit_status -eq 1 ]; then
        echo "{0} failed"
        {1}
        exit $exit_status
    fi

    '''.format(command, onFail)


from string import Template
run_autograder_template = Template('''#!/usr/bin/env bash

cd /autograder/source

mkdir -p out
mkdir -p $studentPackage 
$copyCommand

mkdir -p /autograder/results

$checkFilesCommand
$compileStudentCodeCommand
$signatureCheckCommand
#compile tests

# compile everything
$compileAllCodeCommand

java -jar junit-platform-console-standalone-1.14.2.jar --class-path out:$jarList --scan-class-path
''')

from glob import glob
import itertools
import os




studentPackage = config['studentPackage']
jarList = ":".join(config['jars']) if 'jars' in config else ''

copyCommand = ""
compileStudentCodeCommand = ""
checkFilesCommand = ""
signatureCheckCommand = ""
compileAllCodeCommand = ""
if 'studentFiles' in config:
    listOfStudentFiles = " ".join(map(lambda x : "/autograder/submission/" + x, config['studentFiles']))
    copyCommand = 'cp {0} {1}'.format(listOfStudentFiles, studentPackage)
    allJavaFiles = list(itertools.chain(map( lambda x: config['studentPackage'] + "/" + x,
                                         config['studentFiles']),
                                    config["autograderFiles"]))
    checkFilesCommand = tryOrFail("python3 checkForFiles.py {0}".format(listOfStudentFiles))
    compileStudentCodeCommand = 'javac -d out {listOfStudentFiles} >>compileLog.txt 2>&1'.format_map(
        {'listOfStudentFiles' : listOfStudentFiles})
    compileAllCodeCommand = 'javac -d out -cp out:{jarList} {allJavaFiles} >>compileLog.txt 2>&1'.format_map(
    {'jarList' : jarList, 'allJavaFiles' : " ".join(allJavaFiles)})

else:
    copyCommand = 'cp /autograder/submission/* ' + studentPackage
    compileStudentCodeCommand = 'javac -d out {studentPackage}/*.java >>compileLog.txt 2>&1'.format_map({'studentPackage': studentPackage})
    compileAllCodeCommand = 'javac -d out -cp out:{jarList} {studentPackage}/*.java {autograderFiles} >>compileLog.txt 2>&1'.format_map({'jarList' : jarList, 'studentPackage': studentPackage, 'autograderFiles' : " ".join(config["autograderFiles"])})

methodCheckFiles = {}
signatureCheckCommand = ""
if 'signatureChecks' in config:
    methodCheckFiles['methodSignatures.json'] = json.dumps(config['signatureChecks'])
    signatureCheckCommand = tryOrFail("java -cp out:{jarList} edu/utah/cs/autograder/MethodSignatureChecker.java < methodSignatures.json".format_map({"jarList" : jarList}))
    
substitutions = {
    "studentPackage" : studentPackage,
    "copyCommand" : copyCommand,
    "checkFilesCommand" : checkFilesCommand,
    "compileStudentCodeCommand" : tryOrFail(compileStudentCodeCommand, "python3 compileFail.py"),
    "signatureCheckCommand" : signatureCheckCommand,
    "jarList" : jarList,
    "compileAllCodeCommand" : tryOrFail(compileAllCodeCommand, "python3 compileFail.py")
}

# if run_autograder exists, use that, otherwise use the default template
runAutograderContents = ""
if os.path.exists("run_autograder"):
    print("Using run_autograder script from project folder")
    runAutograderContents = open('run_autograder', encoding="utf-8").read()
else:
    print("Using default run_autograder script")
    runAutograderContents = run_autograder_template.substitute(substitutions)


scripts = {
"compileFail.py": '''#!/usr/bin/env python3

import json

res = {}
res['score'] = 0
res['output'] = "Failed to compile: " + open('compileLog.txt', encoding='utf-8').read()

f = open('/autograder/results/results.json', 'w', encoding="utf-8")
f.write(json.dumps(res))
''',

"setup.sh": '''#!/usr/bin/env bash

# autograder uses gson and the junit 5 runner
# nothing to do...
''',
"checkForFiles.py": '''#!/usr/bin/env python3
import os
import sys
import json

for f in sys.argv[1:]:
    if not os.path.exists(f):
        res = {}
        res['score'] = 0
        res['output'] = "Expected file " + f + " missing.  You will currently earn 0 autograder points. Please make sure all required files are included and resubmit."

        f = open('/autograder/results/results.json', 'w', encoding="utf-8")
        f.write(json.dumps(res))
        sys.exit(1)
'''
}
from zipfile import ZipFile

zipContents = scripts | {'run_autograder' : runAutograderContents} | methodCheckFiles

output = ZipFile(config['studentPackage'] + "_autograder.zip", 'w')
for path, contents in zipContents.items():
    output.writestr(path, contents)


for jar in config['jars']:
    output.write(jar, jar)

for f in config['autograderFiles']:
    output.write("src/" + f, f)

if 'extraFiles' in config:
    for f in config['extraFiles']:
        output.write(f, f)

