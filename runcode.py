import subprocess
def run(path):
        command = subprocess.run(args= 'python {}'.format(path), shell=True)
        return command, command.returncode