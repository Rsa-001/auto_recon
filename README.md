# auto_recon
Automated recon tool for CTFs and pentesting

A fast and modular automated reconnaissance tool for pentesters and CTF players.  
It combines basic recon tools with recursive web fuzzing using [ffuf](https://github.com/ffuf/ffuf), saving only clean and valid URLs (status 200/301).

---

## 🔧 Features

- 🔍 Port scanning with **nmap**
- 🌐 Subdomain discovery with **subfinder**
- 🧠 Web fingerprinting with **whatweb**
- 🚀 Recursive web fuzzing with **ffuf**
- 🧼 Only valid URLs are extracted and saved

---

## 📦 Requirements

- Python 3
- [`ffuf`](https://github.com/ffuf/ffuf)
- [`nmap`](https://nmap.org/)
- [`whatweb`](https://github.com/urbanadventurer/WhatWeb)
- [`subfinder`](https://github.com/projectdiscovery/subfinder)

You also need [SecLists](https://github.com/danielmiessler/SecLists) installed, because this tool uses:
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt


## Install tools on a Debian-based system:

```bash
sudo apt install ffuf nmap whatweb jq
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

Usage:
```python
python3 auto_recon.py <target>
```

Example:
```python
python3 auto_recon.py 10.10.10.185
```

📁 Output
Results are saved in a folder named after the target:

recon-10.10.10.185/
├── nmap.txt
├── subfinder.txt
├── whatweb.txt
└── ffuf_urls.txt     ✅ Clean valid URLs only


## Disclaimer
This tool is intended for educational and authorized testing only.
Do NOT use it against systems without explicit permission.
