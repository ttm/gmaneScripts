import os

for i in xrange(17649,20001):
    os.system("wget http://download.gmane.org/gmane.comp.gcc.libstdc++.devel/%i/%i -O %i" % (i,i+1,i))
