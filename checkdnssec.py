import dns.name
import dns.query
import dns.dnssec
import dns.message
import dns.resolver
import dns.rdatatype
import sys
from datetime import datetime

# Based on some of the code in;
# https://stackoverflow.com/questions/26137036/programmatically-check-if-domains-are-dnssec-protected
# https://stackoverflow.com/questions/5235569/using-the-dig-command-in-python
# https://stackoverflow.com/questions/3898363/python-dns-resolver-set-specific-dns-server
# http://www.dnspython.org/examples.html

def get_dnssec(dnsresolver, domain_name):

    # Check the input and add missing . if needed
    if not domain_name.endswith("."):
        domain_name = domain_name + "."

    # get the primarynameservers for the target domain
    response = dnsresolver.query(domain_name, dns.rdatatype.NS)
    nsname = response.rrset[0] # name
    try:
        response = dnsresolver.query(str(nsname), dns.rdatatype.A)
    except:
        raise Exception("timeout")
    nsaddr = response.rrset[0].to_text() # IPv4

    # get the DNSKEY for the zone
    request = dns.message.make_query(domain_name,
                                     dns.rdatatype.DNSKEY,
                                     want_dnssec=True)

    # send the query
    response = dns.query.udp(request,nsaddr,timeout=1.0)
    if response.rcode() != 0:
        raise Exception("get_dnssec_status: rcode was not 0")
    # the answer should contain both DNSKEY and RRSIG(DNSKEY)

    answer = response.answer
    if len(answer) != 2:
        # an exception was raised
        raise Exception("get_dnssec_status: lenght of answer != 2, " +
                        str(len(answer)))

    # validate the DNSKEY signature
    name = dns.name.from_text(domain_name)

    try:
        dns.dnssec.validate(answer[0],answer[1],{name:answer[0]})
    except dns.dnssec.ValidationFailure:
        # an exception was raised
        raise Exception("get_dnssec_status: Failed validation.")

    else:
        # valid DNSSEC signature found
        return


if __name__ == "__main__":
    main()


def main():
    dnsresolver = dns.resolver.Resolver()
    # set a default nameserver
    dnsresolver.nameservers = ["8.8.8.8"]
    dnsresolver.timeout = 1.0
    dnsresolver.lifetime = 1.0
    if len(sys.argv) == 2:
        domain_name = sys.argv[1]
    else:
        domaigitgn_name = "faalkaart.nl."

    try:
        get_dnssec(dnsresolver, domain_name)
    except:
        print("Failure " + domain_name)
        sys.exit(1)

    print("Success " + domain_name)
    sys.exit(0)
