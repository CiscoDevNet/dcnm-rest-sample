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


def changePwd(serverip,dcnmusername,dcnmpassword,resttoken):
  conn = http.client.HTTPSConnection(serverip)
  postpayload = 'userName='+dcnmusername+'&password='+dcnmpassword+'&roleName=network-admin'

  headers = {
      'dcnm-token': resttoken,
      'content-type': "application/x-www-form-urlencoded",
      'cache-control': "no-cache"
      }

  conn.request("POST", "/fm/fmrest/dbadmin/modifyUser", postpayload, headers)
  
  res = conn.getresponse()
  print(res)
  data = res.read()
  print(data.decode("utf-8"))
  return

# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "nbv_12345", "10.157.34.131")
print(restToken)

# DCNM serverip username, dcnm password, toekn
changePwd("10.157.34.131", "test", "nbv_123456789" , restToken)

restToken=getRestToken("test", "nbv_123456789", "10.157.34.131")
print(restToken)


