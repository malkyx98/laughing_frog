import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mobile Laughing Frog", layout="wide")

# Hide Streamlit UI elements and ensure the container takes full height
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stSidebar"], #MainMenu {display: none;}
    .block-container { 
        padding: 0 !important; 
        margin: 0 !important; 
        background: #1a1a1a !important; 
        height: 100vh !important; 
        overflow: hidden;
    }
    iframe { border: none !important; width: 100vw !important; height: 100vh !important; }
    </style>
    """, unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Fredoka+One&family=VT323&display=swap');
        
        body, html { 
            margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; 
            background: #1a1a1a; font-family: 'Fredoka One', cursive; user-select: none;
            touch-action: manipulation;
        }

        #stage {
            position: relative; width: 100vw; height: 100vh;
            background: linear-gradient(180deg, #2d5a27 0%, #1a1a1a 100%);
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
            padding-top: env(safe-area-inset-top);
        }

        /* Speech Bubble - Responsive Width */
        #speech-wrap {
            position: absolute; top: 5%; width: 100%; display: flex; justify-content: center; z-index: 100;
        }
        #bubble {
            background: #fff; border: 4px solid #000; padding: 15px; border-radius: 20px;
            width: 85%; max-width: 400px; font-size: clamp(16px, 4vw, 24px); 
            color: #000; text-align: center;
            box-shadow: 10px 10px 0px rgba(0,0,0,0.5); display: none; 
            animation: pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes pop { 0% { transform: scale(0); } 100% { transform: scale(1); } }

        /* Math UI Area - Centered and Scaled */
        #ui-layer {
            position: relative; z-index: 50; display: flex; flex-direction: column; 
            align-items: center; width: 90%; margin-top: 25vh;
        }
        .monitor {
            background: #000; border: 6px solid #555; padding: 20px; border-radius: 10px;
            box-shadow: inset 0 0 15px #39ff14, 0 6px 0 #333; margin-bottom: 20px;
            width: 100%; box-sizing: border-box; text-align: center;
        }
        #calc-text { 
            font-family: 'VT323', monospace; color: #39ff14; 
            font-size: clamp(40px, 12vw, 80px); text-shadow: 0 0 10px #39ff14; 
        }

        .btn-grid { 
            display: grid; grid-template-columns: repeat(2, 1fr); 
            gap: 15px; width: 100%; 
        }
        .ans-btn {
            background: #ff4d6d; color: #fff; padding: 15px; 
            font-size: clamp(20px, 6vw, 36px);
            border: 4px solid #000; border-radius: 12px; cursor: pointer;
            font-family: 'Bungee'; box-shadow: 0 6px 0 #800020; transition: 0.1s;
        }
        .ans-btn:active { transform: translateY(4px); box-shadow: 0 0px 0 #800020; }

        canvas { position: absolute; inset: 0; z-index: 5; pointer-events: none; }

        #starter {
            position: absolute; inset: 0; background: #22c55e; z-index: 200;
            display: flex; flex-direction: column; align-items: center; justify-content: center; 
            color: white; text-align: center; padding: 20px;
        }
        #starter h1 { font-size: clamp(40px, 10vw, 80px); margin: 0; text-shadow: 4px 4px 0 #064e3b; }
    </style>
</head>
<body>

<div id="starter">
    <h1>LAUGHING FROG</h1>
    <p style="font-size: 20px;">SHITTY MATH EDITION</p>
    <button class="ans-btn" style="background:#fbbf24; margin-top:30px; color:#000;" onclick="core.init()">START ROASTING</button>
</div>

<div id="stage">
    <div id="speech-wrap"><div id="bubble"></div></div>
    <div id="ui-layer" style="display:none">
        <div class="monitor"><div id="calc-text">2 + 2</div></div>
        <div class="btn-grid" id="options"></div>
    </div>
    <canvas id="canvas"></canvas>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const bubble = document.getElementById('bubble');

const core = {
    running: false,
    frame: 0,
    answer: 0,
    level: 1,
    particles: [],
    frog: { x: 0, y: 0, state: 'idle', jumpY: 0, rot: 0, sizeBase: 0 },
    
    shittyQuotes: [
        "I have 14 toes and none of them are mine.",
        "Your math is okay, but your haircut is a crime.",
        "I just licked a bus seat. 10/10 experience.",
        "Your brain is basically a damp sponge.",
        "I sleep in a bucket of mayonnaise.",
        "I'm 30% water and 70% pure confusion.",
        "Your math skills are almost as good as my toe fungus.",
        "I eat flies because they taste like regret.",
        "I'm sweating. I don't think I'm supposed to do that.",
        "I'm a frog. What's your excuse?",
        "Stop clickin' and start ribbitin'."
    ],

    init() {
        document.getElementById('starter').style.display = 'none';
        document.getElementById('ui-layer').style.display = 'flex';
        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.newMath();
        this.running = true;
        this.animate();
    },

    resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        this.frog.x = canvas.width / 2;
        // Frog stays near the bottom, adjusted for mobile height
        this.frog.y = canvas.height * 0.85;
        this.frog.sizeBase = Math.min(canvas.width * 0.3, 120);
    },

    newMath() {
        const a = Math.floor(Math.random() * (10 + this.level)) + 1;
        const b = Math.floor(Math.random() * (10 + this.level)) + 1;
        this.answer = a + b;
        document.getElementById('calc-text').innerText = `${a} + ${b}`;
        
        let pool = [this.answer];
        while(pool.length < 4) {
            let fake = this.answer + (Math.floor(Math.random() * 10) - 5);
            if(fake > 0 && !pool.includes(fake)) pool.push(fake);
        }
        pool.sort(() => Math.random() - 0.5);

        const grid = document.getElementById('options');
        grid.innerHTML = '';
        pool.forEach(val => {
            const b = document.createElement('button');
            b.className = 'ans-btn';
            b.innerText = val;
            b.onclick = () => this.check(val);
            grid.appendChild(b);
        });
    },

    check(val) {
        if(val === this.answer) {
            this.level++;
            this.frog.state = 'laugh';
            this.frog.jumpY = -60;
            this.triggerRoast();
            this.spawnExplosion();
            setTimeout(() => {
                this.frog.state = 'idle';
                bubble.style.display = 'none';
                this.newMath();
            }, 3000);
        } else {
            this.frog.state = 'angry';
            bubble.innerText = "WRONG. You're a disappointment to frogs.";
            bubble.style.display = 'block';
            setTimeout(() => {
                this.frog.state = 'idle';
                bubble.style.display = 'none';
            }, 1000);
        }
    },

    triggerRoast() {
        bubble.innerText = this.shittyQuotes[Math.floor(Math.random() * this.shittyQuotes.length)];
        bubble.style.display = 'block';
    },

    spawnExplosion() {
        for(let i=0; i<15; i++) {
            this.particles.push({
                x: this.frog.x, y: this.frog.y - 30,
                vx: (Math.random() - 0.5) * 15,
                vy: (Math.random() - 0.5) * 15,
                life: 1, rot: Math.random() * 6,
                icon: ['💩', '🧼', '✨', '🤣'][Math.floor(Math.random() * 4)],
                size: 20 + Math.random() * 20
            });
        }
    },

    update() {
        this.frame++;
        this.frog.jumpY *= 0.85;
        this.frog.rot = Math.sin(this.frame * 0.05) * 0.05;

        for(let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            p.x += p.vx; p.y += p.vy; p.vy += 0.5;
            p.life -= 0.02; p.rot += 0.1;
            if(p.life <= 0) this.particles.splice(i, 1);
        }
    },

    draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for(let p of this.particles) {
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot);
            ctx.globalAlpha = p.life;
            ctx.font = `${p.size}px Arial`;
            ctx.fillText(p.icon, 0, 0);
            ctx.restore();
        }

        ctx.save();
        ctx.translate(this.frog.x, this.frog.y + this.frog.jumpY);
        ctx.rotate(this.frog.rot);
        
        let bounce = Math.sin(this.frame * 0.1) * 3;
        if(this.frog.state === 'laugh') bounce = Math.sin(this.frame * 0.5) * 10;

        const s = this.frog.sizeBase;

        // Body
        ctx.fillStyle = '#22c55e'; ctx.strokeStyle = '#000'; ctx.lineWidth = 5;
        ctx.beginPath(); ctx.ellipse(0, bounce, s, s*0.7, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

        // Belly
        ctx.fillStyle = '#86efac';
        ctx.beginPath(); ctx.ellipse(0, (s*0.15) + bounce, s*0.6, s*0.4, 0, 0, Math.PI * 2); ctx.fill();

        // Eyes
        ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.arc(-s*0.4, -s*0.6 + bounce, s*0.28, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.arc(s*0.4, -s*0.6 + bounce, s*0.28, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        
        ctx.fillStyle = '#000';
        let eyeSize = (this.frog.state === 'laugh') ? s*0.04 : s*0.1;
        ctx.beginPath(); ctx.arc(-s*0.4, -s*0.6 + bounce, eyeSize, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(s*0.4, -s*0.6 + bounce, eyeSize, 0, Math.PI * 2); ctx.fill();

        // Mouth
        ctx.beginPath(); ctx.lineWidth = 4;
        if(this.frog.state === 'laugh') {
            ctx.fillStyle = '#991b1b'; ctx.arc(0, s*0.07 + bounce, s*0.4, 0, Math.PI); ctx.fill();
        } else if(this.frog.state === 'angry') {
            ctx.moveTo(-s*0.35, s*0.07 + bounce); ctx.lineTo(s*0.35, s*0.07 + bounce);
        } else {
            ctx.arc(0, -s*0.07 + bounce, s*0.35, 0.4, Math.PI - 0.4);
        }
        ctx.stroke();
        ctx.restore();
    },

    animate() {
        if(!this.running) return;
        this.update();
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
};
</script>
</body>
</html>
"""

components.html(game_code, height=1000)
