let visited = new Set();
let shoot = false;

function k(r,c){ return r+"-"+c }

/* ---------------- START ---------------- */

document.addEventListener("DOMContentLoaded", () => {
    newGame();
});

/* ---------------- GAME ---------------- */

async function newGame(){
    visited.clear();
    await fetch("/api/start",{credentials:"include"});
    update();
}

async function move(d){
    if(shoot){
        await fetch("/api/shoot",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            credentials:"include",
            body:JSON.stringify({direction:d})
        });
        shoot=false;
    }else{
        await fetch("/api/move",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            credentials:"include",
            body:JSON.stringify({direction:d})
        });
    }
    update();
}

async function grab(){
    await fetch("/api/grab",{method:"POST",credentials:"include"});
    update();
}

async function climb(){
    await fetch("/api/climb",{method:"POST",credentials:"include"});
    update();
}

function shootMode(){ shoot=!shoot }

async function autoPlay(){
    const r=await fetch("/api/auto",{credentials:"include"});
    const d=await r.json();
    update();
    if(!d.game_over) setTimeout(autoPlay,500);
}

/* ---------------- UPDATE ---------------- */

async function update(){
    const r = await fetch("/api/state",{credentials:"include"});

    if(!r.ok){
        console.error("API error", r.status);
        return;
    }

    const d = await r.json();

    if(!d.position){
        console.error("Invalid state", d);
        return;
    }

    visited.add(k(d.position[0],d.position[1]));
    draw(d);
    hud(d);

    if(d.game_over) reveal();
}


/* ---------------- UI ---------------- */

function hud(d){
    document.getElementById("score").innerText="🏆 "+d.score;
    document.getElementById("arrow").innerText="🏹 "+d.arrow;

    let s="";
    if(d.percepts.includes("stench")) s+="👃 ";
    if(d.percepts.includes("breeze")) s+="💨 ";
    if(d.percepts.includes("glitter")) s+="✨ ";

    document.getElementById("sense").innerText=s;
    document.getElementById("msg").innerText=d.message;
}

function draw(d){
    const g=document.getElementById("grid");
    g.innerHTML="";

    for(let r=3;r>=0;r--){
        for(let c=0;c<4;c++){

            const div=document.createElement("div");
            div.className="cell";

            if(!visited.has(k(r,c))){
                div.classList.add("hidden");
                div.innerText="?";
            }
            else if(d.position[0]==r && d.position[1]==c){
                div.classList.add("player");
                div.innerText="🧍";
            }

            g.appendChild(div);
        }
    }
}

async function reveal(){
    const r=await fetch("/api/reveal",{credentials:"include"});
    const m=await r.json();
    console.log("map",m);
}
