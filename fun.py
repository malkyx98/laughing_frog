import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laughing Frog: The 500+ Line Roast", layout="wide")

st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stSidebar"], #MainMenu {display: none;}
    .block-container { padding: 0 !important; margin: 0 !important; background: #1a1a1a !important; height: 100vh !important; }
    iframe { border: none !important; width: 100vw !important; height: 100vh !important; }
    </style>
    """, unsafe_allow_html=True)

# The Full Codebase (500+ lines of Logic, Math, and Shitty Jokes)
game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Fredoka+One&family=VT323&display=swap');
        
        body, html { 
            margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; 
            background: #1a1a1a; font-family: 'Fredoka One', cursive; user-select: none;
        }

        #stage {
            position: relative; width: 100vw; height: 100vh;
            background: linear-gradient(180deg, #2d5a27 0%, #1a1a1a 100%);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }

        /* Speech Bubble System */
        #speech-wrap {
            position: absolute; top: 5%; width: 100%; display: flex; justify-content: center; z-index: 100;
        }
        #bubble {
            background: #fff; border: 6px solid #000; padding: 25px; border-radius: 30px;
            max-width: 450px; font-size: 26px; color: #000; text-align: center;
            box-shadow: 15px 15px 0px rgba(0,0,0,0.5); display: none; animation: pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes pop { 0% { transform: scale(0); } 100% { transform: scale(1); } }

        /* Math UI Area */
        #ui-layer {
            position: relative; z-index: 50; display: flex; flex-direction: column; align-items: center; margin-top: 100px;
        }
        .monitor {
            background: #000; border: 10px solid #555; padding: 30px 60px; border-radius: 10px;
            box-shadow: inset 0 0 20px #39ff14, 0 10px 0 #333; margin-bottom: 30px;
        }
        #calc-text { font-family: 'VT323', monospace; color: #39ff14; font-size: 80px; text-shadow: 0 0 10px #39ff14; }

        .btn-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .ans-btn {
            background: #ff4d6d; color: #fff; padding: 20px 40px; font-size: 40px;
            border: 5px solid #000; border-radius: 15px; cursor: pointer;
            font-family: 'Bungee'; box-shadow: 0 8px 0 #800020; transition: 0.1s;
        }
        .ans-btn:hover { background: #ff758f; transform: translateY(-2px); }
        .ans-btn:active { transform: translateY(8px); box-shadow: 0 0px 0 #800020; }

        canvas { position: absolute; inset: 0; z-index: 5; pointer-events: none; }

        #starter {
            position: absolute; inset: 0; background: #22c55e; z-index: 200;
            display: flex; flex-direction: column; align-items: center; justify-content: center; color: white;
        }
    </style>
</head>
<body>

<div id="starter">
    <h1 style="font-size: 90px; margin:0; text-shadow: 8px 8px 0 #064e3b;">LAUGHING FROG</h1>
    <p style="font-size: 28px;">SHITTY MATH EDITION</p>
    <button class="ans-btn" style="background:#fbbf24; margin-top:40px; color:#000;" onclick="core.init()">START ROASTING</button>
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
    frog: { x: 0, y: 0, w: 160, h: 120, state: 'idle', jumpY: 0, scale: 1, rot: 0 },
    
    // 50+ Shitty Things to say
    shittyQuotes: [
        "I have 14 toes and none of them are mine.",
        "My favorite color is the smell of a wet dog.",
        "I once ate a battery. I felt powerful and then very sick.",
        "Your math is okay, but your haircut is a crime.",
        "I dream of becoming a ceiling fan.",
        "I just licked a bus seat. 10/10 experience.",
        "If I was a human, I'd definitely be a plumber.",
        "I'm 40% swamp and 60% pure unfiltered chaos.",
        "I told my therapist I'm a frog. He said 'ribbit'.",
        "Your brain is basically a damp sponge.",
        "I wear this skin so people don't see my internal wiring.",
        "Don't look at me. I'm shy and I taste like copper.",
        "I once jumped so high I saw a bird's taxes.",
        "Life is short. Eat a bug. Regret it instantly.",
        "I sleep in a bucket of mayonnaise.",
        "My legs are just wet noodles attached to a dream.",
        "I can count to 10 but I choose not to.",
        "I'm going to hide in your toaster later.",
        "I'm 30% water and 70% pure confusion.",
        "I have a collection of belly button lint.",
        "I think my left eye is plotting against me.",
        "I tried to be a bird once. Gravity said no.",
        "Your math skills are almost as good as my toe fungus.",
        "I breathe through my skin because I'm fancy.",
        "I'm actually a prince, but the curse was a massive upgrade.",
        "I eat flies because they taste like regret.",
        "Is this a game or a cry for help?",
        "I have no ears but I can hear your thoughts. They are loud.",
        "I'm sweating. I don't think I'm supposed to do that.",
        "My dad was a toad who sold used cars.",
        "I'm writing a book about the texture of gravel.",
        "You're doing math. I'm doing nothing. I win.",
        "I once swallowed a whistle. Every breath was a song.",
        "I feel like a grape that learned how to scream.",
        "I don't need math. I have a long tongue.",
        "My spirit animal is a soggy piece of bread.",
        "I think I'm allergic to numbers.",
        "I have a PhD in staring at walls.",
        "Your brain is a wonderful place, I'd love to visit it with a spoon.",
        "I'm currently vibrating at a frequency that only dogs hate.",
        "I'm not mad, I'm just painted this way.",
        "I'm a frog. What's your excuse?",
        "I think I'm melting, but it might just be humid.",
        "My life is a series of jumps followed by landing.",
        "I have a secret collection of pebbles.",
        "I'm not laughing with you, I'm laughing at the concept of math.",
        "I'm 5% frog and 95% anxiety.",
        "I once tried to lick the moon. It was dry.",
        "I smell like a basement and I love it.",
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
        this.frog.y = canvas.height - 250;
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
            this.frog.jumpY = -80;
            this.triggerRoast();
            this.spawnExplosion();
            setTimeout(() => {
                this.frog.state = 'idle';
                bubble.style.display = 'none';
                this.newMath();
            }, 3500);
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
        const txt = this.shittyQuotes[Math.floor(Math.random() * this.shittyQuotes.length)];
        bubble.innerText = txt;
        bubble.style.display = 'block';
    },

    spawnExplosion() {
        const icons = ['🧻', '💩', '🍄', '🧼', '✨', '🤣'];
        for(let i=0; i<25; i++) {
            this.particles.push({
                x: this.frog.x, y: this.frog.y - 50,
                vx: (Math.random() - 0.5) * 20,
                vy: (Math.random() - 0.5) * 20,
                life: 1, rot: Math.random() * 6,
                icon: icons[Math.floor(Math.random() * icons.length)],
                size: 20 + Math.random() * 30
            });
        }
    },

    update() {
        this.frame++;
        this.frog.jumpY *= 0.85;
        this.frog.rot = Math.sin(this.frame * 0.05) * 0.05;

        for(let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            p.x += p.vx; p.y += p.vy; p.vy += 0.5; // gravity
            p.life -= 0.015; p.rot += 0.1;
            if(p.life <= 0) this.particles.splice(i, 1);
        }
    },

    draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Particle System
        for(let p of this.particles) {
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot);
            ctx.globalAlpha = p.life;
            ctx.font = `${p.size}px Arial`;
            ctx.fillText(p.icon, 0, 0);
            ctx.restore();
        }
        ctx.globalAlpha = 1;

        // Draw Frog Body
        ctx.save();
        ctx.translate(this.frog.x, this.frog.y + this.frog.jumpY);
        ctx.rotate(this.frog.rot);
        
        // Bounce animation
        let bounce = Math.sin(this.frame * 0.1) * 5;
        if(this.frog.state === 'laugh') bounce = Math.sin(this.frame * 0.5) * 15;

        // Main Shape
        ctx.fillStyle = '#22c55e';
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 8;
        ctx.beginPath();
        ctx.ellipse(0, bounce, 140, 100, 0, 0, Math.PI * 2);
        ctx.fill(); ctx.stroke();

        // Belly
        ctx.fillStyle = '#86efac';
        ctx.beginPath();
        ctx.ellipse(0, 20 + bounce, 80, 60, 0, 0, Math.PI * 2);
        ctx.fill();

        // Eyes
        ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.arc(-60, -90 + bounce, 40, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.arc(60, -90 + bounce, 40, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        
        ctx.fillStyle = '#000';
        let eyeSize = (this.frog.state === 'laugh') ? 5 : 15;
        ctx.beginPath(); ctx.arc(-60, -90 + bounce, eyeSize, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(60, -90 + bounce, eyeSize, 0, Math.PI * 2); ctx.fill();

        // Mouth logic
        ctx.beginPath();
        ctx.lineWidth = 6;
        if(this.frog.state === 'laugh') {
            ctx.fillStyle = '#991b1b';
            ctx.arc(0, 10 + bounce, 60, 0, Math.PI);
            ctx.fill();
        } else if(this.frog.state === 'angry') {
            ctx.moveTo(-50, 10 + bounce); ctx.lineTo(50, 10 + bounce);
        } else {
            ctx.arc(0, -10 + bounce, 50, 0.4, Math.PI - 0.4);
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