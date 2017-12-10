# paramiko_wrapper
This is a simple Python 3 wrapper class for the [Pramiko](http://www.paramiko.org/) Python library. Paramiko allows your python program to send commands remotly via ssh. Also, it allows you to retrieve their standard error, standard output and return value with ease. The wrapper class [ssh_wrapper.py](ssh_wrapper.py) handles the case of `sudo` commands and makes the overall use more pleasant and clean.

If you want to run bash scripts running after closing the ssh session use `nohup` before your command (only tested on Linux). This stops the process from terminating when paramiko returns. This is because every command sent is its own session that is terminated after paramiko is done executing your command.

For command-line applications and executables a workaround to keep them running after closing the ssh session is to imvoke them in a bash script.

# Usage Example
Change `0.0.0.0`, `myuser` and `mypassword` to you host credentials in the code below. 
```
import SSH_wrapper.sh

host, user, password = ('0.0.0.0', 'myuser', 'mypass')
ssh = SshClient(host, user, password)

tmp = ssh.execute("echo I can accept commands")
print("stdout: " + tmp['out'])
print("stderr: " + tmp['err'])

tmp = ssh.execute("sudo echo I can accept sudo commands")
print("stdout: " + tmp['out'])
print("stderr: " + tmp['err'])
ssh.close()
```

**Output:**
```
stdout: I can accept commands

stderr: 
stdout: avidbeam

I can accept sudo commands

stderr: 

Process finished with exit code 0
```

# Reference
[ssh_wrapper.py](ssh_wrapper.py) was compiled from many open-source blogs and Paramiko docs with a few tweaks and additional functionality added by me.

