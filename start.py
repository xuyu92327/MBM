import paramiko
from paramiko import SSHClient
from paramiko import AutoAddPolicy

#from MySSHClient import MySSHClient, console

host = '192.168.10.16'
username = 'root'
password = 'centos'

#trans = paramiko.Transport((host, 22))
#trans.connect(username=username, password=password)
#ssh = MySSHClient()
ssh = SSHClient()
#ssh._transport = trans
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(host, username=username, password=password)

stdin, stdout, stderr = ssh.exec_command('./test.sh')

fin = open('muon_test.dat', 'w+')
while True:
    line = stdout.readline()
    if not line:
        break
    print(line, end=" ", flush=True)
    if line[:4] == 'Pack':
        sp_line = line.split()
        fin.write('%s %s %s \n'%(sp_line[5][:-1], sp_line[7][:-1], sp_line[9][:-1]))

fin.close()



