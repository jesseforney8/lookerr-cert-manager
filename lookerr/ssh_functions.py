from paramiko import SSHClient

def show_dir(user, password, ip):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=ip, username=user, password=password)

    (stdin, stdout, stderr) = ssh.exec_command("dir")

    cmd_output = str(stdout.read())


    cmd_output = list(cmd_output.split("<DIR>"))



    slash = "\$"
    slash = slash.replace("$", "")


    for e in cmd_output:
        
        e = e.strip()
        index = e.index(slash)
        e = e[0:index]
        
    return cmd_output


