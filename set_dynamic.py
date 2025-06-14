#----------------------------------------------------------------------------------------
# set_dynamic_ip() using systemd-networkd
#----------------------------------------------------------------------------------------
import os
import shutil

def set_dynamic_ip(interface: str):
    """
    Configures dynamic IP (DHCP) for the specified Ethernet interface using systemd-networkd.
    
    :param interface: Network interface name (e.g., 'eth0')
    """
    file_path = f"/etc/systemd/network/{interface}.network"
    backup_path = f"{file_path}.bak"

    config_content = f"""[Match]
Name={interface}

[Network]
DHCP=yes
"""

    try:
        # Backup existing config if it exists
        if os.path.exists(file_path):
            shutil.copy(file_path, backup_path)
            print(f"🔄 Backup created: {backup_path}")

        # Write the new DHCP config
        with open(file_path, "w") as f:
            f.write(config_content)
        print(f"✅ DHCP config written to {file_path}")

        # Enable and restart systemd-networkd
        os.system("sudo systemctl enable systemd-networkd")
        os.system("sudo systemctl restart systemd-networkd")
        print("🔁 systemd-networkd service restarted and enabled.")

    except Exception as e:
        print(f"🚨 Failed to configure DHCP: {e}")
        
#----------------------------------------------------------------------------------------
# Alternative Using /etc/network/interfaces (Debian-based)
#----------------------------------------------------------------------------------------
# def set_dynamic_ip_legacy(interface: str):
#     """
#     Configures dynamic IP (DHCP) for the specified Ethernet interface using /etc/network/interfaces.
#
#     :param interface: Network interface name (e.g., 'eth0')
#     """

#     # Prepare the DHCP configuration for the given interface
#     config = f"""auto {interface}
# iface {interface} inet dhcp
# """

#     try:
#         # Backup the existing /etc/network/interfaces file
#         shutil.copy("/etc/network/interfaces", "/etc/network/interfaces.bak")
#         print("🔄 Backup of /etc/network/interfaces created.")

#         # Write the new DHCP configuration into the interfaces file
#         with open("/etc/network/interfaces", "w") as f:
#             f.write(config)
#         print("✅ DHCP config written to /etc/network/interfaces")

#         # Restart the networking service to apply changes
#         os.system("sudo systemctl restart networking")
#         print("🔁 Networking service restarted.")

#     except Exception as e:
#         # Print any exception that occurs during the configuration process
#         print(f"🚨 Failed to configure DHCP: {e}")
