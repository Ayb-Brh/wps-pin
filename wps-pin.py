#!/usr/bin/env python

class WPSException(Exception):
    pass

class WPS(object):

    def checksum(self, pin):
       
        accum = 0

        while pin:
            accum += (3 * (pin % 10))
            pin = int(pin / 10)
            accum += (pin % 10)
            pin = int(pin / 10)

        return ((10 - accum % 10) % 10)

class DLink(object):

    def __init__(self):
        self.wps = WPS()

    def __mac2nic(self, mac):
       
        mac = mac.replace(':', '').replace('-', '')

        if len(mac) == 12:
            try:
                nic = int(mac[6:], 16)
            except ValueError as e:
                raise WPSException("Invalid NIC: [%s]" % mac[6:])
        elif len(mac) == 6:
            try:
                nic = int(mac, 16)
            except ValueError as e:
                raise WPSException("Invalid NIC: [%s]" % mac)
        else:
            raise WPSException("Invalid MAC address: [%s]" % mac)

        return nic

    def generate(self, mac):
        nic = self.__mac2nic(mac)

        pin = nic ^ 0x55AA55
        pin = pin ^ (((pin & 0x0F) << 4) +
                     ((pin & 0x0F) << 8) +
                     ((pin & 0x0F) << 12) +
                     ((pin & 0x0F) << 16) +
                     ((pin & 0x0F) << 20))
        pin = pin % int(10e6)

        if pin < int(10e5):
            pin += ((pin % 9) * int(10e5)) + int(10e5);
        return (pin * 10) + self.wps.checksum(pin)

if __name__ == '__main__':
    import sys

    try:
        mac = sys.argv[1]
    except IndexError:
        print ("Usage: %s <mac>" % sys.argv[0])
        sys.exit(1)

    try:
        print ("Default pin: %d" % DLink().generate(mac))
    except WPSException as e:
        print (str(e))
        sys.exit(1)