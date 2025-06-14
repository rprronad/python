#-----------------------------------------------------------------------------------
# set_static_ip() using systemd-networkd
#-----------------------------------------------------------------------------------
import os
import shutil

def set_static_ip(interface, address, netmask, gateway, dns_servers):
    """
    Configures a static IP address for the given interface using systemd-networkd.

    :param interface: Interface name (e.g., 'eth0')
    :param address: Static IP address (e.g., '192.168.1.100')
    :param netmask: Netmask in dotted-decimal (e.g., '255.255.255.0')
    :param gateway: Default gateway (e.g., '192.168.1.1')
    :param dns_servers: List of DNS server IPs (e.g., ['8.8.8.8', '1.1.1.1'])
    """
    def netmask_to_cidr(mask):
        """Convert dotted-decimal netmask to CIDR notation."""
        return sum(bin(int(part)).count('1') for part in mask.split('.'))

    try:
        # Prepare CIDR format and DNS string
        cidr = netmask_to_cidr(netmask)
        ip_cidr = f"{address}/{cidr}"
        dns_line = " ".join(dns_servers)

        # Build the .network configuration content
        config = f"""[Match]
Name={interface}

[Network]
Address={ip_cidr}
Gateway={gateway}
DNS={dns_line}
"""

        # Path to network configuration file
        config_path = f"/etc/systemd/network/{interface}.network"
        backup_path = f"{config_path}.bak"

        # Backup existing file if it exists
        if os.path.exists(config_path):
            shutil.copy(config_path, backup_path)
            print(f"🔄 Backup created at: {backup_path}")

        # Write the new static IP config
        with open(config_path, "w") as f:
            f.write(config)
        print(f"✅ Static IP configuration written to {config_path}")

        # Apply the new network settings
        os.system("sudo systemctl enable systemd-networkd")
        os.system("sudo systemctl restart systemd-networkd")
        print("🔁 systemd-networkd service restarted.")

    except Exception as e:
        print(f"🚨 Failed to configure static IP: {e}")
#-----------------------------------------------------------------------------------
# Method (Debian-style /etc/network/interfaces)
#-----------------------------------------------------------------------------------
# def set_static_ip_legacy(interface, address, netmask, gateway, dns_servers):
#     """
#     Configures a static IP using /etc/network/interfaces and updates /etc/resolv.conf.
#
#     :param interface: Interface name
#     :param address: Static IP
#     :param netmask: Netmask
#     :param gateway: Default gateway
#     :param dns_servers: List of DNS servers
#     """

#     # Prepare the /etc/network/interfaces content for static IP configuration
#     interfaces_config = f"""auto {interface}
# iface {interface} inet static
#     address {address}
#     netmask {netmask}
#     gateway {gateway}
#     dns-nameservers {' '.join(dns_servers)}
# """

#     # Create the resolv.conf content with DNS servers
#     resolv_conf = "\n".join([f"nameserver {dns}" for dns in dns_servers]) + "\n"

#     try:
#         # Backup the original interfaces file
#         shutil.copy("/etc/network/interfaces", "/etc/network/interfaces.bak")
