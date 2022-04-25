import paramiko
from paramiko.py3compat import input
client = paramiko.SSHClient()
def connect(host,id,pw):
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    try:
        client.connect(hostname=host,port=22,username=id, password=pw, timeout=5)
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
        

def close():
    try:
        client.close()
        return True
    except Exception as e:
        return str(e)