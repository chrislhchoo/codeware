import paramiko
import paras as pr


username = pr.id
password = pr.pwd
hostname = pr.ip
port = 22
if __name__=='__main__':
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=pr.ip, port=22, username=pr.id, password=pr.pwd)
        print(list)
        # sftp.put("/home/***/py_test/from/1.txt", "/home/***/py_test/to/1.txt")
        # sftp.get("/home/***/py_test/to/2.txt", "/home/***/py_test/from/2.txt")
        t.close()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except:
            pass