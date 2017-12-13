import paramiko

paramiko.util.log_to_file("../io/paramiko.log")


class SshClient:

    # __init__:
    # constructs an ssh handle that can be used to send commands
    #
    # @arg host: the host IP address
    # @arg user: the username for log in
    # @arg password: the password for log in and sudo commands
    def __init__(self, host, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        self.client = client
        self.user = user
        self.password = password

    # close:
    # call when done
    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    # execute:
    # IMPORTANT: for bash scripts to keep running after returning use "nohup" before the commands!
    # executes a bash command
    #
    # @arg command: the command you want to execute
    #
    # @return: dictionary with retval, stdout, stderr of the sent command
    def execute(self, command):
        feed_password = False
        sudo = command.strip().split()[0]
        if sudo == 'sudo' and self.user != "root":
            command = "sudo -S -p ' ' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()

        return {'retval': stdout.channel.recv_exit_status(),
                'out': bytes.decode(stdout.read()),
                'err': bytes.decode(stderr.read())
                }

