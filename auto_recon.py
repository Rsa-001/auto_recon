import os
import sys
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
WORDLIST = "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt"
EXTENSIONS = ".php,.html,.txt"
THREADS = 200
DEPTH = 5
FFUF_JSON = "ffuf.json"

TOOLS = {
    "subfinder": "subfinder -d {domain} -silent",
    "nmap": "nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn {domain}",
    "whatweb": "whatweb {domain}"
}

def is_tool_installed(name):
    return subprocess.call(f"type {name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def run_command(name, cmd, outfile, index, total):
    print(f"[{index}/{total}] Running {name}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        with open(outfile, "w") as f:
            f.write(result.stdout)
        print(f"[+] {name} completed.")
    except Exception as e:
        print(f"[!] Error in {name}: {e}")

def create_output_dir(domain):
    path = f"recon-{domain}"
    os.makedirs(path, exist_ok=True)
    return path

def run_ffuf(base_url, output_json):
    cmd = (
        f"ffuf -u {base_url}/FUZZ -w {WORDLIST} -e {EXTENSIONS} "
        f"-recursion -recursion-depth {DEPTH} -t {THREADS} -of json -o {output_json}"
    )
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def extract_urls_from_json(json_file):
    urls = set()
    if not os.path.exists(json_file):
        return urls

    with open(json_file, "r") as f:
        data = json.load(f)
        for result in data.get("results", []):
            url = result.get("url", "")
            status = result.get("status", 0)
            if url and status in [200, 301]:
                urls.add(url)
    return sorted(urls)

def ffuf_wrapper(domain, output_dir, index, total):
    print(f"[{index}/{total}] Running ffuf...")
    output_json = os.path.join(output_dir, FFUF_JSON)
    base_url = f"http://{domain}"
    run_ffuf(base_url, output_json)

    urls = extract_urls_from_json(output_json)
    with open(os.path.join(output_dir, "ffuf_urls.txt"), "w") as out:
        for url in urls:
            out.write(url + "\n")

    if os.path.exists(output_json):
        os.remove(output_json)

    print(f"[+] ffuf completed.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 auto_recon.py <target>")
        sys.exit(1)

    domain = sys.argv[1]
    output_dir = create_output_dir(domain)

    print("[*] Checking required tools...")
    required = ["subfinder", "nmap", "whatweb", "ffuf"]
    for tool in required:
        if not is_tool_installed(tool):
            print(f"[!] The tool '{tool}' is not installed.")
            sys.exit(1)

    tasks = {
        "subfinder": (
            TOOLS["subfinder"].format(domain=domain),
            f"{output_dir}/subfinder.txt"
        ),
        "nmap": (
            TOOLS["nmap"].format(domain=domain),
            f"{output_dir}/nmap.txt"
        ),
        "whatweb": (
            TOOLS["whatweb"].format(domain=domain),
            f"{output_dir}/whatweb.txt"
        )
    }

    total = len(tasks) + 1
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i, (name, (cmd, outfile)) in enumerate(tasks.items(), start=1):
            futures.append(executor.submit(run_command, name, cmd, outfile, i, total))

        futures.append(executor.submit(ffuf_wrapper, domain, output_dir, total, total))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[!] Error while running task: {e}")

    print(f"\nAll tasks completed. Results saved in: {output_dir}")

if __name__ == "__main__":
    main()
