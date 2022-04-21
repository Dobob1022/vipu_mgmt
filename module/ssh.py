import paramiko
from paramiko.py3compat import input
client = paramiko.SSHClient()
def connect(host,id,pw):
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    try:
        client.connect(host,22,id, pw)
    except Exception as e:
        return str(e)
def exe_command_no_return(command):
        client.exec_command(command)
        return True

def exe_command_no_return(command):
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.readlines()
        if len(output) == 0:
            result = stderr.read()
            return result
        else:
            return True
        
def exe_command_return(command):
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.readlines()
        if len(output) == 0:
            result = stderr.read()
            return False,result
        else:
            return output
        
def test(command):
    try:
        stdin, stdout, stderr = client.exec_command(command)
        a = stdout.read()
        if len(a) == 0:
            result = stderr.read()
            print("stderr:",result)
            return str(result)
        else:
            print(stdout.read())
            return "FUW"
    except Exception as e:
        return str(e)

def close():
    try:
        client.close()
        return True
    except Exception as e:
        return str(e)