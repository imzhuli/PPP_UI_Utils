from components.remote_run import remote_run
from queue import Queue

q = Queue()


remote_run(q, remote_python_script="/home/ubuntu/Tmp/hw.py")
