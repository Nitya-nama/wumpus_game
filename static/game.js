let state=null;
let shooting=false;

// ---------- API ----------
async function api(url,method="GET",data=null){
    const res = await fetch(url,{
        method:method,
        headers:{"Content-Type":"application/json"},
        body:data?JSON.stringify(data):null
    });

    state = await res.json();
    draw();
}

// ---------- GAME ACTIONS ----------
function newGame(){ api("/new"); }

function moveDir(dir){
    if(shooting){
        api("/shoot","POST",{direction:dir});
        shooting=false;
    }else{
        api("/move","POST",{direction:dir});
    }
}

function grab(){ api("/grab","POST"); }
function climb(){ api("/climb","POST"); }

function shootMode(){
    shooting=!shooting;
    alert("Shoot mode: "+(shooting?"ON":"OFF"));
}

// ---------- DRAW ----------
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
            }else if(state.player[0]==i && state.player[1]==j){
                c.innerText="🧑";
            }else{
                let p=state.percepts;
                let icons="";
                if(p.breeze) icons+="💨";
                if(p.stench) icons+="💀";
                if(p.glitter) icons+="✨";
                c.innerText=icons;
            }

            grid.appendChild(c);
        }
    }

    document.getElementById("score").innerText=state.score;

    // NEW
    updateStatus();
    updatePercepts();
}

function updateStatus(){
    const box=document.getElementById("statusBox");

    if(!state.alive && !state.won){
        box.className="status danger";
        box.innerText="💀 Game Over! You fell into a bottomless pit.";
        return;
    }

    if(state.won){
        box.className="status win";
        box.innerText="🏆 You escaped with the gold!";
        return;
    }

    box.className="status info";
    box.innerText="You are exploring the cave...";
}

function updatePercepts(){
    const p=state.percepts;
    let msgs=[];

    if(p.breeze) msgs.push("💨 Breeze (Pit nearby)");
    if(p.stench) msgs.push("💀 Stench (Wumpus nearby)");
    if(p.glitter) msgs.push("✨ Glitter (Gold here)");
    if(p.bump) msgs.push("🧱 Bump (Wall)");
    if(p.scream) msgs.push("😱 Scream (Wumpus killed)");

    const box=document.getElementById("senseBox");
    box.innerText = msgs.length ? msgs.join(" | ") : "No unusual percepts.";
}

const toggle=document.getElementById("themeToggle");

toggle.onclick=()=>{
    document.body.classList.toggle("light");
    toggle.innerText =
        document.body.classList.contains("light") ? "☀️" : "🌙";
};

// ---------- AUTO START ----------
window.onload = newGame;
