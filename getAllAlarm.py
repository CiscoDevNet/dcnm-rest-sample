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

def  getAllAlarm(serverip, resttoken, start, end):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)
  rangestr="items="+str(start)+"-"+str(end)
  print(rangestr);
  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Range': rangestr
    }


  conn.request("GET", "/fm/fmrest/alarms/alarmlist/?history=false&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  print("******************************************")
  print(len(decoded));
  for alarm in decoded :
    print("=================ALARM=======================")
    print(alarm['deviceName'])
    print(alarm['deviceAttributes'])
    print(alarm['message'])
    print(alarm['lastScanTimeStamp'])
    events = json.loads(alarm['associatedEvents'])
    descriptionStr=''
    severityStr=''
    for y in events :
        if 'description' in y :
            descriptionStr=y['description']
        if 'severity' in y :
            severityStr=y['severity']
        print('    ------------EVENT------------------')
        print('    '+y['EventSwitch']+':'+y['EventType']+':'+descriptionStr+':'+severityStr)
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "cisco123", "172.23.244.229")
print(restToken)

# DCNM server ip,  resetTotken start_idx end_idx
getAllAlarm("172.23.244.229", restToken, 0, 10000)
