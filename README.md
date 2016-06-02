Quick start
===========

This project lets you set up OpenVPN profiles for privateinternetaccess.com
in Chrome OS with minimal fuss.  It does not require enabling developer
mode.

Short link to this page: <http://tinyurl.com/cros-pia>

1. Download the "prebuilt"
[cros-pia.zip](https://docs.google.com/uc?id=0B-U-1pC_l1hRMGZtck95Mndza1E&export=download)
to your Chromebook.

2. Click "Show in folder," or open the File Manager with Alt-Shift-M.  Then
double-click on the zip file to mount it.

3. Enter `chrome://net-internals/#chromeos` in the location bar, hit enter,
and click "Choose File" under "Import ONC File."

4. Double-click ALL.onc (to import configurations for all servers), or
import individual VPN configuration(s) one at a time.

5. Click on the Tray &rarr; VPN &rarr; one of the PIA configurations.

6. Fill in Username and Password using your normal PIA (*not* L2TP)
credentials.  Always leave OTP blank.


Troubleshooting
===============

If import failed, scroll down to the end of `file:///var/log/ui/ui.LATEST`
and look for any errors.  (The net-internals UI doesn't provide a whole
lot of feedback, unfortunately.)

If your connection fails, do the same for `file:///var/log/net.log`

To delete VPN configurations:

1. Navigate to `chrome://settings/network`

2. Select Private Network &rarr; Preferred networks.

3. Click the "X" icon on the right side of each configuration you want to
delete.


Rebuilding the ONC files by hand
================================

First, clone this repo on a Linux machine:

`git clone https://chromium.googlesource.com/experimental/cros-pia`

Then run `./build_all.sh` to download the default OpenVPN configuration
files from
[the official PIA site](https://www.privateinternetaccess.com/pages/client-support/),
convert them into ONC format, and create `cros-pia.zip` in the current
directory.

To embed your PIA credentials into the generated `cros-pia.zip` so that
you never need to manually enter them on the Chromebook, use:

`./build_all.sh -u "USERNAME" -p "PASSWORD"`

To manually convert a single configuration, use:

`./ovpn_to_onc.py "US California.ovpn"`

To download an alternate set of OVPN files, specify the appropriate flag as
the first argument:

`./build_all.sh --pia-tcp`

The supported flags are:

 * `--pia-ip`: Connect via IP address instead of server hostname.
 * `--pia-tcp`: Connect over 443/tcp instead of 1194/udp.
 * `--pia-ip-tcp`: Same as above, but connect via IP address.


Limitations and notes
=====================

To avoid IP address leaks, install the
[WebRTC Leak Prevent extension](https://chrome.google.com/webstore/detail/webrtc-leak-prevent/eiadekoaikejlgdbkbdfeijglgfdalml?hl=en) and then run the
<https://ipleak.net> tests to double-check.

ONC does not currently support the certificate revocation list (CRL)
bundled with the PIA .ovpn files.

The converter only handles the fields that are relevant for PIA; it is
not a general purpose OVPN&rarr;ONC converter.

PIA's official site does not currently offer ONC files for download, but
if enough Chromebook users bug them about it, maybe they will reconsider.


Further reading
===============

The file format is defined in the [ONC specification](https://chromium.googlesource.com/chromium/chromium/+/0142427081581becff601f489e9b5cb9f53c5a5d/components/onc/docs/onc_spec.html).

(To get a copy in .html format, click the "txt" link at the bottom and run
`base64 -d` on it.  This is a workaround for a
[gitiles limitation](https://code.google.com/p/gitiles/issues/detail?id=7).)

The original OpenVPN ONC walkthrough document can be found [here](https://docs.google.com/document/d/18TU22gueH5OKYHZVJ5nXuqHnk2GN6nDvfu2Hbrb4YLE/pub).
