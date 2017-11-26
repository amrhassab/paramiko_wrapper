import paramiko
import atexit


class SshClient:

    def __init__(self, host, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        atexit.register(client.close)
        self.client = client
        self.user = user
        self.password = password

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command):
        feed_password = False
        sudo = command.strip().split()[0]
        if sudo == 'sudo' and self.user != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()

        return {'out': stdout.read(),
                'err': stderr.read(),
                'retval': stdout.channel.recv_exit_status()}

