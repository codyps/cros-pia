#!/bin/bash

# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

set -euo pipefail

BASE_URL="https://www.privateinternetaccess.com/openvpn"
OUT="cros-pia.zip"

case "${1:-}" in
	--pia-ip)
		URL="$BASE_URL/openvpn-ip.zip"
		shift
		;;
# ONC doesn't handle "lport"
#	--pia-ip-lport)
#		URL="$BASE_URL/openvpn-ip-lport.zip"
#		shift
#		;;
	--pia-tcp)
		URL="$BASE_URL/openvpn-tcp.zip"
		shift
		;;
	--pia-ip-tcp)
		URL="$BASE_URL/openvpn-ip-tcp.zip"
		shift
		;;
	*)
		URL="$BASE_URL/openvpn.zip"
		;;
esac

rm -rf tmp
mkdir tmp
cd tmp
if ! curl -L "$URL" > ovpn.zip; then
	echo "error: can't download $URL"
	exit 1
fi

unzip ovpn.zip
../ovpn_to_onc.py "$@" *.ovpn

rm -f "../$OUT"
zip "../$OUT" *.onc

cd ..
rm -rf tmp

echo "Wrote $OUT"

exit 0
