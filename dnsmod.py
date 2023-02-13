#!/usr/bin/env python3

import argparse
import os
import platform
import sys
from time import sleep

import requests

VERSION = "1.0.0"
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
    }
    return dns


# DNSMod main class
class DNSMod:
    """
    This is the main class to manage DNS.
    """

    def __init__(self, args) -> None:
        self.system = platform.system()
        self.args = args

        self.check_permissions()

        if self.system == "Linux":
            self.dns_path = "/etc/resolv.conf"
            self.dns_bak_path = "/etc/resolv.conf.bak"
        # TODO: add MacOS support
        elif self.system == "Darwin":
            pass

        self.backup_dns()

    # Backup DNS
    def backup_dns(self) -> None:
        """
        Backup the current DNS config.
        """
        if self.system == "Linux" and os.path.isfile(self.dns_path):
            os.system(f"cp {self.dns_path} {self.dns_bak_path}")
        # TODO: add MacOS support
        elif self.system == "Darwin":
            pass

    # Restore DNS
    def restore_dns(self) -> None:
        """
        Restore the DNS config.
        """
        if self.system == "Linux" and os.path.isfile(self.dns_bak_path):
            os.rename(self.dns_bak_path, self.dns_path)
            print("Previous DNS config has been restored ...")
            self.test_connection()
        # TODO: add MacOS support
        elif self.system == "Darwin":
            pass

    # Test connection
    def test_connection(self) -> bool:
        """
        Test the connection.
        """
        try:
            requests.get(CONNECTION_TEST_URL, timeout=5)
            print("Connection test passed ...")
            print("Good luck Have Fun! :)")
            # os.system("ping -c 4 " + PING_TEST_IP)
            return True
        except Exception as e:
            print("Connection test failed ...")
            print("Try another DNS provider. -_-")
            # os.system("ping -c 4 " + PING_TEST_IP)
            return False

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
        if self.system == "Linux":
            if os.geteuid() != 0:
                print("You need to have root privileges to run this.")
                print("Try again, this time using 'sudo'. May we meet again!")
                sys.exit(1)
        # TODO: add MacOS support
        elif self.system == "Darwin":
            pass

    # Set DNS
    def set_dns(self) -> None:
        """
        Set the DNS config.
        """
        dns = dns_providers()
        if self.args.provider != None:
            dns = dns[self.args.provider]
        elif self.args.custom != None:
            dns = self.args.custom
        self.check_provider(self.args.provider)

        if self.system == "Linux":
            with open(self.dns_path, "w") as f:
                f.write(
                    f"# Overwritten by DNSMod v{VERSION} - Provider: {self.args.provider} \n"
                )
                f.write(f"# Previous DNS config at {self.dns_bak_path} \n \n")
                f.write(f"nameserver {dns[0]} \n")
                f.write(f"nameserver {dns[1]} \n")
        # TODO: add MacOS support
        elif self.system == "Darwin":
            pass

        # Test connection
        self.test_connection()

    # Update DNSMod
    def update(self) -> None:
        """
        Update DNSMod.
        """
        # TODO: add update feature
        pass

    # Do the magic :)
    def do_magic(self) -> None:
        """
        Do the magic.
        """
        self.set_dns()


# handler
def handler(args):
    app = DNSMod(args)
    if args.update:
        app.update()
    elif args.version:
        print(f"DNSMod v{VERSION}")
    elif args.restore:
        app.restore_dns()
    else:
        app.do_magic()


def main():
    dns = dns_providers()
    parser = argparse.ArgumentParser(description="DNSMod")
    # providers
    parser.add_argument(
        "-p",
        "--provider",
        help=f"Choose a DNS provider from {dns.keys()}",
        type=str,
        action="store",
        default=list(dns.keys())[1],
    )
    # custom (2 ip)
    parser.add_argument(
        "-c",
        "--custom",
        help="Use custom DNS",
        nargs=2,
        type=str,
        action="store",
        metavar=("DNS1", "DNS2"),
        default=None,
    )
    parser.add_argument(
        "-v", "--version", help="Show version", action="store_true", default=False
    )
    parser.add_argument(
        "-u", "--update", help="Update DNSMod", action="store_true", default=False
    )
    parser.add_argument(
        "-r", "--restore", help="Restore DNS", action="store_true", default=False
    )
    args = parser.parse_args()
    # if there is nor provider or custom
    if args.provider == None and args.custom == None:
        print("Choose a provider or use custom DNS!")
        exit()
    # if there is a provider and custom
    if args.provider != None and args.custom != None:
        print("Either choose a provider or use custom DNS!")
        exit()

    print(args)
    handler(args)


if __name__ == "__main__":
    main()
