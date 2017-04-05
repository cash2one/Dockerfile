from distutils.core import setup
from distutils.core import Extension
import platform
import sys


def InstallPython():
    
    plate = platform.architecture()
    strbit= plate[0]
    iswin = 'Windows' in platform.system();
    version=sys.version  
    #print(version);
    verss=version.split()[0].split('.');
    ver=int(verss[0])+float(verss[1])/10;
    bit=int(strbit.split('bit')[0]);

    if(len(sys.argv)<=1):
        print('No iFinDPy path!');
        return;
    #print(sys.argv[1:])

    srcpath=sys.argv[1];
    if(iswin):
        if not (srcpath.endswith('\\')):
            srcpath=srcpath+'\\'
    else:     
        if not (srcpath.endswith('/')):
            srcpath=srcpath+'/'
        
    sitepath=".";
    for x in sys.path:
        ix=x.find('site-packages')
        if( ix>=0 and x[ix:]=='site-packages'):
          sitepath=x;
          break;
        ix=x.find('dist-packages')
        if( ix>=0 and x[ix:]=='dist-packages'):
          sitepath=x;
          break;

    print(sitepath)
    if(iswin):
        filepath=sitepath+"\\iFinDPy.pth"
    else:
        filepath=sitepath+"/iFinDPy.pth"
    #print(filepath);    

    if(ver<2.6):
       print('Error: Python version must be >=2.6!')
       return;

    if(bit==64 ):
       print('Python is 64 bits')
       srcpath=srcpath+"bin64"
    else:#if(bit==64 ):
       print('Python is 32 bits')
       srcpath=srcpath+"bin"

    #print(srcpath);
    sitefile=open(filepath,'w');
    sitefile.writelines(srcpath)
    sitefile.close();
    print('Installed into'),
    print(sitepath),
    print('OK!');


InstallPython()
