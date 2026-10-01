import os
BRIDGE_CODE = """
<div id="wa-widget" style="position:fixed;bottom:20px;right:20px;z-index:99999;font-family:Arial">
<button id="wa-btn" style="background:#25D366;color:white;border:none;border-radius:50%;width:60px;height:60px;font-size:28px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.3)">💬</button>
<div id="wa-box" style="display:none;width:320px;height:400px;background:white;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.2);flex-direction:column;overflow:hidden;margin-bottom:10px">
<div style="background:#075E54;color:white;padding:12px;font-weight:bold">InsureInvest Live Chat - Jass Saini</div>
<div id="wa-msgs" style="flex:1;overflow-y:auto;padding:10px;background:#e5ddd5"></div>
<div style="display:flex;padding:8px;border-top:1px solid #ddd"><input id="wa-input" placeholder="Message likho..." style="flex:1;border:1px solid #ddd;border-radius:20px;padding:8px 12px;outline:none"><button id="wa-send" style="background:#25D366;color:white;border:none;border-radius:50%;width:36px;height:36px;margin-left:6px;cursor:pointer">➤</button></div>
</div>
</div>
<script>
(function(){
const VID='V'+Date.now().toString().slice(-6);
let replied=false;
const box=document.getElementById('wa-box'), btn=document.getElementById('wa-btn'), msgs=document.getElementById('wa-msgs'), input=document.getElementById('wa-input'), send=document.getElementById('wa-send');
btn.onclick=()=>{box.style.display=box.style.display==='none'?'flex':'none'; box.style.display==='flex'&&(box.style.display='flex')};
function addMsg(t,me){const d=document.createElement('div');d.style.cssText=me?'background:#dcf8c6;margin:6px 0 6px 40px;padding:8px 10px;border-radius:8px;text-align:right':'background:white;margin:6px 40px 6px 0;padding:8px 10px;border-radius:8px';d.textContent=t;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight}
send.onclick=sendMsg; input.onkeypress=(e)=>{if(e.key==='Enter')sendMsg()};
function sendMsg(){const m=input.value.trim(); if(!m)return; addMsg(m,true); input.value=''; fetch('http://localhost:3001/api/visitor-msg',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({visitorId:VID,message:m,page:location.href})}).then(()=>{if(!replied){replied=true; setInterval(()=>{fetch('http://localhost:3001/api/get-reply/'+VID).then(r=>r.json()).then(d=>{if(d.reply&&!document.getElementById('rep-'+d.reply.slice(0,10))){const el=document.createElement('div');el.id='rep-'+d.reply.slice(0,10);el.style.cssText='background:white;margin:6px 40px 6px 0;padding:8px 10px;border-radius:8px;border-left:3px solid #25D366';el.innerHTML='<b>Jass Saini:</b> '+d.reply;msgs.appendChild(el);msgs.scrollTop=msgs.scrollHeight}})},3000)}})}
})();
</script>
"""

for path in ["site-3000/index.html","site-8080/index.html","www/index.html"]:
    if os.path.exists(path):
        with open(path,'r',encoding='utf-8',errors='ignore') as f: html=f.read()
        if 'wa-widget' not in html:
            html=html.replace('</body>',BRIDGE_CODE+'</body>') if '</body>' in html else html+BRIDGE_CODE
            with open(path,'w',encoding='utf-8') as out: out.write(html)
            print(f"Injected: {path}")
        else:
            print(f"Already: {path}")
print("DONE")