import subprocess
import re

# regex pattern for iwevent messages
pattern = re.compile('(.*?)\s+(.*?)\s+([\w|\s]+):(.*)$')

# spaw new iwevent process and capture output
result = subprocess.Popen("iwevent", shell=True, stdout=subprocess.PIPE)

# each line is a new event
for line in result.stdout:
    m = pattern.search(line.decode("utf-8"))
    if m:
        # new peer connected
        if "Registered" in m.group(3):
            print("New peer connected: " + m.group(4))

        # peer disconnected
        elif "Expired" in m.group(3):
            print("Peer disconnected: " + m.group(4))

# TODO: Fire Events for manager