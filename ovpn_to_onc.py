#!/usr/bin/env python2

# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse, json, md5, os, re, sys, uuid

def read_cert(filename):
    # Assumes this is a valid PEM-encoded cert. If it contains e.g.
    # quotes, all bets are off.
    f = open(filename, "r")
    data = ""
    for line in f:
        # force CRLF -> LF
        data += line.rstrip() + "\n"
    f.close()
    return data

def write_onc(prefix, certs, configs):
    certlist = [ ]
    for guid in sorted(certs.keys()):
        certlist += [ certs[guid] ]

    configlist = [ ]
    for guid in sorted(configs.keys()):
        configlist += [ configs[guid] ]

    onc = {
        "Type": "UnencryptedConfiguration",
        "Certificates": certlist,
        "NetworkConfigurations": configlist
    }

    outfile = open(prefix + ".onc", "w")
    json.dump(onc, outfile, sort_keys=True, indent=4)
    outfile.write("\n")
    outfile.close()

# main

parser = argparse.ArgumentParser(
        description="Convert .ovpn files to .onc format")
parser.add_argument("ovpn_file", nargs='+',
                    help="an .ovpn file to convert")
parser.add_argument("--username", "-u",
                    help="hardcoded username to add to each entry")
parser.add_argument("--password", "-p",
                    help="hardcoded password to add to each entry")
args = vars(parser.parse_args(sys.argv[1:]))

certs = { }
configs = { }
for ovpn_file in args['ovpn_file']:
    infile = open(ovpn_file, "r")

    # rewrite suffix from .ovpn -> .onc
    m = re.match("(.*)\.ovpn", ovpn_file)
    if m:
        prefix = m.group(1)
    else:
        prefix = ovpn_file

    host = proto = port = cacert = None
    for line in infile:
        if re.match("^#", line):
            continue

        m = re.search("remote\s+(\S+)\s+(\S+)", line)
        if m:
            host = m.group(1)
            port = int(m.group(2))

        m = re.search("proto\s+(\S+)", line)
        if m:
            proto = m.group(1)

        m = re.search("ca\s+(\S+)", line)
        if m:
            cacert = read_cert(m.group(1))

    # stable UUID based on the VPN profile name (e.g. US_California)
    baseprefix = os.path.basename(prefix)
    h = md5.new(baseprefix)
    vpn_guid = str(uuid.UUID(h.hexdigest()))

    # stable UUID based on the CA cert's contents
    h = md5.new(cacert)
    cert_guid = str(uuid.UUID(h.hexdigest()))

    if re.search("privateinternetaccess", host):
        nameprefix = "PIA: "
    else:
        nameprefix = ""

    certs[cert_guid] = cert = {
        "GUID": cert_guid,
        "Type": "Authority",
        "X509": cacert
    }

    configs[baseprefix] = config = {
        "GUID": vpn_guid,
        "Name": nameprefix + baseprefix,
        "Type": "VPN",
        "VPN": {
            "Type": "OpenVPN",
            "Host": host,
            "OpenVPN": {
                "AuthRetry": "interact",
                "ClientCertType": "None",
                "CompLZO": "true",
                "Port": port,
                "Proto": proto,
                "RemoteCertTLS": "server",
                "ServerCARef": cert_guid,
                "UserAuthenticationType": "Password"
            }
        }
    }

    if args["username"]:
        config["VPN"]["Username"] = args["username"]
    if args["password"]:
        config["VPN"]["Password"] = args["password"]

    write_onc(prefix, {cert_guid: cert}, {baseprefix: config})

write_onc("ALL", certs, configs)

sys.exit(0)
