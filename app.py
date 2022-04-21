from flask import Flask, render_template, request, Response # flask module
from module import ssh
import os
import logging

##logging
logging.basicConfig(filename='./log/example.log', encoding='utf-8', level=logging.ERROR)

##flask
app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def main():
        return render_template("index.html")

@app.route("/test",methods=["GET","POST"])
def test():
    if request.method == "GET":
        return render_template("test.html")
    else:
        if request.form.get('test') == 'test':
            result = os.popen('ls -al')
            output = result.read()
            return output
        if request.form.get("mkdir") == 'mkdir':
            result = os.system('mkdir test')
            print(result)
            if result == 256:
                return "ERROR DIRECOTR IS EXISTED!"
            elif result == 0:
                return "OK!"
            else:
                return "SOMETHING"
        return "FUQS"

@app.route("/ex_test",methods=["GET","POST"])
def external():
    if request.method == "GET":
        return render_template('ext.html')
    else:
        if request.method == "POST":
            request.form.get('ext_1') == 'ext_1'
            hostname = request.form["hostname"]
            id = request.form["id"]
            password = request.form["password"]
            ssh_result = ssh.connect(hostname,id,password)
            if ssh_result == None:
                exec = ssh.exe_command_return("wtf")
                ssh.close()
                if exec[0] == False:
                    logging.error(exec[1])
                    return render_template('ext.html',err = str(exec[1]))
                else:
                    result = [w.replace('\n','<p>') for w in exec]
                    return render_template('ext.html',value = result)
            else:
                logging.error(ssh_result)
                return render_template('ext.html',err = ssh_result)

            

        else:
            return Response("Method is not allowed!",status=405)


    


##flask
if __name__ == "__main__":
    app.run(debug=True, host = '127.0.0.1')