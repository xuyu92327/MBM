from paramiko import SSHClient
from itertools import zip_longest

class MySSHClient(SSHClient):
    def run(self, command, callback):
        stdin, stdout, stderr = self.exec_command(command, bufsize=1)

        stdout_iter = iter(stdout.readline, '')
        stderr_iter = iter(stderr.readline, '')

        for out, err in zip_longest(stdout_iter, stderr_iter):
            if out: callback(out.strip())
            if err: callback(err.strip())

        return stdin, stdout, stderr

def console(text):
    print(text)
