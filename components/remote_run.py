import os
import paramiko
import time
import shlex
import select
import sys
from queue import Queue
from pathlib import PurePosixPath

class RemoteOutput:
    def __init__(self, out=None, exit_code=None):
        self.out = out
        self.exit_code=exit_code


def pick_name(src_filename):
    path = PurePosixPath(src_filename)
    return path.name

def pick_path(src_filename):
    path = PurePosixPath(src_filename)
    return str(path.parent)


def pick_path_quoted(src_filename):
    return shlex.quote(pick_path(src_filename))



def remote_run(poster, remote_python_script = "", remote_host = "zhuli.cool", remote_port=22, remote_user = "ubuntu", rsa_key_path=os.path.expanduser("~/.ssh/id_rsa")):

    command = shlex.split(remote_python_script)
    script_path = command[0]
    params = command[1::]
    for i,v in enumerate(params):
        params[i] = shlex.quote(v)

    remote_dir = pick_path_quoted(script_path)
    remote_name = pick_name(script_path)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(rsa_key_path)
    ssh.connect(remote_host, port=remote_port, username=remote_user, pkey=private_key)

    transport = ssh.get_transport()
    channel  = transport.open_session()
    channel .get_pty()  # 分配伪终端（某些命令需要）

    channel.exec_command(f"cd {remote_dir} && python3 {remote_name} {" ".join(params)}")

    undecoded = b""
    while True:
        # 使用 select 检查是否有数据可读
        rlist, _, _ = select.select([channel], [], [], 0.1)
        if channel in rlist:
            output = channel.recv(1024)
            if not output:
                break
            undecoded += output
            try:
                decoded = undecoded.decode('utf-8')
                undecoded = b""
                text = RemoteOutput(decoded)
                poster(text)
            except UnicodeDecodeError:
                continue

    
    # 获取退出状态码
    exit_status = channel.recv_exit_status()
    poster(RemoteOutput(exit_code=exit_status))
    pass
