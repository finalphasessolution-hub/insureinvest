const http=require('http'),fs=require('fs'),path=require('path');http.createServer((q,s)=>{let f=path.join(__dirname,q.url==='/'?'index.html':q.url);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f=path.join(__dirname,'index.html');fs.readFile(f,(e,d)=>{if(e){s.writeHead(404);s.end()}else{s.writeHead(200,{'Content-Type':'text/html'});s.end(d)}})}).listen(8081,()=>console.log('ADMIN'));

