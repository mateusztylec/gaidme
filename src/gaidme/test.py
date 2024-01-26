import pexpect


def run_commands(commands):
    for command in commands:
        child = pexpect.spawn(f'/bin/zsh -c "{command}"')
        child.expect(pexpect.EOF)
        print(f"Output for '{command}':\n{child.before.decode()}")
        child.close()


# Przykład użycia
commands = [
    "echo 'Hello, World!'",
    "history",
    "pwd"
]
run_commands(commands)

# from librouteros import connect

# # Replace these with your MikroTik's IP, username, and password
# ip = '192.168.88.1'
# username = 'grafana'
# password = '2Vwqyjk823158Gsavsfgh'

# try:
#     api = connect(host=ip, username=username, password=password)
#     # If connection is successful, fetch and print router's identity
#     identity = api(cmd='/system/identity/print')
#     print(identity)
# except Exception as e:
#     print(f"Error: {e}")
