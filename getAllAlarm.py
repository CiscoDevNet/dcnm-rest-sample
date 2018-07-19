import http.client
import ssl
import base64
import string
import json

__author__ = "Louis Jia"
__copyright__ = "Copyright (C) 2018 Cisco System"

def getRestToken(username, password, serverip):
  ssl._create_default_https_context = ssl._create_unverified_context

  ##replace server ip address here
  conn = http.client.HTTPSConnection(serverip)

  payload = "{\"expirationTime\" : 10000000000}\n"

  ## replace user name and password here
  authenStr="%s:%s" % (username, password)

  base64string = base64.encodestring(bytes(authenStr, 'utf-8'))
  tmpstr= "Basic %s" % base64string
  authorizationStr = tmpstr.replace("b\'","").replace("\\n\'","");
  print(authorizationStr);

  headers = {
      'content-type': "application/json",
      'authorization': authorizationStr,
      'cache-control': "no-cache"
      }

  conn.request("POST", "/rest/logon", payload, headers)

  res = conn.getresponse()
  data = res.read()
  print(data)
  longstr=data.decode("utf-8")
  strArr=longstr.split("\"")
  return strArr[3]

def  getAllAlarm(serverip, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/alarms/alarmlist/?history=false&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  for x in decoded :
    print("=============================================")
    print(x['deviceName'])
    print(x['deviceAttributes'])
    print(x['message'])
    print(x['lastScanTimeStamp'])
    events = json.loads(x['associatedEvents'])
    descriptionStr=''
    severityStr=''
    for y in events :
        if 'description' in y :
            descriptionStr=y['description']
        if 'severity' in y :
            severityStr=y['severity']
        print('    '+y['EventSwitch']+':'+y['EventType']+':'+descriptionStr+':'+severityStr)
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "nbv12345", "172.28.164.141")
print(restToken)

# DCNM server ip,  resetTotken
getAllAlarm("172.28.164.141", restToken)


