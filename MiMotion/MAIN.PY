import re
import sys
import json
import time
import random
import requests
import urllib.parse


class Account(object):

    def __init__(self, userName, passWord, stepRange):
        self.error = []
        if userName == "" or passWord == "":
            print("▶▶▶▶▶ UserName Or PassWord Cannot Be Empty! ◀◀◀◀◀")
            self.error.append("UserName Or PassWord Cannot Be Empty")
            return "UserName Or PassWord Cannot Be Empty"
        else:
            self.userName = str(userName)
            self.passWord = str(passWord)

        if int(stepRange[0]) != int(stepRange[1]):
            self.step = str(random.randint(int(stepRange[0]), int(stepRange[1])))
        else:
            self.step = str(int(0.5 * (int(stepRange[0]) + int(stepRange[1]))))


    def getCode(self, e):
        cop = re.compile("(?<=access=).*?(?=&)")
        return cop.findall(e)[0]


    def getError(self):
        return ", ".join(self.error)


    def getTimeStamp(self):
        rsp = requests.get("http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp", headers = {"User-Agent" : "Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)"}).json()
        return rsp['data']['t']


    def getAppToken(self, loginToken):
        url = f"https://account-cn.huami.com/v1/client/app_tokens" \
              f"?app_name=com.xiaomi.hm.health&dn=api-user.huami.com%2Capi-mifit.huami.com%2Capp-analytics.huami.com" \
              f"&login_token={loginToken}"
        rsp = requests.get(url, headers = {"User-Agent" : "Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)"}).json()
        return rsp['token_info']['app_token']


    def startLogin(self):
        header = {
            "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8",
            "User-Agent" : "MiFit/4.6.0 (iPhone; iOS 14.0.1; Scale/2.00)"
        }

        url_ = "https://api-user.huami.com/registrations/+86" + self.userName + "/tokens"
        data_ = {
            "client_id": "HuaMi",
            "password": self.passWord,
            "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
            "token": "access"
        }
        rsp_ = requests.post(url_, data = data_, headers = header, allow_redirects = False)

        try:
            location = rsp_.headers["Location"]
            code = self.getCode(location)
        except:
            return 0, 0    

        url__ = "https://account.huami.com/v2/client/login"
        data__ = {
            "app_name": "com.xiaomi.hm.health",
            "app_version": "4.6.0",
            "code": code,
            "country_code": "CN",
            "device_id": "2C8B4939-0CCD-4E94-8CBA-CB8EA6E613A1",
            "device_model": "phone",
            "grant_type": "access_token",
            "third_name": "huami_phone",
        }
        rsp__ = requests.post(url__, data = data__, headers = header).json()

        return rsp__["token_info"]["user_id"], rsp__["token_info"]["login_token"]


    def startMotion(self):
        userID, loginToken = self.startLogin()

        if loginToken == 0:
            print("▶▶▶▶▶ Login Fail! ◀◀◀◀◀")
            self.error.append("Login Fail")
            return "Login Fail"

        appToken = self.getAppToken(loginToken)

        sum = {
            "v": 6,
            "slp": {
                "st": int(time.time()),
                "ed": int(time.time()),
                "dp": 0,
                "lt": 0,
                "wk": 0,
                "usrSt": -1440,
                "usrEd": -1440,
                "wc": 0,
                "is": 0,
                "lb": 0,
                "to": 0,
                "dt": 0,
                "rhr": 0,
                "ss": 0
            },
            "stp": {
                "ttl": self.step,
                "dis": 10627,
                "cal": 510,
                "wk": 41,
                "rn": 50,
                "runDist": 7654,
                "runCal": 397,
                "stage": [
                    {
                        "start": 327,
                        "stop": 341,
                        "mode": 1,
                        "dis": 481,
                        "cal": 13,
                        "step": 680
                    },
                    {
                        "start": 342,
                        "stop": 367,
                        "mode": 3,
                        "dis": 2295,
                        "cal": 95,
                        "step": 2874
                    },
                    {
                        "start": 368,
                        "stop": 377,
                        "mode": 4,
                        "dis": 1592,
                        "cal": 88,
                        "step": 1664
                    },
                    {
                        "start": 378,
                        "stop": 386,
                        "mode": 3,
                        "dis": 1072,
                        "cal": 51,
                        "step": 1245
                    },
                    {
                        "start": 387,
                        "stop": 393,
                        "mode": 4,
                        "dis": 1036,
                        "cal": 57,
                        "step": 1124
                    },
                    {
                        "start": 394,
                        "stop": 398,
                        "mode": 3,
                        "dis": 488,
                        "cal": 19,
                        "step": 607
                    },
                    {
                        "start": 399,
                        "stop": 414,
                        "mode": 4,
                        "dis": 2220,
                        "cal": 120,
                        "step": 2371
                    },
                    {
                        "start": 415,
                        "stop": 427,
                        "mode": 3,
                        "dis": 1268,
                        "cal": 59,
                        "step": 1489
                    },
                    {
                        "start": 428,
                        "stop": 433,
                        "mode": 1,
                        "dis": 152,
                        "cal": 4,
                        "step": 238
                    },
                    {
                        "start": 434,
                        "stop": 444,
                        "mode": 3,
                        "dis": 2295,
                        "cal": 95,
                        "step": 2874
                    },
                    {
                        "start": 445,
                        "stop": 455,
                        "mode": 4,
                        "dis": 1592,
                        "cal": 88,
                        "step": 1664
                    },
                    {
                        "start": 456,
                        "stop": 466,
                        "mode": 3,
                        "dis": 1072,
                        "cal": 51,
                        "step": 1245
                    },
                    {
                        "start": 467,
                        "stop": 477,
                        "mode": 4,
                        "dis": 1036,
                        "cal": 57,
                        "step": 1124
                    },
                    {
                        "start": 478,
                        "stop": 488,
                        "mode": 3,
                        "dis": 488,
                        "cal": 19,
                        "step": 607
                    },
                    {
                        "start": 489,
                        "stop": 499,
                        "mode": 4,
                        "dis": 2220,
                        "cal": 120,
                        "step": 2371
                    },
                    {
                        "start": 500,
                        "stop": 511,
                        "mode": 3,
                        "dis": 1268,
                        "cal": 59,
                        "step": 1489
                    },
                    {
                        "start": 512,
                        "stop": 522,
                        "mode": 1,
                        "dis": 152,
                        "cal": 4,
                        "step": 238
                    }
                ]
            },
            "goal": 8000,
            "tz": "28800"
        }

        data = [
            {
                "data_hr": "//////9L////////////Vv///////////0v///////////9e/////0n/a///S////////////0b//////////1FK////////////R/////////////////9PTFFpaf9L////////////R////////////0j///////////9K////////////Ov///////////zf///86/zr/Ov88/zf/Pf///0v/S/8/////////////Sf///////////z3//////0r/Ov//////S/9L/zb/Sf9K/0v/Rf9H/zj/Sf9K/0//N////0D/Sf83/zr/Pf9M/0v/Ov9e////////////S////////////zv//z7/O/83/zv/N/83/zr/N/86/z//Nv83/zn/Xv84/zr/PP84/zj/N/9e/zr/N/89/03/P/89/z3/Q/9N/0v/Tv9C/0H/Of9D/zz/Of88/z//PP9A/zr/N/86/zz/Nv87/0D/Ov84/0v/O/84/zf/MP83/zH/Nv83/zf/N/84/zf/Of82/zf/OP83/zb/Mv81/zX/R/9L/0v/O/9I/0T/S/9A/zn/Pf89/zn/Nf9K/07/N/83/zn/Nv83/zv/O/9A/0H/Of8//zj/PP83/zj/S/87/zj/Nv84/zf/Of83/zf/Of83/zb/Nv9L/zj/Nv82/zb/N/85/zf/N/9J/zf/Nv83/zj/Nv84/0r/Sv83/zf/MP///zb/Mv82/zb/Of85/z7/Nv8//0r/S/85/0H/QP9B/0D/Nf89/zj/Ov83/zv/Nv8//0f/Sv9O/0ZeXv///////////1X///////////9B////////////TP///1b//////0////////////9N/////////v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+",
                "date": time.strftime("%F"),
                "data": [
                    {
                        "start": 0,
                        "stop": 1439,
                        "value": "UA8AUBQAUAwAUBoAUAEAYCcAUBkAUB4AUBgAUCAAUAEAUBkAUAwAYAsAYB8AYB0AYBgAYCoAYBgAYB4AUCcAUBsAUB8AUBwAUBIAYBkAYB8AUBoAUBMAUCEAUCIAYBYAUBwAUCAAUBgAUCAAUBcAYBsAYCUAATIPYD0KECQAYDMAYB0AYAsAYCAAYDwAYCIAYB0AYBcAYCQAYB0AYBAAYCMAYAoAYCIAYCEAYCYAYBsAYBUAYAYAYCIAYCMAUB0AUCAAUBYAUCoAUBEAUC8AUB0AUBYAUDMAUDoAUBkAUC0AUBQAUBwAUA0AUBsAUAoAUCEAUBYAUAwAUB4AUAwAUCcAUCYAUCwKYDUAAUUlEC8IYEMAYEgAYDoAYBAAUAMAUBkAWgAAWgAAWgAAWgAAWgAAUAgAWgAAUBAAUAQAUA4AUA8AUAkAUAIAUAYAUAcAUAIAWgAAUAQAUAkAUAEAUBkAUCUAWgAAUAYAUBEAWgAAUBYAWgAAUAYAWgAAWgAAWgAAWgAAUBcAUAcAWgAAUBUAUAoAUAIAWgAAUAQAUAYAUCgAWgAAUAgAWgAAWgAAUAwAWwAAXCMAUBQAWwAAUAIAWgAAWgAAWgAAWgAAWgAAWgAAWgAAWgAAWREAWQIAUAMAWSEAUDoAUDIAUB8AUCEAUC4AXB4AUA4AWgAAUBIAUA8AUBAAUCUAUCIAUAMAUAEAUAsAUAMAUCwAUBYAWgAAWgAAWgAAWgAAWgAAWgAAUAYAWgAAWgAAWgAAUAYAWwAAWgAAUAYAXAQAUAMAUBsAUBcAUCAAWwAAWgAAWgAAWgAAWgAAUBgAUB4AWgAAUAcAUAwAWQIAWQkAUAEAUAIAWgAAUAoAWgAAUAYAUB0AWgAAWgAAUAkAWgAAWSwAUBIAWgAAUC4AWSYAWgAAUAYAUAoAUAkAUAIAUAcAWgAAUAEAUBEAUBgAUBcAWRYAUA0AWSgAUB4AUDQAUBoAXA4AUA8AUBwAUA8AUA4AUA4AWgAAUAIAUCMAWgAAUCwAUBgAUAYAUAAAUAAAUAAAUAAAUAAAUAAAUAAAUAAAUAAAWwAAUAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAeSEAeQ8AcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBcAcAAAcAAAcCYOcBUAUAAAUAAAUAAAUAAAUAUAUAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcCgAeQAAcAAAcAAAcAAAcAAAcAAAcAYAcAAAcBgAeQAAcAAAcAAAegAAegAAcAAAcAcAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcCkAeQAAcAcAcAAAcAAAcAwAcAAAcAAAcAIAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcCIAeQAAcAAAcAAAcAAAcAAAcAAAeRwAeQAAWgAAUAAAUAAAUAAAUAAAUAAAcAAAcAAAcBoAeScAeQAAegAAcBkAeQAAUAAAUAAAUAAAUAAAUAAAUAAAcAAAcAAAcAAAcAAAcAAAcAAAegAAegAAcAAAcAAAcBgAeQAAcAAAcAAAcAAAcAAAcAAAcAkAegAAegAAcAcAcAAAcAcAcAAAcAAAcAAAcAAAcA8AeQAAcAAAcAAAeRQAcAwAUAAAUAAAUAAAUAAAUAAAUAAAcAAAcBEAcA0AcAAAWQsAUAAAUAAAUAAAUAAAUAAAcAAAcAoAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAYAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBYAegAAcAAAcAAAegAAcAcAcAAAcAAAcAAAcAAAcAAAeRkAegAAegAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAEAcAAAcAAAcAAAcAUAcAQAcAAAcBIAeQAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBsAcAAAcAAAcBcAeQAAUAAAUAAAUAAAUAAAUAAAUBQAcBYAUAAAUAAAUAoAWRYAWTQAWQAAUAAAUAAAUAAAcAAAcAAAcAAAcAAAcAAAcAMAcAAAcAQAcAAAcAAAcAAAcDMAeSIAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBQAeQwAcAAAcAAAcAAAcAMAcAAAeSoAcA8AcDMAcAYAeQoAcAwAcFQAcEMAeVIAaTYAbBcNYAsAYBIAYAIAYAIAYBUAYCwAYBMAYDYAYCkAYDcAUCoAUCcAUAUAUBAAWgAAYBoAYBcAYCgAUAMAUAYAUBYAUA4AUBgAUAgAUAgAUAsAUAsAUA4AUAMAUAYAUAQAUBIAASsSUDAAUDAAUBAAYAYAUBAAUAUAUCAAUBoAUCAAUBAAUAoAYAIAUAQAUAgAUCcAUAsAUCIAUCUAUAoAUA4AUB8AUBkAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAA",
                        "tz": 32,
                        "did": "DA932FFFFE8816E7",
                        "src": 24
                    }
                ],
                "summary": json.dumps(sum),
                "source": 24,
                "type": 0
            }
        ]

        requests.post(f'https://api-mifit-cn.huami.com/v1/data/band_data.json?&t={self.getTimeStamp()}', data = f'userid={userID}&last_sync_data_time=1597306380&device_type=0&last_deviceid=DA932FFFFE8816E7&data_json={urllib.parse.quote(json.dumps(data))}', headers = {"apptoken" : appToken, "Content-Type" : "application/x-www-form-urlencoded"}).json()


class DingRobot(object):

    def __init__(self, pushMode, pushTokn, msgTitle):
        if pushMode != "" and pushTokn == "":
            print("▶▶▶▶▶ PushTokn Cannot Be Empty! ◀◀◀◀◀")
            return "PushTokn Cannot Be Empty"
        elif pushMode != "":
            self.pushMode = "1"; self.pushTokn = pushTokn
        else:
            self.pushMode = "0"; self.pushTokn = "0"

        self.title = msgTitle

        self.url = f"https://oapi.dingtalk.com/robot/send?access_token={self.pushTokn}"
        self.data = {}
        self.header = {"Content-Type" : "application/json"}

        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600))


    def makeMsg(self, bodyList):
        fail = 0; sucs = 0
        text_fail = ""; text_sucs = ""

        for body in bodyList:
            if body.error != []:
                fail += 1
                text_fail += f"【{fail}】 {body.userName[:3]}****{body.userName[-4:]} \n\n 修改步数：{body.step}步 修改失败！ {body.getError()}! \n\n "
            else:
                sucs += 1
                text_sucs += f"【{sucs}】 {body.userName[:3]}****{body.userName[-4:]} \n\n 修改步数: {body.step}步 修改成功！ \n\n "

        if fail != 0:
            self.data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"{self.title}",
                    "text": f"<font color=#6A65FF>**{self.title}**</font> \n\n {self.time} \n\n --- \n\n <font color=#76CCFF>**现有管理账号 {len(bodyList)} 个**</font> \n\n 成功账号 {sucs} 个，失败账号 {fail} 个 \n\n --- \n\n <font color=#92D050>**成功账号列表**</font> \n\n {text_sucs} --- \n\n <font color=#FF6666>**失败账号列表**</font> \n\n {text_fail} <font color=#6A65FF>{self.title}</font> \n\n @xxx"
                },
                "at": {
                    "atMobiles": ["xxx"]
                    }
            }
        else:
            self.data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"{self.title}",
                    "text": f"<font color=#6A65FF>**{self.title}**</font> \n\n {self.time} \n\n --- \n\n <font color=#76CCFF>**现有管理账号 {len(bodyList)} 个**</font> \n\n 成功账号 {sucs} 个，失败账号 {fail} 个 \n\n --- \n\n <font color=#92D050>**成功账号列表**</font> \n\n {text_sucs} <font color=#6A65FF>{self.title}</font>"
                }
            }

        return "MakeMsg Success"


    def pushMsg(self):

        try:
            rsp = requests.post(self.url, data = json.dumps(self.data), headers = self.header)
            msg = rsp.json()

            if msg['errcode'] != 0:
                print("▶▶▶▶▶ PushMsg Error! ◀◀◀◀◀")
                return "PushMsg Error"

        except:
            print("▶▶▶▶▶ PushMsg Fail! ◀◀◀◀◀")
            return "PushMsg Fail"

        else:
            return "PushMsg Success"


if __name__ == "__main__":

    try:
        pushMode = sys.argv[1]
        pushTokn = sys.argv[2]
        userList = sys.argv[3].split('#')
        passList = sys.argv[4].split('#')
        stepArry = sys.argv[5].replace('[', '').replace(']', '').split('-')
    except:
        print("▶▶▶▶▶ Parameter Error! ◀◀◀◀◀")
        exit(1)

    DingRobotGithub = DingRobot(pushMode = pushMode, pushTokn = pushTokn, msgTitle = "【Github】MiMotion状态推送")

    if len(userList) == len(passList):
        seqs = 0; text = ""
        for user in userList:
            exec(f"Account{user} = Account(userName = userList[seqs], passWord = passList[seqs], stepRange = stepArry)")
            exec(f"Account{user}.startMotion()")
            text += f"Account{user}, "
            seqs += 1
    else:
        print("▶▶▶▶▶ UserName/PassWord Error! ◀◀◀◀◀")
        exit(2)
    
    exec(f"DingRobotGithub.makeMsg(bodyList = [{text[:-2]}])")
    exec(f"DingRobotGithub.pushMsg()")
