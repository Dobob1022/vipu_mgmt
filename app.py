from crypt import methods
from encodings import utf_8
from wsgiref.util import request_uri
from flask import Flask, render_template, request, Response, session, redirect # flask module
from module import ssh
import os
import logging
import json



#2022-04-20 Starting Devoloping
# By Dobob(dobob@dobob.kr)
# WHERE IS MY WATER :3

##logging
logging.basicConfig(filename='./log/example.log', encoding='utf-8', level=logging.ERROR)

##flask
app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def main():
        return render_template("index.html")

@app.route("/ex_test",methods=["GET","POST"])
def external():
    if request.method == "GET":
        if 'login_status' in session:
            return redirect("/command")
        else:
            return render_template('ext.html')
    else:
        if request.method == "POST":
            if 'login_status' in session:
                return redirect("/vipu")
            else:
                request.form.get('ext_1') == 'ext_1'
                hostname = request.form["hostname"]
                id = request.form["id"]
                password = request.form["password"]
                ssh_result = ssh.connect(hostname,id,password) #if successfully login, Return None
                if ssh_result == None:
                    session['login_status'] = True
                    return redirect("/vipu")
                else: #ssh login error expection.
                    logging.error(f"SSH:{ssh_result}")
                    return render_template('ext.html',err = ssh_result)
        else:
            return Response("Method is not allowed!",status=405)

@app.route("/command", methods = ['GET','POST'])
def command():
    if 'login_status' in session:
        if request.method == "GET":
            return render_template("command.html")
        elif request.method == "POST":
            if 'login_status' in session:
                request.form.get('send') == "send"
                command = request.form['command']
                exec = ssh.exe_command_return(command)
                if exec[0] == False:
                    logging.error(exec[1])
                    return render_template('command.html',err = exec[1])
                else:
                    result = [w.replace('\n','<p>') for w in exec]
                return render_template('command.html',value = result)
            else:
                return Response("NOT OK",status=500)
        else:
            return Response("Method is not allowed!",status=405)
    else:
        return redirect("/ex_test")

    

# @app.route("/vipu", methods = ['GET','POST'])
# def vipu():
#     if 'login_status' in session:
#         if request.method == "GET":
#             return render_template("vipu.html")
#         elif request.method == "POST":
#             if 'login_status' in session:
#                 partition_name = request.form['partition_name']
#                 size = request.form['size']
#                 size = int(size)
#                 command = f"vipu-admin create partition {partition_name} --size {size}"
#                 exec = ssh.exe_command_return(command)
#                 ssh.close()
#                 if exec[0] == False:
#                     logging.error("exec",{exec[1]})
#                     return render_template('vipu.html',err = exec[1].decode('utf-8'))
#                 else:
#                     result = [w.replace('\n','<p>') for w in exec]
#                 return render_template('vipu.html',value = result)
#             else:
#                 return Response("NOT OK",status=500)
#         else:
#             return Response("Method is not allowed!",status=405)
#     else:
#         return redirect("/ex_test")

@app.route("/vipu", methods = ['GET','POST'])
def vipu():
    if 'login_status' in session:
        if request.method == "GET":
            return render_template("vipu.html")
        elif request.method == "POST":
            if 'login_status' in session:
                # command = f"vipu-admin {clr} {pac}"
                # exec = ssh.exe_command_return(command)
                # ssh.close()
                # if exec[0] == False:
                #     logging.error("exec",{exec[1]})
                #     return render_template('vipu.html',err = exec[1].decode('utf-8'))
                # else:
                #     result = [w.replace('\n','<p>') for w in exec]
                return render_template('vipu.html',value = result)
            else:
                return Response("NOT OK",status=500)
        else:
            return Response("Method is not allowed!",status=405)
    else:
        return redirect("/ex_test")



    

@app.route("/exec",methods=["GET","POST"])
def jsontest():
    # if 'login_status' in session:
        if request.method=="GET":
            info = request.args.to_dict()
            print(info)
            # data = json.loads(str(info))
            clr = info['clr_checkbox']
            pac = info['pac_checkbox']
            print("clr:",clr)
            print("pac",pac)
            return info
    # else:
    #     return "not loggined!"
    



##flask
if __name__ == "__main__":
    app.run(debug=True, host = '127.0.0.1')