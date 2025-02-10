# CORSMANIC

**CORSMANIC** is an automated tool for detecting and exploiting Cross-Origin Resource Sharing (CORS) vulnerabilities. It scans target APIs for misconfigurations, generates an exploit script, and sets up an exfiltration server using Flask and Ngrok. This makes it a powerful tool for security researchers and bug bounty hunters.

## Features
- 🔍 **Automated CORS Misconfiguration Detection**: Scans provided API URLs and identifies vulnerable endpoints.
- 🚀 **Exploit Script Generation**: Creates a JavaScript payload to extract sensitive data from vulnerable targets.
- 🌐 **Ngrok Integration**: Tunnels requests for remote exfiltration.
- 🛠 **Flask Backend**: Acts as a listener to receive stolen data.
- 🛑 **Graceful Exit Handling**: Stops Flask and Ngrok properly upon termination.

## Installation

Ensure you have **Python 3**, **pip**, and **Ngrok** installed.

```sh
# Clone the repository
git clone https://github.com/amrendra1111/corsmanic.git
cd corsmanic

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Run the tool:**
   ```sh
   python corsmanic.py
   ```
2. **Enter the target API URL** when prompted.
3. If the API is vulnerable, CORSMANIC will:
   - Start a Flask server
   - Start an Ngrok tunnel
   - Generate an exploit script (`exploit.js`)
4. **Inject the generated script** into a vulnerable web page.
5. View exfiltrated data on the Flask server.

## Example Output
```
[+] Starting Flask server...
[+] Starting Ngrok tunnel...
[+] Ngrok URL: https://example.ngrok-free.app
[+] Scanning https://target.com/api/data for CORS vulnerabilities...
[+] Vulnerable API found: https://target.com/api/data
[+] Exploit script generated: exploit.js
[+] CORSMANIC is running! Inject exploit.js into your target.
```

## Future Enhancements
✅ Multi-target scanning (scan multiple URLs at once)  
✅ Advanced payload customization  
✅ Support for other exfiltration methods (e.g., WebSockets)  

## Disclaimer
This tool is for educational and authorized penetration testing purposes only. Unauthorized use against systems you do not own is illegal.

---

⚡ **GitHub Repo:** [your-github-link]
📢 **Follow me on LinkedIn for more security tools!**

