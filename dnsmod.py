#!/usr/bin/env python3

import argparse
import os
import platform
import re
import sys
from abc import ABC, abstractmethod

import requests

VERSION = "1.0.4"
CONNECTION_TEST_URL = "https://google.com"
PING_TEST_IP = "1.1.1.1"


def dns_providers():
    dns = {
        "Shecan": ["178.22.122.100", "185.51.200.2"],
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"],
        "AdGuard": ["94.140.14.14", "94.140.15.15"],
        "403": ["10.202.10.202", "10.202.10.102"],
        "RadarGame": ["10.202.10.10", "10.202.10.11"],
    }
    return dns


# DNSMod abstract class
class DNSModAbs(ABC):
    """
    Abstract DNSMod class.
    """

    # Init
    def __init__(self, args) -> None:
        self.args = args

    # Backup DNS
    @abstractmethod
    def backup_dns(self) -> None:
        """
        Backup the current DNS config.
        """
        pass

    # Restore DNS
    @abstractmethod
    def restore_dns(self) -> None:
        """
        Restore the DNS config.
        """
        pass

    # Test connection
    def test_connection(self) -> None:
        """
        Test the connection.
        """
        try:
            requests.get(CONNECTION_TEST_URL, timeout=5)
            print("Connection test passed ...")
            print("Good luck have fun! :)")
        except Exception as e:
            print("Connection test failed ...")
            print("Try another DNS provider. T_T")

    # Test connection via ping
    def test_connection_ping(self) -> None:
        """
        Test the connection via ping.
        """
        os.system("ping -c 4 " + PING_TEST_IP)

    # Check provider
    def check_provider(self, provider) -> None:
        """
        Check if the provider is secure.
        """
        if provider == "403":
            print("WARNING: This provider is government based and probably not secure!")

    # Check permissions
    def check_permissions(self) -> None:
        """
        Check if the user has the required permissions.
        """
        if os.geteuid() != 0:
            print("You need to have root privileges to run this.")
            print("Try again, this time using 'sudo'. May we meet again!")
            sys.exit(1)

    # Check current DNS
    @abstractmethod
    def check_current_dns(self) -> None:
        """
        Check the current DNS config.
        """
        pass

    # Set DNS
    @abstractmethod
    def set_dns(self) -> None:
        """
        Set the DNS config.
        """
        pass

    # Update
    @abstractmethod
    def update(self) -> None:
        """
        Update DNSMod.
        """
        pass

    # Do the magic :)
    def do_magic(self) -> None:
        """
        Do the magic.
        """
        self.set_dns()


# DNSMod Linux
class DNSModLinux(DNSModAbs):
    """
    This is the main class to manage DNS.
    """

    def __init__(self, args) -> None:
        super().__init__(args)
        self.dns_path = "/etc/resolv.conf"
        self.dns_bak_path = "/etc/resolv.conf.dnsmod.bak"

        self.check_permissions()
        self.backup_dns()

    # Backup DNS
    def backup_dns(self) -> None:
        """
        Backup the current DNS config.
        """
        os.system(f"cp {self.dns_path} {self.dns_bak_path}")

    # Restore DNS
    def restore_dns(self) -> None:
        """
        Restore the DNS config.
        """
        if not os.path.isfile(self.dns_bak_path):
            print("No previous DNS config found!")
            return

        os.rename(self.dns_bak_path, self.dns_path)
        print("Previous DNS config has been restored!")
        self.test_connection()

    # Check current DNS
    def check_current_dns(self) -> None:
        """
        Check the current DNS config.
        """
        print("Current DNS config:")
        print("====" * 6)
        with open(self.dns_path, "r") as f:
            print(f.read())

    # Set DNS
    def set_dns(self) -> None:
        """
        Set the DNS config.
        """
        dns = dns_providers()
        if self.args.provider != None:
            dns = dns[self.args.provider]
        elif self.args.set != None:
            dns = self.args.set
        self.check_provider(self.args.provider)

        with open(self.dns_path, "w") as f:
            f.write(
                f"# Overwritten by DNSMod v{VERSION} - Provider: {self.args.provider} \n"
            )
            f.write(f"# Previous DNS config at {self.dns_bak_path} \n \n")
            f.write(f"nameserver {dns[0]} \n")
            f.write(f"nameserver {dns[1]} \n")
        print("DNS config has been set!")
        self.test_connection()

    # Update DNSMod
    def update(self) -> None:
        """
        Update DNSMod.
        """
        # TODO: add update feature
        pass


# DNSMod Darwin
class DNSModDarwin(DNSModAbs):
    """
    This is the main class to manage DNS.
    """

    def __init__(self, args) -> None:
        super().__init__(args)
        self.dns_bak_path = "/var/root/.dnsmod"
        self.interface = "Wi-Fi"

        self.check_permissions()
        self.backup_dns()

    # Backup DNS
    def backup_dns(self) -> None:
        """
        Backup the current DNS config.
        """
        current = (
            os.popen(f"networksetup -getdnsservers {self.interface}")
            .read()
            .replace("\n", " ")
        )
        with open(self.dns_bak_path, "w") as f:
            f.write(current)

    # Restore DNS
    def restore_dns(self) -> None:
        """
        Restore the DNS config.
        """
        if not os.path.isfile(self.dns_bak_path):
            print("No previous DNS config found!")
            return

        with open(self.dns_bak_path, "r") as f:
            dns = f.read().split(" ")
            os.system(f"networksetup -setdnsservers {self.interface} {dns[0]} {dns[1]}")
        print("Previous DNS config has been restored!")
        self.test_connection()

    # Check current DNS
    def check_current_dns(self) -> None:
        """
        Check the current DNS config.
        """
        current = os.popen(f"networksetup -getdnsservers {self.interface}").read()
        print("Current DNS config:")
        print("====" * 6)
        print(current)

    # Set DNS
    def set_dns(self) -> None:
        """
        Set the DNS config.
        """
        dns = dns_providers()
        if self.args.provider != None:
            dns = dns[self.args.provider]
        elif self.args.set != None:
            dns = self.args.set
        self.check_provider(self.args.provider)

        os.system(f"networksetup -setdnsservers {self.interface} {dns[0]} {dns[1]}")
        print("DNS config has been set!")
        self.test_connection()

    # Update DNSMod
    def update(self) -> None:
        """
        Update DNSMod.
        """
        # TODO: add update feature
        pass


# handler
def handler(args):
    system = platform.system()
    if system == "Linux":
        app = DNSModLinux(args)
    elif system == "Darwin":
        app = DNSModDarwin(args)
    elif system == "Windows":
        return

    if args.version:
        print(f"DNSMod v{VERSION}")

    if args.check:
        app.check_current_dns()
    elif args.restore:
        app.restore_dns()
    elif args.test:
        app.test_connection_ping()
        app.test_connection()
    elif args.update:
        app.update()
    else:
        app.do_magic()


def main():
    dns = dns_providers()
    parser = argparse.ArgumentParser(description="DNSMod")
    # providers
    parser.add_argument(
        "-p",
        "--provider",
        help=f"Choose a DNS provider from {', '.join(list(dns.keys()))}",
        type=str,
        choices=list(dns.keys()),
        action="store",
        default=None,
    )
    # set (2 ip addresses)
    parser.add_argument(
        "-s",
        "--set",
        help="Set custom DNS",
        nargs=2,
        type=str,
        action="store",
        metavar=("DNS1", "DNS2"),
        default=None,
    )
    parser.add_argument(
        "-c",
        "--check",
        help="Check current DNS config",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="Test connection",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-r", "--restore", help="Restore DNS", action="store_true", default=False
    )
    parser.add_argument(
        "-u", "--update", help="Update DNSMod", action="store_true", default=False
    )
    parser.add_argument(
        "-v", "--version", help="Show version", action="store_true", default=False
    )

    args = parser.parse_args()
    # if there is nor provider or custom
    if not (args.check or args.test or args.restore or args.update or args.version):
        if args.provider == None and args.set == None:
            print(
                f"Choose a provider from {', '.join(list(dns.keys()))} or use custom DNS!"
            )
            exit()
        # if there is a provider and custom
        if args.provider != None and args.set != None:
            print("Either choose a provider or use custom DNS!")
            exit()
        # check if the custom DNS patterns are valid using regex
        if args.set != None:
            if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args.set[0]):
                print("Invalid DNS1!")
                exit()
            if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args.set[1]):
                print("Invalid DNS2!")
                exit()

    handler(args)


if __name__ == "__main__":
    main()
