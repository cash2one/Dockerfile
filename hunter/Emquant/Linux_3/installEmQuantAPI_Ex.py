# -*- encoding:utf-8 -*-

__author__ = 'jiejie'

import sys
import os
import platform

def installEmQuantAPI():
    print("Start to install EmQuantAPI...")
    print("Current Python version:", sys.version)

    ver = sys.version_info
    vernum = ver[0] * 10 + ver[1]
    if vernum < 30:
        exit('Error: EmQuantAPI currently only supports Python 3.x')

    currDir = os.path.split(os.path.realpath(__file__))[0]
    if str(type(currDir)) == "<type 'unicode'>":
        currDir = currDir.encode("utf-8")

    #get site-packages path
    osname = platform.uname()[0].lower()
    site_pkg_name = "dist-packages"
    
    packagepath = "."
    for x in sys.path:
        ix=x.find(site_pkg_name)
        if( ix>=0 and x[ix:]==site_pkg_name):
            packagepath=x
            pthPath = os.path.join(packagepath, "EmQuantAPI.pth")
            print(pthPath)
            pthFile = open(pthPath, "w")
            pthFile.writelines(currDir)
            pthFile.close()

    print("Success:", "EmQuantAPI installed.")

installEmQuantAPI()
