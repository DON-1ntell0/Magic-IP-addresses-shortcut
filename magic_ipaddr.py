# Here is magic_ipaddr which is just a copy implemented in python of the one made 
# in C by Spike (https://github.com/spikex) 
# It can be found here on this article here : https://stuff-things.net/2014/09/25/magic-ip-address-shortcuts/



import socket
import click
import struct
from colorama import Fore, Style, init

init()

@click.command()
@click.option('--ipaddr', '-i', prompt='Please mention the I.P', help='I.P address you are trying to masquerade')

def main(ipaddr):
    if not is_valid_ipv4_address(ipaddr):
        click.echo(Fore.RED + 'Sorry mate! We need a valid I.P address to do the trick!' + Style.RESET_ALL)
    else:
        try:
            unsigned_addr = socket.ntohl(struct.unpack("!I", socket.inet_aton(ipaddr))[0])

            unsigned_octet1 = (0xff000000 & unsigned_addr) >> 24
            unsigned_octet2 = (0x00ff0000 & unsigned_addr) >> 16
            unsigned_octet3 = (0x0000ff00 & unsigned_addr) >> 8
            unsigned_octet4 = (0x000000ff & unsigned_addr)

            click.echo(Fore.CYAN + "\nYou can try to ping those I.Ps below: " + Style.RESET_ALL)
            click.echo(Fore.CYAN + "--------------------------------------" + Style.RESET_ALL)
            click.echo(Fore.CYAN + "ping {}.{}.{}.{}".format(unsigned_octet1, unsigned_octet2, unsigned_octet3, unsigned_octet4) + Style.RESET_ALL)
            click.echo(Fore.CYAN + "ping {}.{}".format(unsigned_octet1, (unsigned_octet2 << 16) + (unsigned_octet3 << 8) + unsigned_octet4) + Style.RESET_ALL)
            click.echo(Fore.CYAN + "ping {}.{}".format(unsigned_octet1, (unsigned_octet2 << 16) + (unsigned_octet3 << 8) + unsigned_octet4) + Style.RESET_ALL)
            click.echo(Fore.CYAN + "ping {}".format(unsigned_addr) + Style.RESET_ALL)
        except socket.error:
            click.echo(Fore.RED + "\nInvalid I.P address." + Style.RESET_ALL)
            click.echo(Fore.RED + 'inet_aton could not parse %s' % ipaddr + Style.RESET_ALL)

def is_valid_ipv4_address(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        click.echo(Fore.RED + '\ninet_aton could not parse %s' % address + Style.RESET_ALL)
        return False

if __name__ == "__main__":
    main()
