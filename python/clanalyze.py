import sys
import os.path
from itertools import takewhile
import re
import python.system

# directory = os.path.abspath(sys.argv[1])
# csv       = os.path.abspath(sys.argv[2])
# exe       = sys.argv[3]
# opts      = sys.argv[4]

def clanalyze(directory, temp_path, csv, exe, opts):
    print("======Running cl /analyze=======")
    print("Working dir:", directory)
    print("CSV file:", csv)
    print("Excutable:", exe)
    print("Executable options:", opts)

    try:
        command = exe + " \"" + directory + "/*.c*\" /I \"" + directory + "\""
        (output, err, exit, time) = python.system.system_call(command)
    except:
        print("TROUBLE CALLING ANALYZER(0): warning XXX: ", sys.exc_info())

    with open(temp_path, "w") as text_file:
        print(output, file=text_file)

    regexp = re.compile("(\S+)\((\d+)\)\s?:\s+\S+\s+\S+:\s+(.+)")
    sys.stdout = open(csv, "w")
    with open(temp_path) as f:
        for line in f.readlines():
            m = regexp.match(line)
            if not (m is None):
                name = m.groups()[0]
                idx = name.rfind("\\")
                print(name[idx+1:], ", ", m.groups()[1], ",", m.groups()[2])
    sys.stdout = sys.__stdout__
