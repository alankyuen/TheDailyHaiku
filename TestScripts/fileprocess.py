"""
f = open("/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/COMMON_RAW.txt", 'r+')
f2 = open("/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/COMMON.txt", 'wb')
lines = f.readlines()
for line in lines:
    text = line.split("\t")
    f2.write(text[0]+"\n")
"""

from collections import OrderedDict

seen = OrderedDict()
for line in open('/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/words_copy.txt'):
    line = line.rstrip()
    seen[line] = seen.get(line, 0) + 1

f3 = open('/Users/alanyuen/.virtualenvs/SBHacks/DeepPoetry/words_copy_unique.txt', 'wb')
f3.write("\n".join([k for k,v in seen.items() if v == 1]))
