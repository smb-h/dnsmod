# DNSMod
Fastest and easiest tool to update system wide *DNS* with help of some predefined providers. 
 - [Shecan](https://shecan.ir/)
 - [Cloudflare](https://www.cloudflare.com/)
 - ...
<br>

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
2. python 3 requests library

# LICENSE
Project is under GPL3


Inspired from [Ali](https://github.com/ali77gh/shecan-cli)
