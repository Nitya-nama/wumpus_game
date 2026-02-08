const API_BASE = "https://wumpus-game-1jj6.onrender.com";

let visited = new Set();
let shoot = false;

function k(r,c){ return r+"-"+c }

/* ---------------- THEME ---------------- */

document.addEventListener("DOMContentLoaded", () => {

    const toggle = document.getElementById("themeToggle");

    if(toggle){
        if(localStorage.getItem("theme")==="light"){
            document.body.classList.add("light");
            toggle.checked=true;
        }

        toggle.addEventListener("change",()=>{
            document.body.classList.toggle("light");
            localStorage.setItem(
                "theme",
                document.body.classList.contains("light")?"light":"dark"
            );
        });
    }

    newGame(); // start after DOM ready
});


/* ---------------- GAME ACTIONS ---------------- */

async function newGame(){
    visited.clear();
    await fetch(API_BASE + "/start", {credentials:"include"});
    update();
}

async function move(d){
    if(shoot){
        await fetch(API_BASE + "/shoot",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            credentials:"include",
            body:JSON.stringify({direction:d})
        });
        shoot=false;
    }else{
        await fetch(API_BASE + "/move",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            credentials:"include",
            body:JSON.stringify({direction:d})
        });
    }
    update();
}

async function grab(){
    await fetch(API_BASE + "/grab",{method:"POST",credentials:"include"});
    update();
}

async function climb(){
    await fetch(API_BASE + "/climb",{method:"POST",credentials:"include"});
    update();
}

function shootMode(){ shoot=!shoot }

/* ---------------- UPDATE ---------------- */

async function update(){
    const r = await fetch(API_BASE + "/state",{credentials:"include"});
    const d = await r.json();

    visited.add(k(d.position[0],d.position[1]));

    draw(d);
    hud(d);

    if(d.game_over) reveal();
}

async function autoPlay(){
    const r=await fetch(API_BASE + "/auto",{credentials:"include"});
    const d=await r.json();
    update();
    if(!d.game_over) setTimeout(autoPlay,500);
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
    const r=await fetch(API_BASE + "/reveal",{credentials:"include"});
    const m=await r.json();
    console.log("map",m);
}
