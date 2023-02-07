import re
import sys
import json
import time
import hashlib
import requests


class Account(object):

    def __init__(self, userName, passWord, hostBase):
        self.error = []
        if userName == "" or passWord == "":
            print("▶▶▶▶▶ UserName Or PassWord Cannot Be Empty! ◀◀◀◀◀")
            self.error.append("UserName Or PassWord Cannot Be Empty")
            return "UserName Or PassWord Cannot Be Empty"
        else:
            self.userNameOri = str(userName)
            self.passWordOri = str(passWord)
            self.userName = self.userNameOri.encode('GBK')
            self.passWord = hashlib.md5(self.passWordOri.encode('GBK')).hexdigest()

        if hostBase == "":
            print("▶▶▶▶▶ HostBase Cannot Be Empty! ◀◀◀◀◀")
            self.error.append("HostBase Cannot Be Empty")
            return "HostBase Cannot Be Empty"
        else:
            self.hostBase = hostBase
            self.baseURL = "https://" + self.hostBase + "/portal.php"
            self.homeURL = "https://" + self.hostBase + "/home.php"
            self.loginURL = "https://" + self.hostBase + "/member.php"
            self.checkinURL = "https://" + self.hostBase + "/plugin.php"
            self.checkinPage = "https://" + self.hostBase + "/k_misign-sign.html"

        self.ticketNum = -1

        self.UA = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
        self.header = {"User-Agent" : self.UA, "Host": self.hostBase}
        self.session = requests.Session()


    def getError(self):
        return ", ".join(self.error)


    def userLogin(self):
        rsp = self.session.get(self.loginURL, params = {"referer" : "", "mod" : "logging", "action" : "login"}, headers = self.header).text

        loginFormHash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', rsp).group(1).encode('ascii')
        loginLoginHash = re.search(r'<div class="nex_denglu_box" id="main_messaqge_(.+?)">', rsp).group(1).encode('ascii')

        rqs = self.session.post(self.loginURL, params = {"mod" : "logging", "action" : "login", "loginsubmit" : "yes", "loginhash" : loginLoginHash, "inajax" : 1}, \
            data = {"referer" : self.baseURL, "loginfield" : "username", "username" : self.userName, "password" : self.passWord, "questionid" : 0, "answer" : "", "formhash" : loginFormHash}, headers = self.header).text

        if not re.search(u'现在将转入登录前页面', rqs):
            print("▶▶▶▶▶ Login Fail! ◀◀◀◀◀")
            self.error.append("Login Fail")
            return "Login Fail"


    def userCheckin(self):
        rsp = self.session.get(self.checkinPage, params = {"referer" : self.baseURL}).text

        checkinFormHash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', rsp).group(1).encode('ascii')
        self.session.get(self.checkinURL, params = {"id" : "k_misign:sign", "operation" : "qiandao", "formhash" : checkinFormHash, "format" : "empty"})

        rqs = self.session.get(self.checkinPage, params = {"referer" : self.baseURL}).text

        try:
            checkinNum = re.search(r'<input type="hidden" class="hidnum" id="qiandaobtnnum" value="(.+?)">', rqs).group(1).encode('ascii')
        except:
            print("▶▶▶▶▶ Checkin Fail! ◀◀◀◀◀")
            self.error.append("Checkin Fail")
            return "Checkin Fail"

        if not int(checkinNum) >= 1:
            print("▶▶▶▶▶ Checkin Fail! ◀◀◀◀◀")
            self.error.append("Checkin Fail")
            return "Checkin Fail"


    def getTicketNum(self):
        rsp = self.session.get(self.homeURL, params = {"referer" : self.baseURL, "mod" : "spacecp", "ac" : "credit", "showcredit" : 1, "inajax" : 1, "ajaxtarget" : "extcreditmenu_menu"}).text

        try:
            # hCredit1 = re.search(r'<span id="hcredit_1">(.+?)</span>', rsp).group(1).encode('ascii')
            hCredit2 = re.search(r'<span id="hcredit_2">(.+?)</span>', rsp).group(1).encode('ascii')
            # hCredit3 = re.search(r'<span id="hcredit_3">(.+?)</span>', rsp).group(1).encode('ascii')

            #self.ticketNum = hCredit1
            self.ticketNum = hCredit2
            #self.ticketNum = hCredit3
        except:
            print("▶▶▶▶▶ Get Ticket Number Fail! ◀◀◀◀◀")
            self.error.append("Get Ticket Number Fail")
            return "Get Ticket Number Fail"           


    def startExecute(self):
        self.userLogin()
        if len(self.error) == 0: self.userCheckin()
        if len(self.error) == 0: self.getTicketNum()


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
                text += f"【{fail}】</font> {body.userName.decode('utf-8')} \n\n 登录密码：{body.passWordOri} 签到失败！ {body.getError()}! \n\n "
            else:
                sucs += 1
                text += f"【{sucs}】</font> {body.userName.decode('utf-8')} \n\n 当前积分：{body.ticketNum.decode('utf-8')}分 签到成功！ \n\n "

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

            if msg["errcode"] != 0:
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
        userList = sys.argv[3].split("#")
        passList = sys.argv[4].split("#")
        hostPool = sys.argv[5].split("#")
    except:
        print("▶▶▶▶▶ Parameter Error! ◀◀◀◀◀")
        exit(1)

    DingRobotGithub = DingRobot(pushMode = pushMode, pushTokn = pushTokn, msgTitle = "【Github】DiscuzX状态推送")

    if len(userList) == len(passList):
        seqs = 0; text = ""
        for user in userList:
            if len(userList) > 1:
                exec(f"Account{user} = Account(userName = userList[seqs], passWord = passList[seqs], hostBase = hostPool[seqs + 1])")
                exec(f"Account{user}.startExecute()")
                text += f"Account{user}, "
                seqs += 1
            else:
                exec(f"Account{user} = Account(userName = userList[seqs], passWord = passList[seqs], hostBase = hostPool[seqs])")
                exec(f"Account{user}.startExecute()")
                text += f"Account{user}, "
                seqs += 1
    else:
        print("▶▶▶▶▶ UserName/PassWord Error! ◀◀◀◀◀")
        exit(2)
    
    exec(f"DingRobotGithub.makeMsg(bodyList = [{text[:-2]}])")
    exec(f"DingRobotGithub.pushMsg()")
