#!/usr/bin/env python

from nose.tools import *
from miniprobe.sensors import adns,apt,cpuload,cputemp,diskspace,ds18b20,external_ip,http,memory,nmap,ping,port,portrange,probehealth,snmpcustom,snmptraffic

# NMAP
def test_nmap_get_kind():
    """nmap returns the correct kind"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.get_kind(), 'mpnmap')

def test_nmap_get_sensordef():
    """NMAP returns correct definition"""
    test_nmap = nmap.NMAP()
    test_sensordef = {
            "kind": test_nmap.get_kind(),
            "name": "NMAP",
            "description": "Checks the availability of systems.",
            "help": "Checks the availability of systems on a network and logs this to a separate logfile on the miniprobe.",
            "tag": "mpnmapsensor",
            "groups": [
                {
                    "name": "nmapspecific",
                    "caption": "NMAP specific",
                    "fields": [
                        {
                            "type": "integer",
                            "name": "timeout",
                            "caption": "Timeout (in ms)",
                            "required": "1",
                            "default": 50,
                            "minimum": 10,
                            "maximum": 1000,
                            "help": "If the reply takes longer than this value the request is aborted "
                                    "and an error message is triggered. Max. value is 1000 ms. (=1 sec.)"
                        },
                        {
                            "type": "edit",
                            "name": "ip",
                            "caption": "IP-Address(es)",
                            "required": "1",
                            "default": "",
                            "help": "Specify the ip-address or a range of addresses using one of the following notations:[br]Single: 192.168.1.1[br]CIDR: 192.168.1.0/24[br]- separated: 192.168.1.1-192.168.1.100"
                        }
                    ]
                }
            ]
    }
    assert_equal(test_nmap.get_sensordef(), test_sensordef)

def test_nmap_icmp_echo_request():
    """nmap const ICMP_ECHO_REQUEST is set correct"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.ICMP_ECHO_REQUEST, 8)

def test_nmap_dec2bin():
    """nmap dec2bin results"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.dec2bin(255,8),'11111111')
    assert_equal(test_nmap.dec2bin(254,8),'11111110')
    assert_equal(test_nmap.dec2bin(128,8),'10000000')
    assert_equal(test_nmap.dec2bin(127,8),'01111111')
    assert_equal(test_nmap.dec2bin(0,8),'00000000')

def test_nmap_ip2bin():
    """nmap ip2bin results"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.ip2bin('255.255.255.255'),'11111111111111111111111111111111')
    assert_equal(test_nmap.ip2bin('254.254.254.254'),'11111110111111101111111011111110')
    assert_equal(test_nmap.ip2bin('128.128.128.128'),'10000000100000001000000010000000')
    assert_equal(test_nmap.ip2bin('127.127.127.127'),'01111111011111110111111101111111')
    assert_equal(test_nmap.ip2bin('0.0.0.0'),'00000000000000000000000000000000')

def test_nmap_bin2ip():
    """nmap bin2ip results"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.bin2ip('11111111111111111111111111111111'),'255.255.255.255')
    assert_equal(test_nmap.bin2ip('11111110111111101111111011111110'),'254.254.254.254')
    assert_equal(test_nmap.bin2ip('10000000100000001000000010000000'),'128.128.128.128')
    assert_equal(test_nmap.bin2ip('01111111011111110111111101111111'),'127.127.127.127')
    assert_equal(test_nmap.bin2ip('00000000000000000000000000000000'),'0.0.0.0')

def test_nmap_validateCIDRBlock():
    """nmap validateCIDRBlock results"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.validateCIDRBlock('127.0.0.0'),'Error: Invalid CIDR format!')
    assert_equal(test_nmap.validateCIDRBlock('256.256.256.256/8'),'Error: quad 256 wrong size.')
    assert_equal(test_nmap.validateCIDRBlock('127.0.0.0/33'),'Error: subnet 33 wrong size.')
    assert_true(test_nmap.validateCIDRBlock('127.0.0.0/8'))

def test_nmap_returnCIDR():
    """nmap returnCIDR results"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.returnCIDR('127.0.0.0/30'),['127.0.0.0', '127.0.0.1', '127.0.0.2', '127.0.0.3'])

def test_nmap_checksum():
    """nmap checksum results"""
    test_nmap = nmap.NMAP()
    assert_equal(test_nmap.checksum('test'),6182)
    assert_equal(test_nmap.checksum('python'),43951)
    assert_equal(test_nmap.checksum('prtg'),6950)


# aDNS
def test_adns_get_kind():
    """dns returns the correct kind"""
    test_adns = adns.aDNS()
    assert_equal(test_adns.get_kind(), 'mpdns')

def test_adns_get_sensordef():
    """dns returns correct definition"""
    test_adns = adns.aDNS()
    test_sensordef = {
            "kind": test_adns.get_kind(),
            "name": "DNS",
            "description": "Monitors a DNS server (Domain Name Service), resolves a domain name, and compares it to an IP address",
            "help": "The DNS sensor monitors a Domain Name Service (DNS) server. It resolves a domain name and compares it to a given IP address.",
            "tag": "mpdnssensor",
            "groups": [
                {
                    "name": "DNS Specific",
                    "caption": "DNS Specific",
                    "fields": [
                        {
                            "type": "integer",
                            "name": "timeout",
                            "caption": "Timeout (in s)",
                            "required": "1",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 900,
                            "help": "Timeout in seconds. A maximum value of 900 is allowed."
                        },
                        {
                            "type": "integer",
                            "name": "port",
                            "caption": "Port",
                            "required": "1",
                            "default": 53,
                            "minimum": 1,
                            "maximum": 65535,
                            "help": "Enter the port on which the DNS service of the parent device is running."
                        },
                        {
                            "type": "edit",
                            "name": "domain",
                            "caption": "Domain",
                            "required": "1",
                            "help": "Enter a DNS name or IP address to resolve."
                        },
                        {
                            "type": "radio",
                            "name": "type",
                            "caption": "Query Type",
                            "required": "1",
                            "help": "Specify the type of query that the sensor will send to the DNS server.",
                            "options": {
                                "A": "Host address IPv4 (A)",
                                "AAAA": "Host address IPv6 (AAAA)",
                                "CNAME": "Canonical name for an alias (CNAME)",
                                "MX": "Mail exchange (MX)",
                                "NS": "Authoritative name server (NS)",
                                "PTR": "Domain name pointer (PTR)",
                                "SOA": "Start of a zone of authority marker (SOA)",
                                "SRV": "Service Record"
                            },
                            "default": "A",
                        },
                    ]
                }
            ]
    }
    assert_equal(test_adns.get_sensordef(), test_sensordef)

#APT
def test_apt_get_kind():
    """apt returns the correct kind"""
    test_apt = apt.APT()
    assert_equal(test_apt.get_kind(), 'mpapt')


def test_apt_get_sensordef():
    """apt returns correct definition"""
    test_apt = apt.APT()
    test_sensordef = {
            "kind": test_apt.get_kind(),
            "name": "Linux Updates",
            "description": "Monitors the available updates for the linux system",
            "help": "Monitors the available updates for the linux system using apt-get/yum",
            "tag": "mpaptsensor",
            "fields": [],
            "groups": []
    }
    assert_equal(test_apt.get_sensordef(), test_sensordef)

# CPU Load
def test_cpuload_get_kind():
    """cpuload returns the correct kind"""
    test_cpuload = cpuload.CPULoad()
    assert_equal(test_cpuload.get_kind(), 'mpcpuload')

def test_cpuload_get_sensordef():
    """cpuload returns correct definition"""
    test_cpuload = cpuload.CPULoad()
    test_sensordef = {
            "kind": test_cpuload.get_kind(),
            "name": "CPU Load",
            "description": "Monitors CPU load avg on the system the mini probe is running on",
            "default": "yes",
            "help": "Monitors CPU load avg on the system the mini probe is running on",
            "tag": "mpcpuloadsensor",
            "fields": [],
            "groups": []
    }
    assert_equal(test_cpuload.get_sensordef(), test_sensordef)

# CPU Temp
def test_cputemp_get_kind():
    """cputemp returns the correct kind"""
    test_cputemp = cputemp.CPUTemp()
    assert_equal(test_cputemp.get_kind(), 'mpcputemp')

def test_cputemp_get_sensordef():
    """cputemp returns correct definition"""
    test_cputemp = cputemp.CPUTemp()
    test_sensordef = {
            "kind": test_cputemp.get_kind(),
            "name": "CPU Temperature",
            "description": "Returns the CPU temperature",
            "default": "yes",
            "help": "Returns the CPU temperature",
            "tag": "mpcputempsensor",
            "groups": [
                {
                    "name": "Group",
                    "caption": "Temperature settings",
                    "fields": [
                        {
                            "type": "radio",
                            "name": "celfar",
                            "caption": "Choose between Celsius or Fahrenheit display",
                            "help": "Choose wether you want to return the value in Celsius or Fahrenheit",
                            "options": {
                                "C": "Celsius",
                                "F": "Fahrenheit"
                            },
                            "default": "C"
                        },
                    ]
                }
            ]
    }
    assert_equal(test_cputemp.get_sensordef(testing=True), test_sensordef)

# SNMP Traffic
def test_snmptraffic_get_kind():
    """snmptraffic returns the correct kind"""
    test_snmptraffic = snmptraffic.SNMPTraffic()
    assert_equal(test_snmptraffic.get_kind(), 'mpsnmptraffic')

def test_snmptraffic_get_sensordef():
    """snmptraffic returns correct definition"""
    test_snmptraffic = snmptraffic.SNMPTraffic()
    test_sensordef = {
            "kind": test_snmptraffic.get_kind(),
            "name": "SNMP Traffic",
            "description": "Monitors Traffic on provided interface using SNMP",
            "help": "Monitors Traffic on provided interface using SNMP",
            "tag": "mpsnmptrafficsensor",
            "groups": [
                {
                    "name": "Interface Definition",
                    "caption": "Interface Definition",
                    "fields": [
                        {
                            "type": "edit",
                            "name": "ifindex",
                            "caption": "Interface Index (ifIndex)",
                            "required": "1",
                            "help": "Please enter the ifIndex of the interface to be monitored."
                        }

                    ]
                },
                {
                    "name": "SNMP Settings",
                    "caption": "SNMP Settings",
                    "fields": [
                        {
                            "type": "radio",
                            "name": "snmp_version",
                            "caption": "SNMP Version",
                            "required": "1",
                            "help": "Choose your SNMP Version",
                            "options": {
                                "1": "V1",
                                "2": "V2c",
                                "3": "V3"
                            },
                            "default": 2
                        },
                        {
                            "type": "edit",
                            "name": "community",
                            "caption": "Community String",
                            "required": "1",
                            "help": "Please enter the community string."
                        },
                        {
                            "type": "integer",
                            "name": "port",
                            "caption": "Port",
                            "required": "1",
                            "default": 161,
                            "help": "Provide the SNMP port"
                        },
                        {
                            "type": "radio",
                            "name": "snmp_counter",
                            "caption": "SNMP Counter Type",
                            "required": "1",
                            "help": "Choose the Counter Type to be used",
                            "options": {
                                "1": "32 bit",
                                "2": "64 bit"
                            },
                            "default": 2
                        }
                    ]
                }
            ],
            "fields": []
    }
    assert_equal(test_snmptraffic.get_sensordef(), test_sensordef)

# SNMP Custom
def test_snmpcustom_get_kind():
    """snmpcustom returns the correct kind"""
    test_snmpcustom = snmpcustom.SNMPCustom()
    assert_equal(test_snmpcustom.get_kind(), 'mpsnmpcustom')

def test_snmpcustom_get_sensordef():
    """snmpcustom returns correct definition"""
    test_snmpcustom = snmpcustom.SNMPCustom()
    test_sensordef = {
            "kind": test_snmpcustom.get_kind(),
            "name": "SNMP Custom",
            "description": "Monitors a numerical value returned by a specific OID using SNMP",
            "help": "Monitors a numerical value returned by a specific OID using SNMP",
            "tag": "mpsnmpcustomsensor",
            "groups": [
                {
                    "name": "OID values",
                    "caption": "OID values",
                    "fields": [
                        {
                            "type": "edit",
                            "name": "oid",
                            "caption": "OID Value",
                            "required": "1",
                            "help": "Please enter the OID value."
                        },
                        {
                            "type": "edit",
                            "name": "unit",
                            "caption": "Unit String",
                            "default": "#",
                            "help": "Enter a 'unit' string, e.g. 'ms', 'Kbyte' (for display purposes only)."
                        },

                        {
                            "type": "radio",
                            "name": "value_type",
                            "caption": "Value Type",
                            "required": "1",
                            "help": "Select 'Gauge' if you want to see absolute values (e.g. for temperature value) "
                                    "or 'Delta' for counter differences divided by time period "
                                    "(e.g. for bandwidth values)",
                            "options": {
                                "1": "Gauge",
                                "2": "Delta"
                            },
                            "default": 1
                        },
                        {
                            "type": "integer",
                            "name": "multiplication",
                            "caption": "Multiplication",
                            "required": "1",
                            "default": 1,
                            "help": "Provide a value the raw SNMP value is to be multiplied by."
                        },
                        {
                            "type": "integer",
                            "name": "division",
                            "caption": "Division",
                            "required": "1",
                            "default": 1,
                            "help": "Provide a value the raw SNMP value is divided by."
                        },
                        {
                            "type": "radio",
                            "name": "snmp_version",
                            "caption": "SNMP Version",
                            "required": "1",
                            "help": "Choose your SNMP Version",
                            "options": {
                                "1": "V1",
                                "2": "V2c",
                                "3": "V3"
                            },
                            "default": 2
                        },
                        {
                            "type": "edit",
                            "name": "community",
                            "caption": "Community String",
                            "required": "1",
                            "help": "Please enter the community string."
                        },
                        {
                            "type": "integer",
                            "name": "port",
                            "caption": "Port",
                            "required": "1",
                            "default": 161,
                            "help": "Provide the SNMP port"
                        }
                    ]
                }
            ]
    }
    assert_equal(test_snmpcustom.get_sensordef(), test_sensordef)


# Diskspace
def test_diskspace_get_kind():
    """diskspace returns the correct kind"""
    test_diskspace = diskspace.Diskspace()
    assert_equal(test_diskspace.get_kind(), 'mpdiskspace')

def test_diskspace_sensor_definition():
    """diskspace returns correct definition"""
    test_diskspace = diskspace.Diskspace()
    test_sensordef = {
            "kind": test_diskspace.get_kind(),
            "name": "Disk space",
            "description": "Monitors disk space on the system the mini probe is running on",
            "default": "yes",
            "help": "Monitors disk space on the system the mini probe is running on",
            "tag": "spdiskspacesensor",
            "fields": [],
            "groups": []
    }
    assert_equal(test_diskspace.get_sensordef(), test_sensordef)

# DS18B20
def test_ds18b20_get_kind():
    """ds18b20 returns the correct kind"""
    test_ds18b20 = ds18b20.DS18B20()
    assert_equal(test_ds18b20.get_kind(), 'mpds18b20')

def test_ds18b20_sensor_definition():
    """ds18b20 returns correct definition"""
    test_ds18b20 = ds18b20.DS18B20()
    test_sensordef = {
            "kind": test_ds18b20.get_kind(),
            "name": "DS18B20 Temperature",
            "description": "Returns the temperature measured by an attached DS18B20 temperature sensor on pin 4",
            "default": "no",
            "help": "Returns the temperature measured by an attached DS18B20 temperature sensor on pin 4",
            "tag": "mpds18b20sensor",
            "groups": [
                {
                    "name": "Group",
                    "caption": "Temperature settings",
                    "fields": [
                        {
                            "type": "radio",
                            "name": "celfar",
                            "caption": "Choose between Celsius or Fahrenheit display",
                            "help": "Choose wether you want to return the value in Celsius or Fahrenheit",
                            "options": {
                                "C": "Celsius",
                                "F": "Fahrenheit"
                            },
                            "default": "C"
                        },
                    ]
                }
            ]
    }
    assert_equal(test_ds18b20.get_sensordef(testing=True), test_sensordef)

# External IP
def test_external_ip_get_kind():
    """external_ip returns the correct kind"""
    test_external_ip = external_ip.External_IP()
    assert_equal(test_external_ip.get_kind(), 'mpexternalip')

def test_external_ip_sensor_definition():
    """http returns correct definition"""
    test_external_ip = external_ip.External_IP()
    test_sensordef = {
            "kind": test_external_ip.get_kind(),
            "name": "External IP",
            "description": "Returns the external ip address of the probe",
            "default": "yes",
            "help": "Returns the external ip address of the probe using the website icanhasip.com",
            "tag": "mpexternalipsensor",
            "fields": [],
            "groups": []
    }
    assert_equal(test_external_ip.get_sensordef(), test_sensordef)

# HTTP
def test_http_get_kind():
    """http returns the correct kind"""
    test_http = http.HTTP()
    assert_equal(test_http.get_kind(), 'mphttp')

def test_http_sensor_definition():
    """http returns correct definition"""
    test_http = http.HTTP()
    test_sensordef = {
                "kind": test_http.get_kind(),
                "name": "HTTP",
                "description": "Monitors a web server using HTTP",
                "help": "Monitors a web server using HTTP",
                "tag": "mphttpsensor",
                "groups": [
                    {
                        "name": "HTTP Specific",
                        "caption": "HTTP Specific",
                        "fields": [
                            {
                                "type": "integer",
                                "name": "timeout",
                                "caption": "Timeout (in s)",
                                "required": "1",
                                "default": 60,
                                "minimum": 1,
                                "maximum": 900,
                                "help": "Timeout in seconds. A maximum value of 900 is allowed."
                            },
                            {
                                "type": "edit",
                                "name": "url",
                                "caption": "URL",
                                "required": "1",
                                "default": "http://",
                                "help": "Enter a valid URL to monitor. The server part (e.g. www.paessler.com) "
                                        "may be different from the 'DNS Name' property in the settings of the "
                                        "associated server."
                            },
                            {
                                "type": "radio",
                                "name": "http_method",
                                "caption": "Request Method",
                                "required": "1",
                                "help": "Choose the type of the HTTP request",
                                "options": {
                                    "1": "GET",
                                    "2": "POST",
                                    "3": "HEAD"
                                },
                                "default": 1
                            },
                            {
                                "type": "edit",
                                "name": "post_data",
                                "caption": "POST data",
                                "help": "Data in this field will only be used when request type is POST"
                            }

                        ]
                    },
                    {
                        "name": "Authentication",
                        "caption": "Authentication",
                        "fields": [
                            {
                                "type": "radio",
                                "name": "auth_method",
                                "caption": "Authentication Method",
                                "required": "1",
                                "help": "Choose the type of authentication used",
                                "options": {
                                    "1": "No authentication",
                                    "2": "Basic"
                                },
                                "default": 1
                            },
                            {
                                "type": "edit",
                                "name": "username",
                                "caption": "Username",
                                "help": "Provide username here if target requires authentication"
                            },
                            {
                                "type": "password",
                                "name": "password",
                                "caption": "Password",
                                "help": "Provide password here if target requires authentication"
                            }
                        ]
                    }
                ]
    }
    assert_equal(test_http.get_sensordef(), test_sensordef)

# Memory
def test_memory_get_kind():
    """memory returns the correct kind"""
    test_memory = memory.Memory()
    assert_equal(test_memory.get_kind(), 'mpmemory')

def test_memory_get_sensordef():
    """memory returns correct definition"""
    test_memory = memory.Memory()
    test_sensordef = {
            "kind": test_memory.get_kind(),
            "name": "Memory",
            "description": "Monitors memory on the system the mini probe is running on",
            "default": "yes",
            "help": "Monitors memory on the system the mini probe is running on",
            "tag": "mpmemorysensor",
            "fields": [],
            "groups": []
    }
    assert_equal(test_memory.get_sensordef(), test_sensordef)

# Ping
def test_ping_get_kind():
    """ping returns the correct kind"""
    test_ping = ping.Ping()
    assert_equal(test_ping.get_kind(), 'mpping')

def test_ping_get_sensordef():
    """ping returns correct definition"""
    test_ping = ping.Ping()
    test_sensordef = {
            "kind": test_ping.get_kind(),
            "name": "Ping",
            "description": "Monitors the availability of a target using ICMP",
            "help": "Monitors the availability of a target using ICMP",
            "tag": "mppingsensor",
            "groups": [
                {
                    "name": " Ping Settings",
                    "caption": "Ping Settings",
                    "fields": [
                        {
                            "type": "integer",
                            "name": "timeout",
                            "caption": "Timeout (in s)",
                            "required": "1",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 300,
                            "help": "Timeout in seconds. A maximum value of 300 is allowed."
                        },
                        {
                            "type": "integer",
                            "name": "packsize",
                            "caption": "Packetsize (Bytes)",
                            "required": "1",
                            "default": 32,
                            "minimum": 1,
                            "maximum": 10000,
                            "help": "The default packet size for Ping requests is 32 bytes, "
                                    "but you can choose any other packet size between 1 and 10,000 bytes."
                        },
                        {
                            "type": "integer",
                            "name": "pingcount",
                            "caption": "Ping Count",
                            "required": "1",
                            "default": 1,
                            "minimum": 1,
                            "maximum": 20,
                            "help": "Enter the count of Ping requests PRTG will send to the device during an interval"
                        }
                    ]
                }
            ]
    }
    assert_equal(test_ping.get_sensordef(), test_sensordef)

# Port
def test_port_get_kind():
    """port returns the correct kind"""
    test_port = port.Port()
    assert_equal(test_port.get_kind(), 'mpport')

def test_port_get_sensordef():
    """port returns correct definition"""
    test_port = port.Port()
    test_sensordef = {
            "kind": test_port.get_kind(),
            "name": "Port",
            "description": "Monitors the availability of a port or port range on a target system",
            "help": "test",
            "tag": "mpportsensor",
            "groups": [
                {
                    "name": " portspecific",
                    "caption": "Port specific",
                    "fields": [
                        {
                            "type": "integer",
                            "name": "timeout",
                            "caption": "Timeout (in s)",
                            "required": "1",
                            "default": 60,
                            "minimum": 1,
                            "maximum": 900,
                            "help": "If the reply takes longer than this value the request is aborted "
                                    "and an error message is triggered. Max. value is 900 sec. (=15 min.)"
                        },
                        {
                            "type": "integer",
                            "name": "targetport",
                            "caption": "Port",
                            "required": "1",
                            "default": 110,
                            "minimum": 1,
                            "maximum": 65534,
                            "help": ""
                        }
                    ]
                }
            ]
    }
    assert_equal(test_port.get_sensordef(), test_sensordef)

# Portrange
def test_portrange_get_kind():
    """portrange returns the correct kind"""
    test_portrange = portrange.Portrange()
    assert_equal(test_portrange.get_kind(), 'mpportrange')

def test_portrange_get_sensordef():
    """portrange returns correct definition"""
    test_portrange = portrange.Portrange()
    test_sensordef = {
            "kind": test_portrange.get_kind(),
            "name": "Port Range",
            "description": "Checks the availability of a port range on a target system",
            "help": "Checks the availability of a port range on a target system",
            "tag": "mpportrangesensor",
            "groups": [
                {
                    "name": " portspecific",
                    "caption": "Port specific",
                    "fields": [
                        {
                            "type": "integer",
                            "name": "timeout",
                            "caption": "Timeout (in s)",
                            "required": "1",
                            "default": 60,
                            "minimum": 1,
                            "maximum": 900,
                            "help": "If the reply takes longer than this value the request is aborted "
                                    "and an error message is triggered. Max. value is 900 sec. (=15 min.)"
                        },
                        {
                            "type": "integer",
                            "name": "startport",
                            "caption": "Port",
                            "required": "1",
                            "default": 110,
                            "minimum": 1,
                            "maximum": 65534,
                            "help": "Specify the port ranges starting port"
                        },
                        {
                            "type": "integer",
                            "name": "endport",
                            "caption": "Port",
                            "required": "1",
                            "default": 110,
                            "minimum": 1,
                            "maximum": 65534,
                            "help": "Specify the port ranges end port"
                        }
                    ]
                }
            ]
    }
    assert_equal(test_portrange.get_sensordef(), test_sensordef)

# Probehealth
def test_probehealth_get_kind():
    """probehealth returns the correct kind"""
    test_probehealth = probehealth.Probehealth()
    assert_equal(test_probehealth.get_kind(), 'mpprobehealth')

def test_probehealth_get_sensordef():
    """probehealth returns correct definition"""
    test_probehealth = probehealth.Probehealth()
    test_sensordef = {
            "kind": test_probehealth.get_kind(),
            "name": "Probe Health",
            "description": "Internal sensor used to monitor the health of a PRTG probe",
            "default": "yes",
            "help": "Internal sensor used to monitor the health of a PRTG probe",
            "tag": "mpprobehealthsensor",
            "groups": [
                {
                    "name": "Group",
                    "caption": "Temperature settings",
                    "fields": [
                        {
                            "type": "radio",
                            "name": "celfar",
                            "caption": "Choose between Celsius or Fahrenheit display",
                            "help": "Choose wether you want to return the value in Celsius or Fahrenheit",
                            "options": {
                                "C": "Celsius",
                                "F": "Fahrenheit"
                            },
                            "default": "C"
                        },
                        {
                            "type": "integer",
                            "name": "maxtemp",
                            "caption": "Error temperature",
                            "required": "1",
                            "minimum": 20,
                            "maximum": 75,
                            "help": "Set the maximum temperature above which the temperature sensor will provide a error (not below 20 or above 75)",
                            "default": 45
                        },
                    ]
                }
            ]
    }
    assert_equal(test_probehealth.get_sensordef(), test_sensordef)




