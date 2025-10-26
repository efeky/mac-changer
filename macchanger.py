import subprocess
import re
import random

# by https://github.com/efeky

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Could not read MAC address.")
        return None

def change_mac(interface, new_mac):
    print(f"Changing MAC address for {interface} to {new_mac}.")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    print("MAC address changed!")

def randomize_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

def list_interfaces():
    interfaces = subprocess.check_output(["ifconfig"]).decode("utf-8")
    return re.findall(r"^\w+", interfaces, re.MULTILINE)

if __name__ == "__main__":
    print("Available network interfaces:")
    available_interfaces = list_interfaces()
    for interface in available_interfaces:
        print(interface)

    interface = input("Enter the target interface (e.g., en0): ")

    if interface not in available_interfaces:
        print("Error: Interface does not exist. Please check the name and try again.")
    else:
        print("1 - Check Current MAC Address")
        print("2 - Enter MAC Address Manually")
        print("3 - Randomize MAC Address")
        choice = input("Choose an option: ")

        if choice == '1':
            current_mac = get_current_mac(interface)
            if current_mac:
                print(f"Current MAC address: {current_mac}")

        elif choice == '2':
            new_mac = input("Enter new MAC address (e.g., 00:11:22:33:44:55): ")
            current_mac = get_current_mac(interface)
            if current_mac:
                print(f"Current MAC address: {current_mac}")
            change_mac(interface, new_mac)

        elif choice == '3':
            new_mac = randomize_mac()
            current_mac = get_current_mac(interface)
            if current_mac:
                print(f"Current MAC address: {current_mac}")
            change_mac(interface, new_mac)

        else:
            print("Invalid option selected.")
