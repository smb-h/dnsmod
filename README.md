# DNSMod
Fastest and easiest tool to update system wide *DNS* with help of some predefined providers. 
 - [Shecan](https://shecan.ir/)
 - [Cloudflare](https://www.cloudflare.com/)
 - ...
<br>

### Usage:
```bash
┌────────────────────────────────────────────────────────┐
│                        DNSMod                          │
│ > https://github.com/smb-h/dnsmod                      │
│                                                        │
├────────────────────────────┬───────────────────────────┤
│ > how to use:              │                           │
│   dnsmod help              │ show this beautiful msg   │
│   dnsmod status            │ show status (local&remote)│
│   dnsmod enable            │ enables shecan DNS        │
│   dnsmod disable           │ load your old DNS config  │
│   dnsmod live_status       │ run status in loop        │
│                            │                           │
└────────────────────────────┴───────────────────────────┘

```

# Install/Update with one simple command:

```bash
curl -sfL https://raw.githubusercontent.com/smb-h/dnsmod/main/install.sh | sudo bash -
```

# Dependencies
1. python 3

# TODO
- [ ] Add more providers
- [ ] Add MacOS support
- [ ] Add Windows support
- [ ] Add restore functionality (arguments: -r, --restore) or (arguments: -d, --disable)
- [ ] Add functionality to check if current DNS is modified by DNSMod (arguments: -c, --check)
- [ ] Add update functionality (arguments: -u, --update)
- [ ] Make messages colorful (warnings in yellow, errors in red, success in green)


# LICENSE
Project is under GPL3.


Inspired by [Ali](https://github.com/ali77gh/shecan-cli)
