# -*- coding: utf-8 -*-

"""
io utils function
"""
from __future__ import print_function


def read_content(filename, numline=2):
    if not isinstance(filename, file):
        f = open(filename)
    else:
        f = filename
    content = []
    for i in range(numline):
        line = f.readline().strip()
        content.append(int(line) if line.isdigit() else line)
    f.close()
    return tuple(content)

def write_result(filename, content, sep=" "):
    if not isinstance(filename, file):
        f = open(filename, "w")
    else:
        f = filename
    print(" ".join([str(c) if not isinstance(c,str) else c for c in content]), 
          file=f)

