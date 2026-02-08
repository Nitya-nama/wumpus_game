console.log("NEW JS LOADED");
let state=null;
let shooting=false;
let lastScore=0;

/* ---------- API ---------- */
async function api(url,method="GET",data=null){
    const res = await fetch(url,{
        method:method,
        headers:{"Content-Type":"application/json"},
        body:data?JSON.stringify(data):null
    });
    state = await res.json();
    draw();
}

/* ---------- GAME ACTIONS ---------- */
function newGame(){ api("/new"); }

function moveDir(dir){
    if(shooting){
        shootFlash();
        api("/shoot","POST",{direction:dir});
        shooting=false;
    }else{
        api("/move","POST",{direction:dir});
    }
}

async function grab(){
    await api("/grab","POST");
    if(state.has_gold) playGrabAnimation();
}

function climb(){ api("/climb","POST"); }

function shootMode(){
    shooting=!shooting;
    alert("Shoot mode: "+(shooting?"ON":"OFF"));
}

/* ---------- VISUAL EFFECTS ---------- */
function shootFlash(){
    const grid=document.getElementById("grid");
    grid.classList.add("shooting");
    setTimeout(()=>grid.classList.remove("shooting"),250);
}

function playGrabAnimation(){
    const player=document.querySelector(".player");
    if(!player) return;
    player.classList.add("grabAnim");
    setTimeout(()=>player.classList.remove("grabAnim"),500);
}

/* ---------- DRAW ---------- */
function draw(){
    if(!state) return;

    const grid=document.getElementById("grid");
    grid.innerHTML="";

    for(let i=0;i<4;i++){
        for(let j=0;j<4;j++){
            let c=document.createElement("div");
            c.className="cell";

            let visited=state.visited.some(p=>p[0]==i&&p[1]==j);

            if(!visited){
                c.innerText="?";
            }
            else if(state.player[0]==i && state.player[1]==j){
                c.innerText="🧑";
                c.classList.add("player");
            }
            else{
                let p=state.percepts;
                let icons="";
                if(p.breeze) icons+="💨";
                if(p.stench) icons+="💀";
                if(p.glitter && !state.has_gold) icons+="✨";
                c.innerText=icons;
            }

            grid.appendChild(c);
        }
    }

    updateScore();
    updateStatus();
    updatePercepts();
}

/* ---------- SCORE ---------- */
function updateScore(){
    const el=document.getElementById("score");

    if(state.score > lastScore){
        el.classList.add("scoreUp");
        setTimeout(()=>el.classList.remove("scoreUp"),400);
    }

    el.innerText=state.score;
    lastScore=state.score;
}

/* ---------- STATUS ---------- */
function updateStatus(){
    const box=document.getElementById("statusBox");

    if(!state.alive && !state.won){
        box.className="status danger";
        box.innerText="💀 Game Over! You fell into a bottomless pit.";
        return;
    }

    if(state.won){
        box.className="status win";
        box.innerText="🏆 You escaped the cave with the gold!";
        return;
    }

    if(state.has_gold && state.player[0]==3 && state.player[1]==0){
        box.className="status win";
        box.innerText="🚪 You reached the exit! Press CLIMB to end the game.";
        return;
    }

    if(state.has_gold){
        box.className="status gold";
        box.innerText="🪙 You have the gold! Return to the exit.";
        return;
    }

    box.className="status info";
    box.innerText="Explore the cave carefully...";
}

/* ---------- PERCEPTS ---------- */
function updatePercepts(){
    const p=state.percepts;
    let msgs=[];

    if(p.glitter && !state.has_gold)
        msgs.push("✨ Glitter! Gold is here — grab it!");

    if(p.breeze) msgs.push("💨 Breeze (Pit nearby)");
    if(p.stench) msgs.push("💀 Stench (Wumpus nearby)");
    if(p.bump) msgs.push("🧱 Bumped into a wall");

    if(p.scream){
        document.body.classList.add("shake");
        setTimeout(()=>document.body.classList.remove("shake"),400);
        msgs.push("😱 You hear a scream — Wumpus is dead!");
    }

    const box=document.getElementById("senseBox");
    box.innerText = msgs.length ? msgs.join(" | ") : "The cave is silent...";
}

/* ---------- THEME ---------- */
window.onload = () => {
    newGame();

    const toggle=document.getElementById("themeToggle");

    function applyTheme(mode){
        document.body.classList.toggle("light",mode==="light");
        toggle.innerText = mode==="light" ? "☀️" : "🌙";
        localStorage.setItem("theme",mode);
    }

    toggle.onclick=()=>{
        const mode=document.body.classList.contains("light")?"dark":"light";
        applyTheme(mode);
    };

    applyTheme(localStorage.getItem("theme")||"dark");
};
