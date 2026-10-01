const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

if (!fs.existsSync('replies')) fs.mkdirSync('replies');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { headless: true, args: ['--no-sandbox','--disable-setuid-sandbox'] }
});

client.on('qr', qr => {
    console.log('=== QR AAYA - 9958037734 SE SCAN KAR ===');
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('READY - 9958037734');
});

client.on('message', msg => {
    const text = msg.body.trim();
    const m = text.match(/^(V\d+)\s+(.+)/);
    if (m) {
        fs.writeFileSync(path.join('replies', m[1]+'.txt'), m[2], 'utf8');
        console.log('Reply saved ' + m[1]);
    }
});

client.initialize();

app.post('/api/visitor-msg', async (req,res)=>{
    try{
        const {visitorId,message,page} = req.body;
        await client.sendMessage('919958037734@c.us', '🔔 NEW VISITOR '+visitorId+'\n📄 Page: '+page+'\n💬 Msg: '+message+'\n\nReply: '+visitorId+' <your reply>');
        console.log('Sent '+visitorId);
        res.json({ok:true});
    }catch(e){
        res.status(500).json({error:e.message});
    }
});

app.get('/api/get-reply/:vid', (req,res)=>{
    const fp = path.join('replies', req.params.vid+'.txt');
    res.json({reply: fs.existsSync(fp) ? fs.readFileSync(fp,'utf8') : null});
});

app.listen(3001, ()=> console.log('Bridge API on 3001'));
