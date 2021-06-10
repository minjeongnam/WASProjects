from pymongo import MongoClient

MONGOURL = "ec2-54-180-116-84.ap-northeast-2.compute.amazonaws.com:"
MONGOPORT = "27017"

class mongoManager :
    def __init__(self, url) -> None:
        client = MongoClient(MONGOURL+MONGOPORT)
        self.coll = client['WAS'][url]

    def caseAccessControl(self) -> dict :
        datas = self.coll.find({"vulname": "Broken Access Control"})
        if datas.count() < 1 :
            datas = {
                {
                    "vulname" : None,
                    "Type" : None,
                    "adminpage_Destination" : None,
                    "adminpage_Info" : None,
                    "adminpage_Success" : 0,
                    "adminpage_Fail" : 0
                },
                {
                    "vulname" : None,
                    "Type" : None,
                    "dictpage_Destination" : None,
                    "dictpage_Info" : None,
                    "dictpage_Success" : 0,
                    "dictpage_Fail" : 0
                },
                {
                    "vulname" : None,
                    "Type" : None,
                    "logincount_TargetPage" : None,
                    "logincount_Count" : None,
                    "logincount_Policy" : 0,
                    "logincount_Time" : 0
                }
            }
        return datas
    def craftAccessControl(self, datas) -> dict :
        admin_shape = {
            "adminpage_Destination" : None,
            "adminpage_Info" : None,
            "adminpage_Success" : 0,
            "adminpage_Fail" : 0
        }
        login_shape = {
            "logincount_TargetPage" : None,
            "logincount_Count" : None,
            "logincount_Policy" : 0,
            "logincount_Time" : 0
        }
        dict_shape = {
            "dictpage_Destination" : None,
            "dictpage_Info" : None,
            "dictpage_Success" : 0,
            "dictpage_Fail" : 0
        }
        dict_table = []
        admin_table = []
        login_chart = []
        for data in datas :
            if data["Type"] != None :
                if data["Type"] == "dictpage" :
                    dict_shape["dictpage_Destination"] = data["dictpage_Destination"]
                    dict_shape["dictpage_Info"] = data["dictpage_Info"]
                    dict_shape["dictpage_Success"] = data["dictpage_Success"]
                    dict_shape["dictpage_Fail"] = data["dictpage_Fail"]
                    dict_table.append(dict_shape)
                elif data["Type"] == "logincount" :
                    login_shape["logincount_TargetPage"] = data["logincount_TargetPage"]
                    login_shape["logincount_Count"] = data["logincount_Count"]
                    login_shape["logincount_Policy"] = data["logincount_Policy"]
                    login_shape["logincount_Time"] = data["logincount_Time"]
                    login_chart.append(login_shape)
                elif data["Type"] == "adminpage" :
                    admin_shape["adminpage_Destination"] = data["adminpage_Destination"]
                    admin_shape["adminpage_Info"] = data["adminpage_Info"]
                    admin_shape["adminpage_Success"] = data["adminpage_Success"]
                    admin_shape["adminpage_Fail"] = data["adminpage_Fail"]
                    admin_table.append(admin_shape)
        if len(dict_table) < 1 : 
            dict_table.append(dict_shape)
        if len(login_chart) < 1 :
            login_chart.append(login_shape)
        if len(admin_table) < 1 : 
            admin_table.append(admin_shape)
        return {"dict_table" : dict_table, "admin_table" : admin_table, "login_chart" : login_chart}
    def caseInjection(self) -> dict :
        datas = self.coll.find({"vulname": "Injection"})
        if datas.count() < 1 :
            datas = {
                "Page_URL" : None,
                "Vulname" : None,
                "Method" : None,
                "Parameters" : None,
                "Suspicious Parameters" : None,
                "Payload" : None
            }
        return datas
    def craft(self, datas) -> dict : 
        pass
    def caseXSS(self) -> dict :
        datas = self.coll.find({"vulname": "XSS"})
        if datas.count() < 1 :
            datas = {
                "vulname" : None,
                "method" : None,
                "url" : None,
                "isHack" : None, 
                "totalHack" : None,
                "XssType" : None,
                "hackCode" : None,
                "timpestamp" : None
            }
        return datas
    def craftXSS(self, datas) -> dict : 
        chartTotcnt = {
            "tot_try" : 0,
            "tot_success" : 0 
        }
        chartClassification = {
            "stored" : 0,
            "reflect" : 0
        }
        tableRes = []
        res = {
            "method" : None,
            "URL" : None,
            "Total Attack" : None,
            "Succeed Attack" : None,
            "Attack Code" : None
        }
        for data in datas : 
            if data["vulname"] != None :
                chartTotcnt["tot_try"] += data["totalHack"]
                if data["isHack"] :
                    if data["XssType"] == " Stored" : chartClassification["stored"]+=1
                    else : chartClassification["reflect"]+=1
                    res["method"] = data["method"]
                    res["URL"] = data["url"]
                    res["Total Attack"] = data["totalHack"]
                    res["Attack Code"] = data["hackCode"]
                    res["Succeed Attack"] = len(data["hackCode"])
                    chartTotcnt["tot_success"] = res["Succeed Attack"]
            tableRes.append(res)
        return {"charTotcnt" : chartTotcnt, "charClassification" : chartClassification, "tableRes" : tableRes}
                
    def caseXXE(self) -> dict :
        datas = self.coll.find({"vulname": "XXE"})
        if datas.count() < 1 :
            datas = {
                "type" : None,
                "detail_type" : None,
                "url" : None,
                "isHack" : None,
                "totUse" : None,
                "content" : None
            }
        return datas
    def craftXXE(self, datas) -> dict : 
        pass
    def caseAuthentication(self) -> dict :
        data = self.coll.find({"vulname": "Broken Authentication"})
        if len(data) < 1 :
            data = {
                "vulname" : None,
                "accesstime" : None,
                "name" : None,
                "value" : None,
                "sourceIP" : None,
                "loginIP" : None,
                "max-age" : None,
                "expires" : None,
                "secure" : None,
                "discard" : None,
                "httponly" : None,
                "samesite" : None
            }
        return data
    def craftAuthentication(self, data) -> dict :
        table = {
            "Session ID" : data["value"],
            "Source IP" : data["sourceIP"],
            "Logined IP" : data["loginIP"],
            "Secure" : data["secure"],
            "Discard" : data["discard"],
            "HTTP Only" : data["httponly"],
            "samesite" : data["samesite"]
        }
        chart = {
            "Standard" : 600,
            "Target" : data["max-age"],
            "Expires" : data["expires"]
        }
        return {"table" : table, "chart" : chart}
    def searchDB(self) -> dict :
        data = {
            "XXE" : self.craftXXE(self.caseXXE()),
            "Injection" : self.craftInjection(self.caseInjection()),
            "XSS" : self.craftXSS(self.caseXSS()),
            "Authentication" : self.craftAuthentication(self.caseAuthentication()),
            "AccessControl" : self.craftAccessControl(self.caseAccessControl())
        }
        return data

    def testSample(self) :
        print(2)
        self.coll.find_one(filter={'valname':"XXE"}, no_cursor_timeout=False)
        print(3)
        return None