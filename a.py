import json
import requests
import keyboard
import webbrowser
import time
import datetime
import difflib
from urllib import parse
import re
import pyperclip
import os

set = {
    "uid": "P1024",  #自动记录当前的题号（自动填写，可以 不用管它）
    "judge_record": 58010375, #自动记录当前题交后，查看结果网页的数字 例如：https://www.luogu.com.cn/record/58010375 就对应着提交后的结果（自动填写，可以 不用管它）
    "file": "D:\\All Code\\VS Code\\",
                                            #'''
                                            # 写代码文件存放的目录 改目录下需要创建的文件有 ： 
                                            # a.cpp （在这个文件下编码） 
                                            # ac_write.out （当前输入 正确答案存放文件 自动填写，可以 不用管它）
                                            # read.in （重定向读入文件 当前输入数据的文件  自动填写，可以 不用管它）
                                            # write.out （重定向输出的文件 你的程序重定向输出到这个文件里，才能和正确输出进行对比判断）
                                            # 模板.cpp   （每次写新题的时候，自动初始化a.cpp的代码）
                                            #'''
    "x-csrf-token": "163170236:YVYi6QXLoFmmZynrwIkKodqeta8Wqz08=", #洛谷提交的时候需要的数据 （自动填写，可以 不用管它）
    "cookie":"UM_distinctid=179d7706cbc8c89e62a0e57-51361542-TA5476811=cnzz_e059-1622812186-https%3A%2F%2Fwww.baidu.7433792; __client_id=96abea40e8e5c276d176f81200",#你的账号在洛谷网站中的 cookie 
    "enableO2": 1, #是否开 O2 ： 1 开  0 关  （该项 填写不要带引号）
    "lang": 4,#提交代码的语言 默认 ：4 C++
    "clear": "f1",#清空 a.cpp read.in write.out 文件 的快捷键
    "init": "f2", # 初始化a.cpp 的快捷键
    "check": "f3",# 检查输出是否和答案一直 的快捷键
    "submit": "f4",# 把 a.cpp 中保存的代码提交到洛谷 的快捷键
    "ans": "f6",# 查看该题在洛谷中题解  的快捷键
    "detailed_report": "f7",# 查看输出和答案比较直观，详细的差别  的快捷键
    "judge_web": "f8",# 在浏览器中打开提交代码的运行情况  的快捷键
    "last_init_time": "2021-09-14 18:33:56.906528", #你初始化a.cpp的时间，一般即开始写该题的时间 （自动填写，可以 不用管它）
    "head_diy": "hello world!\n\nJust do it!\n\nstart time:", #每次在初始化a.cpp时，插入到开头的文字 ——DIY
    "work": 1,#当前使用是否是洛谷平台 1 ：是  0 ：不是 （该项 填写不要带引号） 不是的话，只能使用清空代码和初始化代码的功能
    "vscode": 1 # 是否在 vs code 上使用该插件 1 ：是  0 ：不是 （该项 填写不要带引号） 不是的话，会把测试样例输入读取到粘贴版中
}

ac_output = ""
my_out = ""

acin = []
acout = []

order = 0


def if_exist():
    k={
        "uid": "UVA1395",
        "judge_record": 58118910,
        "file": "D:\\All Code\\VS Code\\",
        "x-csrf-token": "1631419:9ViX9GaVJ0kzJq2E85tEOdv45OcHw=",
        "cookie": "UM_distinctid=179dbc89d7706cbde=16276e49abe8e5c276d176f8120e27cfm.cn/prob432480",
        "enableO2": 1,
        "lang": 4,
        "clear": "f1",
        "init": "f2",
        "check": "f3",
        "submit": "f4",
        "ans": "f6",
        "detailed_report": "f7",
        "judge_web": "f8",
        "last_init_time": "2021-09-16 18:43:39.368601",
        "head_diy": "hello world!\n\nJust do it!\n\nstart time:",
        "work": 1,
        "vscode": 1
    }
    if os.path.exists('D:\\code_setting.json')==False :
        with open(set["file"] + "write.out", "w",encoding='utf-8') as f:
            json.dump(k, f, indent=1)

if_exist()

def setting():
    global set
    with open('D:\\code_setting.json', 'w',encoding='utf-8') as f:
        json.dump(set, f, indent=1)


def read():
    global set
    with open('D:\\code_setting.json', 'r',encoding='utf-8') as f:
        set = json.load(f)


def no_vscode(s,flag=0):
    global set
    read()
    # if set["vscode"]==0 :
    print("\n\n"+str(s)+"\n\n")
    if flag == 1 and set["vscode"]==0:
        pyperclip.copy(str(s))

def write_str(s):
    global set
    with open(set["file"] + "write.out", "w",encoding='utf-8') as f:
        no_vscode(str(s))
        f.write(str(s))



	# "0": {
	# 							"id": 0,
	# 							"status": 5,
	# 							"time": 1200,
	# 							"memory": 624,
	# 							"score": 0,
	# 							"signal": 0,
	# 							"exitCode": 0,
	# 							"description": None,
	# 							"subtaskID": 0,
	# 							"__CLASS_NAME": "Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult"
	# 						},



def get_result(num, tim=0):
    read()
    global set

    headers2 = {
        #"authority": "www.luogu.com.cn",
        #"method": "GET",
        #"path": "/problem/UVA10900",
        "scheme":
        "https",
        "accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "accept-encoding": "gzip, deflate, br",
        "accept-language":
        "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control":
        "max-age=0",
        "cookie":
        set["cookie"],
        "sec-ch-ua":
        "\"Microsoft Edge\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
        "sec-ch-ua-mobile":
        "?0",
        "sec-ch-ua-platform":
        "\"Windows\"",
        "sec-fetch-dest":
        "document",
        "sec-fetch-mode":
        "navigate",
        "sec-fetch-site":
        "none",
        "sec-fetch-user":
        "?1",
        "upgrade-insecure-requests":
        "1",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38"
    }
    #a=requests.get("https://www.luogu.com.cn/problem/UVA10900",headers=headers2)

    a = requests.get("https://www.luogu.com.cn/record/" + str(num),
                     headers=headers2)

    # print(a)
    ## print(a.content)
    b = a.text

    #g="<meta name=\"csrf-token\" content=\""

    #if g in b :

    #    b1=b.index(g)+len(g)
    #    # print(b1)
    #    b2=b.index("\"",b1)
    #    # print(b2)
    #    # print(b[b1:b2])

    g = "JSON.parse(decodeURIComponent(\""

    if g in b:

        b1 = b.index(g) + len(g)
        # print(b1)
        b2 = b.index("\"));", b1)
        # print(b2)
        # # print(b[b1:b2])
        js2 = b[b1:b2]
        js = parse.unquote(js2)

        info = json.loads(js)

        # print(info)
        ## print(json.dumps(info, indent=4))

        if info["code"] == 200:

            record = info["currentData"]["record"]

            judgeResult=record["detail"]["judgeResult"]
            ## print(judgeResult)

            t=json.dumps(judgeResult,indent=1)
            
            #t=t.replace("\"__CLASS_NAME\": \"Luogu\\\\DataClass\\\\Record\\\\JudgeResult\\\\TestCaseJudgeResult\"","")

            #h1="\"__CLASS_NAME\": \"Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult\""
            
            #ret = re.sub(r'[0-9a-zA-Z ]+?', "", s)

            statu = {
                0: "Waiting",
                1: "Judging",
                2: "Compile Error",
                3: "Output Limit Exceeded",
                4: "Memory Limit Exceeded",
                5: "Time Limit Exceeded",
                6: "Wrong Answer",
                7: "Runtime Error",
                11: "Unknown Error",
                12: "Accepted",
                14: "Unaccepted",
            }
            statu2 = {
                2: "CE",
                3: "OLE",
                4: "MLE",
                5: "TLE",
                6: "WA",
                7: "RE",
                11: "UE",
                12: "AC",
                14: "WA"
            }

            

            status = record["status"]
            
            ## print(statu[status])

            if status == 0:
                # print("Waiting")
                write_str("Waiting!\n\n" + str(tim) + " s\n\nPlease Wait!")
                time.sleep(0.5)
                get_result(num, tim + 0.5)
                return

            if status == 1:
                write_str("Judging!\n\n" + str(tim) + " s\n\nPlease Wait!")
                time.sleep(0.5)
                get_result(num, tim + 0.5)
                return

            submitTime = time.ctime(record["submitTime"])

            enableO2 = record["enableO2"]

            ranking = info["currentUser"]["ranking"]

            compileResult = record["detail"]["compileResult"]
            success = compileResult["success"]

            score = "null"
            if "score" in record:
                score = record["score"]
            fullScore = record["problem"]["fullScore"]

            sta = ""
            sta2=""
            time_1_struct = datetime.datetime.strptime(set["last_init_time"], "%Y-%m-%d %H:%M:%S.%f")
            time_2_struct = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            seconds2 = (time_2_struct - time_1_struct).seconds
            sta +=  "\n\nSubmit Time : \n" + str(
                submitTime
            ) + "\n\nWait Time : " + str(tim) + " s\n\nSpend Time : "+ str(round(seconds2/60,2)) +" mins\n\nScore : " + str(
                score) + "\nFull Score : " + str(
                    fullScore) + "\n\nEnable O2 : " + str(
                        enableO2) + "\n\nRanking : " + str(ranking) + "\n\n"

            if success == False:
                status=2
                h = statu2[status]
                sta2 += h + " !\n" + h + " ! !\n" + h + " ! ! !\n"
                sta2+="Statu : " + statu[status] 
                sta=sta2+sta
                message = compileResult["message"]
                sta += message

            else:
                b=re.sub(r'"__CLASS_NAME".*?lt"',"",t)
                g="\"status\": "
                b1=0
                status_last=12
                while g in b[b1:] :
                    
                    b1 = b.index(g,b1) + len(g)
                    if b[b1].isdigit() :
                        # print(b1)
                        b2 = b.index(",", b1)
                        # print(b2)
                        # print(b[b1:b2])
                        f=int(b[b1:b2])
                        if f!=12 :
                            status_last=f
                        b=b[:b1]+statu[f]+b[b2:]

            # # print(b)
                all_inf=b
                if status!=12 :
                    status=status_last

                h = statu2[status]
                sta2 += h + " !\n" + h + " ! !\n" + h + " ! ! !\n"
                sta2+="Statu : " + statu[status] 
                sta=sta2+sta
                
                tim = record["time"]

                memory = record["memory"]

                sta += "time : " + str(tim) + "ms\n\nmemory : " + str(
                    memory) + "KB\n"
                sta+="\nJudgeResult : \n"+all_inf+"\n"
            sta += "\n\n  You can click " + set[
                "judge_web"] + " for getting \nmore detailed information.\n"
            sta += "Click " + set[
                "ans"] + " for getting \nthis problem's solutions.\n"
            # print(sta)
            write_str(sta)


#httpURL测试地址
def submit():
    global set
    read()
    httpURL = "https://www.luogu.com.cn/fe/api/problem/submit/" + set["uid"]
    #requests中的请求参数，请求头等都是采用字典方式存储

    with open(set["file"] + "a.cpp", "r",encoding='utf-8') as f:  # 打开文件
        my_code = f.read()  # 读取文件
    # # print(my_code)

    #body接口参数

    body = {"code": my_code, "enableO2": set["enableO2"], "lang": set["lang"]}
    #headers请求头
    headers = {
        "accept-encoding": "gzip, deflate, br",
        #"accept-language":" zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-length": "2036",
        "content-type": "application/json;charset=UTF-8",
        "cookie": set["cookie"],
        "origin": "https://www.luogu.com.cn",
        "referer": "https://www.luogu.com.cn/problem/UVA1636",
        "sec-ch-ua":
        "\"Microsoft Edge\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
        "x-csrf-token": set["x-csrf-token"],
        "x-requested-with": "XMLHttpRequest"
    }

    #发送post请求
    response_post = requests.post(httpURL,
                                  headers=headers,
                                  data=json.dumps(body))  #进行登录
    #cks=requests.utils.dict_from_cookiejar(response_post.cookies)  #保存cookie

    # print(response_post)

    #响应结果解析
    # print(response_post.content)  #以字节格式返回响应内容
    # print("text:" + response_post.text)  #以文本格式返回响应内容
    num = json.loads(response_post.text)
    num2 = num['rid']
    # print(num['rid'])

    set["judge_record"] = num2
    setting()

    get_result(num2)

    #webbrowser.open("https://www.luogu.com.cn/record/"+str(num2), new=2, autoraise=True)


def luogu():
    global acin
    global acout
    global set
    read()

    headers2 = {
        #"authority": "www.luogu.com.cn",
        #"method": "GET",
        #"path": "/problem/UVA10900",
        "scheme":
        "https",
        "accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "accept-encoding": "gzip, deflate, br",
        "accept-language":
        "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control":
        "max-age=0",
        "cookie":
        set["cookie"],
        "sec-ch-ua":
        "\"Microsoft Edge\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
        "sec-ch-ua-mobile":
        "?0",
        "sec-ch-ua-platform":
        "\"Windows\"",
        "sec-fetch-dest":
        "document",
        "sec-fetch-mode":
        "navigate",
        "sec-fetch-site":
        "none",
        "sec-fetch-user":
        "?1",
        "upgrade-insecure-requests":
        "1",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38"
    }
    a = requests.get("https://www.luogu.com.cn/problem/" + set["uid"],
                     headers=headers2)
    # print(a)
    # print(a.text)
    b = a.text

    # g="[PDF]("
    # if set["uid"][0:3] == "UVA" and g in b:
    #     b1 = b.index(g) + len(g)
    #     # print(b1)
    #     b2 = b.index(")", b1)
    #     # print(b2)
    #     # print(b[b1:b2])
    #     webbrowser.open(b[b1:b2],
    #                     new=2,
    #                     autoraise=True)

    g = "<meta name=\"csrf-token\" content=\""

    if g in b:

        b1 = b.index(g) + len(g)
        # print(b1)
        b2 = b.index("\"", b1)
        # print(b2)
        # print(b[b1:b2])
        set["x-csrf-token"] = b[b1:b2]
        setting()

    for num in range(5):

        g = "<h3>输入样例 #" + str(num + 1) + "</h3>\n<pre><code>"

        if g in b:

            b1 = b.index(g) + len(g)
            # print(b1)
            b2 = b.index("</code></pre>", b1)
            # print(b2)
            # print(b[b1:b2])
            acin.append(b[b1:b2])

            g = "<pre><code>"
            b1 = b.index(g, b2) + len(g)
            # print(b1)
            b2 = b.index("</code></pre>", b1)
            # print(b2)
            i = b[b1:b2]
            if i[len(i) - 1] != '\n':
                i = i + "\n"
            acout.append(i)
    if len(acin) > 0:
        with open(set["file"] + "read.in", "w",encoding='utf-8') as f:
            no_vscode(acin[0],1)
            f.write(acin[0])
        with open(set["file"] + "ac_write.out", "w",encoding='utf-8') as f:
            #print(acout[0])
            f.write(acout[0])




def debug2(problem_nid, input_nid):
    global acin
    global acout
    global set
    httpURL = "https://www.udebug.com/udebug-custom-get-selected-input-ajax"

    body = {"input_nid": input_nid}
    #headers请求头
    headers = {
        'Referer': 'https://www.luogu.com.cn/auth/login',
        'Origin': 'https://www.luogu.com.cn',
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.421.0 Safari/537.36",
        "Accept": "*/*",
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrf-token': ''
    }
    #发送post请求
    response_post = requests.post(httpURL, headers=headers, data=body)  #进行登录
    #cks=requests.utils.dict_from_cookiejar(response_post.cookies)  #保存cookie

    ## print(response_post.text)

    ##响应结果解析
    ## print(response_post.content)#以字节格式返回响应内容
    ## print("text:"+response_post.text)#以文本格式返回响应内容
    k = json.loads(response_post.text)
    ## print(k["input_value"])

    h = k["input_value"]

    body2 = {
        "problem_nid": problem_nid,
        "input_data": h,
        "node_nid": "",
        "op": "Get Accepted Output",
        "output_data": "",
        "user_output": "",
        "form_id": "udebug_custom_problem_view_input_output_form"
    }

    url2 = "https://www.udebug.com/UVa/" + set["uid"][3:]

    response_post = requests.post(url2, headers=headers, data=body2)  #进行登录
    #cks=requests.utils.dict_from_cookiejar(response_post.cookies)  #保存cookie

    ## print(response_post.text)

    ##响应结果解析

    b = response_post.text

    b1 = b.index("class=\"form-textarea\">") + len("class=\"form-textarea\">")
    ## print(b1)
    b2 = b.index("</textarea></div>", b1)
    ## print(b2)
    ## print(b[b1:b2])
    input = b[b1:b2]

    b1 = b.index("class=\"form-textarea\">",
                 b1) + len("class=\"form-textarea\">")
    ## print(b1)
    b2 = b.index("</textarea></div>", b1)
    ## print(b2)
    ## print(b[b1:b2])
    output = b[b1:b2]

    ## print(input)
    ## print(output)
    acin.append(input)
    acout.append(output)


def uva():
    global set
    headers = {
        'Referer': 'https://www.luogu.com.cn/auth/login',
        'Origin': 'https://www.luogu.com.cn',
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.421.0 Safari/537.36",
        "Accept": "*/*",
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrf-token': ''
    }

    a = requests.get("https://www.udebug.com/UVa/" + set["uid"][3:])
    ## print(a.text)

    b = a.text

    if "\"problem_nid\" value=\"" in b:

        b1 = b.index("\"problem_nid\" value=\"") + len(
            "\"problem_nid\" value=\"")
        ## print(b1)
        b2 = b.index("\"", b1)
        ## print(b2)
        # print(b[b1:b2])
        problem_nid = b[b1:b2]

        b1 = 0

        for i in range(5):
            if "data-id=\"" in b[b1:]:

                b1 = b.index("data-id=\"", b1) + len("data-id=\"")
                ## print(b1)
                b2 = b.index("\"", b1)
                ## print(b2)
                # print(b[b1:b2])
                input_nid = b[b1:b2]
                debug2(problem_nid, input_nid)
                b1 = b.index("data-id=\"", b1) + len("data-id=\"")


def write():
    global set
    global acin
    global acout
    read()
    luogu()
    if set["uid"][0:3] == "UVA":
        uva()
    if len(acin) > 0:
        with open(set["file"] + "read.in", "w",encoding='utf-8') as f:
            no_vscode(acin[0],1)
            f.write(acin[0])
        with open(set["file"] + "ac_write.out", "w",encoding='utf-8') as f:
            #print(acout[0])
            f.write(acout[0])

    #try:

    #    headers2 = {
    #        'Referer': 'https://www.luogu.com.cn/auth/login',
    #        'Origin': 'https://www.luogu.com.cn',
    #        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.421.0 Safari/537.36",
    #        "Accept": "*/*",
    #        'Connection': 'keep-alive',
    #        'x-requested-with': 'XMLHttpRequest',
    #        'x-csrf-token':''
    #    }
    #    a=requests.get("https://www.luogu.com.cn/problem/"+set["uid"],headers=headers2)
    #    # print(a)
    #    # print(a.text)
    #    b=a.text
    #    b1=b.index("<h3>输入样例 #1</h3>\n<pre><code>")+len("<h3>输入样例 #1</h3>\n<pre><code>")
    #    # print(b1)
    #    b2=b.index("</code></pre>\n<h3>输出样例 #1</h3>")
    #    # print(b2)
    #    # print(b[b1:b2])

    #    with open(set["file"]+"read.in","w") as f:
    #        f.write(b[b1:b2])

    #    # print("\n\noutput:\n\n")
    #    b1=b.index("<h3>输出样例 #1</h3>\n<pre><code>")+len("<h3>输出样例 #1</h3>\n<pre><code>")
    #    # print(b1)
    #    b2=b.index("</code></pre>",b1)
    #    # print(b2)
    #    # print(b[b1:b2])
    #    global ac_output
    #    ac_output=b[b1:b2]+"\n"
    #    with open(set["file"]+"ac_write.out","w") as f:
    #        f.write(ac_output)

    #except:
    #    pass


def init():
    global set
    global order
    global acin
    global acout
    acin.clear()
    acout.clear()
    order = 0

    read()
    set["last_init_time"] = str(datetime.datetime.now())
    setting()
    time.sleep(1)
    with open(set["file"] + "a.cpp", "r",encoding='utf-8') as f:  # 打开文件

        k = f.read().upper().replace(" ","").replace("\n","")  # 读取文件
        if len(k) < 15 and len(k) > 2:
            set["uid"] = k
            setting()
        #if set["uid"][0:3] == "UVA" :
        #webbrowser.open("https://www.udebug.com/UVa/"+set["uid"][3:], new=2, autoraise=True)
        #webbrowser.open("https://uva.onlinejudge.org/external/16/p"+set["uid"][3:]+".pdf", new=2, autoraise=True)

        webbrowser.open("https://www.luogu.com.cn/problem/" + set["uid"],
                        new=2,
                        autoraise=True)
    with open(set["file"] + "模板.cpp", "r",encoding='utf-8') as f:  # 打开文件
        k1 = f.read()  # 读取文件
    with open(set["file"] + "a.cpp", "w",encoding='utf-8') as f:
        no_vscode("/*\n\n" + set["head_diy"] + str(datetime.datetime.now()) +
                "\n\n*/\n\n" + k1)
        f.write("/*\n\n" + set["head_diy"] + str(datetime.datetime.now()) +
                "\n\n*/\n\n" + k1)
    write()


def clear():
    global order
    order = 0
    with open(set["file"] + "a.cpp", "w",encoding='utf-8') as f:
        f.write("")

    with open(set["file"] + "read.in", "w",encoding='utf-8') as f:
        f.write("")

    with open(set["file"] + "write.out", "w",encoding='utf-8') as f:
        f.write("")


def ans():
    global set
    read()
    webbrowser.open("https://www.luogu.com.cn/problem/solution/" + set["uid"],
                    new=2,
                    autoraise=True)


def check():
    global ac_output
    global my_out
    global set
    global order
    global acin
    global acout

    with open(set["file"] + "write.out", "r",encoding='utf-8') as f:  # 打开文件
        my_out = f.read()  # 读取文件
    with open(set["file"] + "ac_write.out", "r",encoding='utf-8') as f:  # 打开文件
        ac_output = f.read()  # 读取文件

    my_out2 = my_out
    ac_output2 = ac_output
    with open(set["file"] + "write.out", "w",encoding='utf-8') as f:
    

        my_lines=my_out.split("\n")
        ac_lines=ac_output.split("\n")
        diff_content=""
        my_idx=0
        dif_num=0
        for idx in range(len(ac_lines)) :
            dif=""
            ac_line=ac_lines[idx]
            if my_idx+1 <len(my_lines) :
                if my_lines[my_idx]=="" and my_lines[my_idx+1][0:3]=="---" :
                    dif+="\n"+my_lines[my_idx]+"\n"
                    start=my_idx
                    my_idx=my_idx+1
                    while my_lines[my_idx][0:3]=="---" :
                        dif+=my_lines[my_idx]+"\n"
                        my_idx=my_idx+1
                    dif+="\n"
                    my_idx=my_idx+1
                

            if my_idx <len(my_lines) :
                my_line=my_lines[my_idx]
            else :
                my_line="null"
            my_idx=my_idx+1
            if my_line!=ac_line :
                dif_num=dif_num+1
                diff_content+=str(idx+1)+" line : \n"+dif+"\nmy : "+my_line+"\nac : "+ac_line+"\n\n"
                #''.join(difflib.Differ().compare(my_line.splitlines(keepends=True),ac_line.splitlines(keepends=True)))+"\n"




        # diff_content = difflib.Differ().compare(
        #     my_out.splitlines(keepends=True),
        #     ac_output.splitlines(keepends=True))
        if dif_num >0 :
            no_vscode("WA!!!\n\n" +"  The number of differences \nis "+str(dif_num)+" .\nSee the data below.\n\n"+ ''.join(diff_content) + "\n\n" +
                    "My write_out:\n\n" + my_out2 + "\n\nAc write_out:\n\n" +
                    ac_output2)
            f.write("WA!!!\n\n" +"  The number of differences \nis "+str(dif_num)+" .\nSee the data below.\n\n"+ ''.join(diff_content) + "\n\n" +
                    "My write_out:\n\n" + my_out2 + "\n\nAc write_out:\n\n" +
                    ac_output2)
            if len(acin) > 0:
                with open(set["file"] + "read.in", "w",encoding='utf-8') as f:
                    no_vscode(acin[order],1)
                    f.write(acin[order])
                with open(set["file"] + "ac_write.out", "w",encoding='utf-8') as f:
                    #print(acout[order])
                    f.write(acout[order])
        else:
            order = order + 1
            if len(acin) > order:
                no_vscode("All : " + str(len(acin)) + "\n\nAC : " + str(order) +
                        "\n\nContinue!!!\n\n" + my_out2)
                f.write("All : " + str(len(acin)) + "\n\nAC : " + str(order) +
                        "\n\nContinue!!!\n\n" + my_out2)

                with open(set["file"] + "read.in", "w",encoding='utf-8') as f:
                    no_vscode(acin[order],1)
                    f.write(acin[order])
                with open(set["file"] + "ac_write.out", "w",encoding='utf-8') as f:
                    #print(acout[order])
                    f.write(acout[order])
            else:
                no_vscode("AC!!!\n\nCongratulations!\n\n  Please click " +
                        set["submit"] + " for \nsubmitting your code!\n\n" +
                        my_out2)
                f.write("AC!!!\n\nCongratulations!\n\n  Please click " +
                        set["submit"] + " for \nsubmitting your code!\n\n" +
                        my_out2)
                order = 0
                if len(acin) > 0:
                    with open(set["file"] + "read.in", "w",encoding='utf-8') as f:

                        no_vscode(acin[0],1)
                        f.write(acin[0])
                    with open(set["file"] + "ac_write.out", "w",encoding='utf-8') as f:
                       # print(acout[0])
                        f.write(acout[0])


def no_work():
    global set
    with open(set["file"] + "write.out", "w",encoding='utf-8') as f:
        f.write("")
    with open(set["file"] + "read.in", "w",encoding='utf-8') as f:
        f.write("")

    with open(set["file"] + "模板.cpp", "r",encoding='utf-8') as f:  # 打开文件
        k1 = f.read()  # 读取文件
    with open(set["file"] + "a.cpp", "w",encoding='utf-8') as f:
        f.write("/*\n\n" + set["head_diy"] + str(datetime.datetime.now()) +
                "\n\n*/\n\n" + k1)


def detailed_report():
    global ac_output
    global my_out

    # print(ac_output)

    global set
    d = difflib.HtmlDiff()

    htmlContent = d.make_file(ac_output.splitlines(keepends=True),
                              my_out.splitlines(keepends=True))
    # # print(htmlContent)
    with open(set["file"] + 'detailed_report.html', 'w',encoding='utf-8') as f:
        f.write(htmlContent)
    webbrowser.open(set["file"] + 'detailed_report.html',
                    new=2,
                    autoraise=True)


def judge_web():
    global set
    read()
    webbrowser.open("https://www.luogu.com.cn/record/" +
                    str(set["judge_record"]),
                    new=2,
                    autoraise=True)


read()

if set["work"] == 1:
    keyboard.add_hotkey(set["clear"], clear)
    keyboard.add_hotkey(set["init"], init)
    keyboard.add_hotkey(set["submit"], submit)
    keyboard.add_hotkey(set["check"], check)
    keyboard.add_hotkey(set["ans"], ans)
    keyboard.add_hotkey(set["detailed_report"], detailed_report)
    keyboard.add_hotkey(set["judge_web"], judge_web)
    keyboard.wait()
else:
    keyboard.add_hotkey(set["init"], no_work)
    keyboard.wait()
