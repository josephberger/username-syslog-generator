import argparse
import ipaddress
import random
import socket
import sys
import time
from datetime import datetime

from faker import Faker


def generate_fake_names(num_names):
    fake = Faker()
    fake_names = []
    
    for _ in range(num_names):
        first_initial = random.choice('abcdefghijklmnopqrstuvwxyz')
        last_name = fake.last_name().lower()
        fake_names.append(first_initial + last_name)
    
    return fake_names

def generate_pid():
    pid = random.randint(1000000, 9999999)
    return pid

def generate_syslog_message_accepted(server_name, name, ip_address, source_port, pid):
    current_time = datetime.now().strftime("%b %d %H:%M:%S")
    syslog_message = f"{current_time} {server_name} sshd[{pid}]: Accepted password for {name} from {ip_address} port {source_port} ssh2"
    return syslog_message

def generate_syslog_message_disconnected(server_name, name, ip_address, source_port, pid):
    current_time = datetime.now().strftime("%b %d %H:%M:%S")
    syslog_message = f"{current_time} {server_name} sshd[{pid}]: Disconnected from user {name} {ip_address} port {source_port}"
    return syslog_message

def send_udp_packet(message, ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip_address, port))
    sock.close()

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate fake syslog messages.')
parser.add_argument('-d', '--destination', metavar='destination_ip', type=str, default="localhost", help='Destination IP address for syslog server (default: localhost)')
parser.add_argument('-n', '--num_users', metavar='num_users', type=int, default=20, help='Number of fake users (default: 20)')
parser.add_argument('--domain', metavar='domain', type=str, default="corp.com", help='Domain desired, only for log output.  (default: corp.com)')
parser.add_argument('--network', metavar='network', type=str, default="172.16.0.0/12", help='Subnet for username mapping.  (default: 172.16.0.0/12)')
parser.add_argument('--speed', metavar='speed', type=str, default="medium", help='Rate which logs are generated; slow, medium, fast  (default: medium)')
args = parser.parse_args()

# Generate fake names
fake_names_list = generate_fake_names(args.num_users)

# Dictionary to track user information
user_ip_dict = {}

# Verify the network specified
try:
    mapping_network = ipaddress.IPv4Network(args.network)
except:
    print(f"[!] '{args.network}' is not a valid IPv4 subnet, please verify. (example: 192.168.1.0/24)")
    sys.exit()

# Verify speed
if args.speed.lower() == "medium":
    speed = [10, 30]
elif args.speed.lower() == "slow":
    speed = [20, 60]
elif args.speed.lower() == "fast":
    speed = [5, 15]
else:
    print(f"[!] '{args.speed}' is not a valid speed.  Defaulting to 'medium'")
    speed = [10, 30]

# Infinite loop for generating syslog messages
while True:
    server_name = Faker().hostname().split(".")[0] + "." + args.domain
    name = random.choice(fake_names_list)
    
    # Check if the user exists in the dictionary
    if name in user_ip_dict:
        server_name, ip_address, source_port, pid = user_ip_dict[name]
        syslog_message = generate_syslog_message_disconnected(server_name, name, ip_address, source_port, pid)
        del user_ip_dict[name]
    else:
        # Generate a new random IP address for the user
        ip_network = ipaddress.IPv4Network(mapping_network)
        ip_address = str(ipaddress.ip_address(random.randint(int(ip_network.network_address), int(ip_network.broadcast_address))))
        
        # Generate a new random source port for the user
        source_port = random.randint(1024, 65535)
        
        # Generate a new random PID for the user
        pid = generate_pid()
        
        user_ip_dict[name] = (server_name, ip_address, source_port, pid)
        syslog_message = generate_syslog_message_accepted(server_name, name, ip_address, source_port, pid)
    
    # Print the syslog message
    print(syslog_message)
    
    # Send UDP packet if destination IP is specified
    if args.destination:
        udp_ip = args.destination  # Destination IP address
        udp_port = 514  # Destination port
        send_udp_packet(syslog_message, udp_ip, udp_port)

    # Generate a random interval between 10 and 30 seconds
    random_interval = random.randint(speed[0], speed[1])
    
    # Wait for the random interval
    time.sleep(random_interval)
