
# JASS V2 - No Nmap needed, only PING + ARP - 100% works
import flask
from flask import Flask, request, jsonify, render_template_string
import subprocess, socket, platform, threading, time, requests, os, json
from datetime import datetime

app = Flask(__name__)
clients = {}
API_KEY = "JASS-123"
SERVER_PORT = 5000

HTML = """
<!DOCTYPE html><html><head><title>JASS V2</title>
<style>body{font-family:Segoe UI;background:#0f172a;color:#e2e8f0;padding:20px}.card{background:#1e293b;padding:16px;border-radius:14px;margin:12px 0;border:1px solid #334155}button{background:#3b82f6;color:white;border:0;padding:8px 16px;border-radius:8px;cursor:pointer;margin:2px}button.green{background:#22c55e}input{padding:9px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:white;width:300px}table{width:100%;border-collapse:collapse}th,td{padding:10px;border-bottom:1px solid #334155;text-align:left;font-size:13px}.badge{padding:3px 8px;border-radius:20px;font-size:11px}.online{background:#22c55e22;color:#22c55e}.offline{background:#ef444422;color:#ef4444}pre{background:#0f172a;padding:12px;border-radius:8px;max-height:400px;overflow:auto;font-size:12px}</style>
</head><body>
<h1>🖥️ JASS V2 - No Nmap Manager</h1><p>My IP: {{my_ip}} | Found: <span id="cnt">0</span></p>
<div class="card"><h3>1. Network Scan</h3>
<p style="font-size:12px">Tumhara Network: 200.9.92.0/24 (200.9.92.1 se 200.9.92.254 tak)</p>
<button onclick="pingScan()" style="background:#22c55e;padding:12px 20px;font-size:15px">🚀 Start Ping Scan (200.9.92.0/24)</button>
<button onclick="arpScan()">⚡ ARP Scan</button>
<pre id="out">Scan dabao, 10-15 sec lagega...</pre></div>
<div class="card"><h3>2. Live Systems</h3><button onclick="load()">Refresh</button><div id="tbl"></div></div>
<div class="card"><h3>3. Remote Install</h3><input id="pkg" placeholder="Google.Chrome"><input id="tip" placeholder="Target IP"><button class="green" onclick="inst()">Install</button><pre id="instOut"></pre></div>
<script>
async function pingScan(){
 document.getElementById('out').innerText='Scanning 200.9.92.1-254 via PING... please wait 15 sec...';
 let r=await fetch('/api/ping_scan'); let d=await r.json();
 document.getElementById('out').innerText=d.log; load();
}
async function arpScan(){
 document.getElementById('out').innerText='ARP Scanning...';
 let r=await fetch('/api/arp_scan'); let d=await r.json();
 document.getElementById('out').innerText=d.output; load();
}
async function load(){
 let r=await fetch('/api/clients'); let data=await r.json();
 document.getElementById('cnt').innerText=Object.keys(data).length;
 let html='<table><tr><th>IP</th><th>Hostname</th><th>Status</th><th>Ping</th><th>Software</th><th>Action</th></tr>';
 for(let ip in data){ let c=data[ip]; let st=c.online?'<span class=badge online>Client OK</span>':'<span class=badge offline>Found (No Client)</span>';
  html+=`<tr><td><b>${ip}</b></td><td>${c.hostname||'-'}</td><td>${st}</td><td>${c.ping||'-'}</td><td>${c.software?c.software.length:0}</td><td><button onclick="viewS('${ip}')">View SW</button> <button class=green onclick="document.getElementById('tip').value='${ip}'">Select</button></td></tr>`;
 } html+='</table>'; document.getElementById('tbl').innerHTML=html;
}
async function viewS(ip){ let r=await fetch('/api/clients'); let d=await r.json(); let sw=d[ip]?.software||[]; if(!sw.length) alert('Is PC pe client nahi chal raha. Wahan bhi yehi file chalao.'); else alert(sw.slice(0,100).map(s=>s.Name).join('\n').substring(0,6000)); }
async function inst(){ let pkg=document.getElementById('pkg').value; let ip=document.getElementById('tip').value; if(!pkg||!ip) return alert('dono bharo'); let r=await fetch('/api/install',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ip:ip,package_id:pkg})}); document.getElementById('instOut').innerText=JSON.stringify(await r.json(),null,2); }
setInterval(load,4000); load();
</script></body></html>
"""

def my_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close(); return ip
    except: return "200.9.92.7"

def get_sw():
    sw=[]
    try:
        out=subprocess.check_output("winget list", shell=True, text=True, encoding='utf-8', errors='ignore', timeout=20)
        for line in out.splitlines()[5:]:
            if line.strip() and '---' not in line and len(line)>5:
                sw.append({"Name": line[:60].strip(), "Version": line[60:80].strip()})
        return sw[:200]
    except Exception as e:
        return [{"Name": str(e)}]

def check_client(ip):
    try:
        r=requests.get(f"http://{ip}:{SERVER_PORT}/info", timeout=1.5)
        d=r.json()
        if ip in clients:
            clients[ip].update({"hostname": d.get('hostname', clients[ip].get('hostname')), "software": d.get('software',[]), "online": True, "last_seen": datetime.now().strftime("%H:%M:%S")})
    except:
        if ip in clients:
            clients[ip]['online']=False

def ping_sweep(base="200.9.92"):
    log=[]
    log.append(f"Starting ping sweep {base}.1-254")
    # Clear old but keep
    found=[]
    def ping_one(i):
        ip=f"{base}.{i}"
        try:
            # Windows ping -n 1 -w 500
            res=subprocess.call(f"ping -n 1 -w 300 {ip}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res==0:
                found.append(ip)
                hostname=""
                try: hostname=socket.gethostbyaddr(ip)[0]
                except: pass
                clients[ip]={"ip": ip, "hostname": hostname or f"PC-{i}", "online": False, "software": [], "ping": "OK", "last_seen": datetime.now().strftime("%H:%M:%S")}
                threading.Thread(target=check_client, args=(ip,), daemon=True).start()
                log.append(f"[+] Found {ip} {hostname}")
        except: pass

    threads=[]
    for i in range(1,255):
        t=threading.Thread(target=ping_one, args=(i,))
        t.start()
        threads.append(t)
        if len(threads)>50: # limit concurrency
            for tt in threads: tt.join(timeout=0.1)
            threads=[tt for tt in threads if tt.is_alive()]
    for t in threads: t.join()
    log.append(f"Scan complete. Found {len(found)} IPs: {', '.join(found)}")
    return "\n".join(log), found

@app.route('/')
def home(): return render_template_string(HTML, my_ip=my_ip())

@app.route('/api/clients')
def get_clients(): return jsonify(clients)

@app.route('/api/ping_scan')
def api_ping():
    base=request.args.get('base','200.9.92')
    log,found=ping_sweep(base)
    return jsonify({"log": log, "found": found})

@app.route('/api/arp_scan')
def api_arp():
    try:
        out=subprocess.check_output("arp -a", shell=True, text=True, encoding='utf-8', errors='ignore')
        ips=[]
        for line in out.splitlines():
            # 200.9.92.x format
            import re
            m=re.findall(r'(\d+\.\d+\.\d+\.\d+)', line)
            for ip in m:
                if ip.startswith("200.9.92.") and ip!="200.9.92.7":
                    if ip not in clients:
                        clients[ip]={"ip": ip, "hostname": "", "online": False, "software": [], "ping": "ARP", "last_seen": datetime.now().strftime("%H:%M:%S")}
                        threading.Thread(target=check_client, args=(ip,), daemon=True).start()
                    ips.append(ip)
        return jsonify({"output": out + f"\n\nFound {len(ips)} relevant: {ips}", "ips": ips})
    except Exception as e:
        return jsonify({"output": str(e)})

@app.route('/api/install', methods=['POST'])
def api_install():
    data=request.json
    ip=data.get('ip'); pkg=data.get('package_id')
    try:
        r=requests.post(f"http://{ip}:{SERVER_PORT}/install", json={"package_id": pkg}, timeout=5)
        return jsonify({"message": f"Sent to {ip}", "resp": r.json()})
    except Exception as e:
        return jsonify({"message": f"Failed - Client not running on {ip}. Wahan bhi yehi file chalao. Error: {e}"})

@app.route('/info')
def info():
    return jsonify({"hostname": socket.gethostname(), "os": platform.platform(), "software": get_sw()})

@app.route('/install', methods=['POST'])
def install():
    pkg=request.json.get('package_id')
    def do():
        try: subprocess.call(f'winget install --id {pkg} --silent --accept-package-agreements --accept-source-agreements', shell=True)
        except: pass
    threading.Thread(target=do, daemon=True).start()
    return jsonify({"status":"installing", "pkg": pkg})

if __name__=='__main__':
    print(f"JASS V2 Started on {my_ip()}:{SERVER_PORT}")
    app.run(host='0.0.0.0', port=SERVER_PORT)
