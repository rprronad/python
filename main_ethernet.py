#Board: RZG2L Board
#------------------------------------------------------------------------------------------------------------
# Sample application to configure Ethernet interface with static or dynamic IP.
#------------------------------------------------------------------------------------------------------------
import subprocess
from set_dynamic import set_dynamic_ip
from set_static import set_static_ip

#------------------------------------------------------------------------------------------------------------
INTERFACE = "eth0"
HOST = "8.8.8.8"
DNS_SERVERS = ["8.8.8.8", "8.8.4.4"]
#------------------------------------------------------------------------------------------------------------

def ping_host(host: str):
    """
    Ping a specified host to check connectivity.

    :param host: Host IP or domain to ping.
    """
    try:
        result = subprocess.run(["ping", "-c", "4", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"✅ Ping to {host} successful:\n{result.stdout.decode()}")
        else:
            print(f"❌ Ping to {host} failed:\n{result.stderr.decode()}")
    except Exception as e:
        print(f"⚠️ Error during ping: {e}")

#------------------------------------------------------------------------------------------------------------
def get_user_choice() -> int:
    """
    Prompt user for IP configuration type.

    :return: 1 for static, 2 for dynamic
    """
    print("\nSelect IP configuration method:")
    print("1. Static IP")
    print("2. Dynamic IP (DHCP)")
    
    try:
        return int(input("Enter choice (1 or 2): "))
    except ValueError:
        return -1  # Invalid input

#------------------------------------------------------------------------------------------------------------
def main():
    """
    Main function to drive the IP configuration logic.
    """
    try:
        while True:
            choice = get_user_choice()

            if choice == 1:
                set_static_ip(INTERFACE, "192.168.1.300", "255.255.255.0", "192.168.1.1", DNS_SERVERS)
                ping_host(HOST)

            elif choice == 2:
                set_dynamic_ip(INTERFACE)
                ping_host(HOST)

            else:
                print("⚠️ Invalid input. Please enter 1 or 2.")

    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user.")
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")

#------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#--------------------------------------------->>>End<<<-------------------------------------------------------
