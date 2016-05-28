#!/bin/bash

# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

set -euo pipefail

URL="https://www.privateinternetaccess.com/openvpn/openvpn.zip"
OUT="cros-pia.zip"

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
