from paramiko import SSHClient

slash = "\$"
slash = slash.replace("$", "")

#SSH' into host and sends a dir command then returns folder names into a list

def show_dir(user, password, ip):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=ip, username=user, password=password)

    (stdin, stdout, stderr) = ssh.exec_command("dir")

    cmd_output = str(stdout.read())


    cmd_output = list(cmd_output.split("<DIR>"))


    for e in cmd_output:
        
        e = e.strip()
        index = e.index(slash)
        e = e[0:index]
        
    return cmd_output


#SSH' into host and checks if cert is in filepath. returns boolean

def check_remote_cert(user, password, ip, filepath):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    try:
        ssh.connect(hostname=ip, username=user, password=password, timeout=5)
        print("Connected!")

        backslash_index = 1 + filepath.rindex(slash)

        filename = filepath[backslash_index:]
        path = filepath[0:backslash_index]


        (stdin, stdout, stderr) = ssh.exec_command(f"cd {path}&& dir")

        cmd_output = str(stdout.read())

        if filename in cmd_output:
            return True
        else:
            return False
    except:
        print("Connection failed!")
        return False

