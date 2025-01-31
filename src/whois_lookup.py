#
# Description: Source code for the WHOIS lookups for a more accurate domain search
# Author: Alexander Powell
# Version: v1.0
# Dependencies: whois
#


import sys
import whois


def domain_search(domain: str):
    try:
        info = whois.whois(domain)
        return info
    except Exception as e:
        return f"WHOIS lookup failed: {e}"



# For personal testing usage
if __name__ == "__main__":
    # Test the search with a sys arg
    try:
        print(domain_search(sys.argv[1]))
    except Exception as e:
        print(f"Error: {e}\n\nMake sure the domain name is added as a system argument.\nIf you are not running this"
              f" in the terminal and are using a run button, dont. \nOnly use the terminal to test this from this file.")
