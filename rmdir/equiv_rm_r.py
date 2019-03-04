#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......equiv_rm_r
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....Remove directory in python
#USAGE....rm_r(path)

import os
import shutil

def rm_r(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)