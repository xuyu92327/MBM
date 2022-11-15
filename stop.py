import paramiko
from paramiko import SSHClient
from paramiko import AutoAddPolicy

from MySSHClient import MySSHClient, console

host = '192.168.10.16'
username = 'root'
password = 'centos'

trans = paramiko.Transport((host, 22))
trans.connect(username=username, password=password)
ssh = MySSHClient()
ssh._transport = trans
ssh.set_missing_host_key_policy(AutoAddPolicy())
sftp = paramiko.SFTPClient.from_transport(trans)

ssh.run('cd /root', console)
ssh.run('./stop.sh', console)





