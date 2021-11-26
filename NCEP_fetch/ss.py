#!/usr/bin/python
#
# python script to download selected files from rda.ucar.edu
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
import sys
import os
import urllib2
import cookielib
import datetime
import subprocess

def dt2str(dt):
    a=[int(i) for i in str(dt).split()[0].split('-')]
    return str(a[0]*100*100+a[1]*100+a[2])
#
#if (len(sys.argv) == 0):
#  print "usage: "+sys.argv[0]+" [-q] password_on_RDA_webserver"
#  print "-q suppresses the progress message for each file that is downloaded"
#  sys.exit(1)
#
passwd_idx=1
verbose=True
if (len(sys.argv) == 3 and sys.argv[1] == "-q"):
  passwd_idx=2
  verbose=False
#
cj=cookielib.MozillaCookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#
# check for existing cookies file and authenticate if necessary
do_authentication=False
if (os.path.isfile("auth.rda.ucar.edu")):
  cj.load("auth.rda.ucar.edu",False,True)
  for cookie in cj:
    if (cookie.name == "sess" and cookie.is_expired()):
      do_authentication=True
else:
  do_authentication=True
if (do_authentication):
#  passwd=sys.argv[1]
  passwd='******'
  login=opener.open("https://rda.ucar.edu/cgi-bin/login","email=*****@***&password="+passwd+"&action=login")
#
# save the authentication cookies for future downloads
# NOTE! - cookies are saved for future sessions because overly-frequent authentication to our server can cause your data access to be blocked
  cj.clear_session_cookies()
  cj.save("auth.rda.ucar.edu",True,True)
#
# download the data file(s)
#os.system('/Users/kuang/bin/ncep.cs')
path='/Users/WRF4.1/NCEP/SRF_ds461.0/'
yrold=os.popen('ls -d '+path+'20*|tail -n1').read().strip('\n').split('/')[-1]
print yrold
blk=os.popen('ls '+path+yrold+'|tail -n1').read().strip('\n').split('_')[-1].split(':')
print blk
try:
  begd=int(int(blk[1].replace('.gz',''))/100)
except:
  begd=(int(yrold)-1)*10000+1231
ldate = datetime.datetime(begd/100/100,begd/100%100,begd%100)
bdate = ldate+datetime.timedelta(days=1)
nowd = int(subprocess.check_output("date +%Y%m%d%H", shell=True)[:-3])
tdate = datetime.datetime(nowd/100/100,nowd/100%100,nowd%100)
edate = tdate+datetime.timedelta(days=-8)
E_B=str(edate-bdate)
if 'day' not in E_B:
  leng=1
else:
  leng=int(str(edate-bdate).split('day')[0])+1
if leng<=0:sys.exit('no need to download, bdate='+str(bdate)+' edate='+str(edate))
ymds=[dt2str(bdate+datetime.timedelta(days=i)) for i in xrange(leng)]
yrs=[ymd[:4] for ymd in ymds]
#add new year directory if necessary
for yr in yrs:
  os.system('mkdir -p '+path+'/'+yr)
head=['little_r/'+yr+'/SURFACE_OBS:' for yr in yrs]
listoffiles=[head[i]+ymds[i]+str(h)  for i in xrange(len(ymds)) for h in ['00','06','12','18']]
for file in listoffiles:
  idx=file.rfind("/")
  if (idx > 0):
    ofile=file[idx+1:]#.replace(':','_')
  else:
    ofile=file#.replace(':','_')
  yr=file.split('/')[1]
  path1=path+yr+'/'
  if os.path.isfile(path1+ofile) or os.path.isfile(path1+ofile+'.gz') :continue
  if (verbose):
    sys.stdout.write("downloading "+ofile+"...")
    sys.stdout.flush()
  try:
    infile=opener.open("http://rda.ucar.edu/data/ds461.0/"+file)
  except:
    continue
  outfile=open(ofile,"wb")
  outfile.write(infile.read())
  outfile.close()
  if (verbose):
    sys.stdout.write("done.\n")
  os.system('mkdir -p '+path1[:-1])
  os.system('mv '+ofile+' '+path1)
