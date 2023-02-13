# DNSMod
Fastest and easiest tool to update system wide *DNS* with help of some predefined providers. 
 - [Shecan](https://shecan.ir/)
 - [Cloudflare](https://www.cloudflare.com/dns/)
 - [Google](https://developers.google.com/speed/public-dns/)
 - [OpenDNS](https://www.opendns.com/)
 - [AdGuard](https://adguard-dns.io/en/public-dns.html)
 - [403](https://403.online/download)
 - ...
<br>

### Usage:

To change DNS to Shecan:
```bash
sudo dnsmod -p Shecan
```

```bash
```

```
options:
  -h, --help            show this help message and exit
  -p {Shecan,Cloudflare,Google,OpenDNS,AdGuard,403}, --provider {Shecan,Cloudflare,Google,OpenDNS,AdGuard,403}
                        Choose a DNS provider from Shecan, Cloudflare, Google, OpenDNS, AdGuard, 403
  -s DNS1 DNS2, --set DNS1 DNS2
                        Set custom DNS
  -c, --check           Check current DNS config
  -t, --test            Test connection
  -r, --restore         Restore DNS
  -u, --update          Update DNSMod
  -v, --version         Show version
```

# Install/Update with one simple command:

```bash
curl -sfL https://raw.githubusercontent.com/smb-h/dnsmod/main/install.sh | sudo bash -
```

# Dependencies
1. python 3
2. python 3 requests library

# TODO
- [ ] Add more providers
- [ ] Add MacOS support
- [ ] Add Windows support
- [ ] Add update functionality (arguments: -u, --update)
- [ ] Make messages colorful (warnings in yellow, errors in red, success in green)


# LICENSE
Project is under GPL3.


Inspired by [Ali](https://github.com/ali77gh/shecan-cli)
