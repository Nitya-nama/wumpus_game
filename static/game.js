let visited = new Set();
let shootMode=false;

function key(r,c){ return r+"-"+c }

async function newGame(){
    visited.clear();
    await fetch("/start");
    update();
}

async function move(dir){
    if(shootMode){
        await fetch("/shoot",{method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({direction:dir})});
        shootMode=false;
    }else{
        await fetch("/move",{method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({direction:dir})});
    }
    update();
}

function toggleShoot(){
    shootMode=!shootMode;
    setMessage(shootMode ? "Shoot mode: choose direction" : "Move mode");
}

function grab(){ setMessage("Auto grab when on gold"); }
function climb(){ move("down"); }

function setMessage(msg){
    document.getElementById("message").innerText=msg;
}

async function update(){
    const res=await fetch("/state");
    const data=await res.json();

    visited.add(key(data.position[0],data.position[1]));

    drawGrid(data);
    document.getElementById("arrow").innerText="🎯 "+data.arrow;
    document.getElementById("message").innerText=data.message || "";
}

function drawGrid(data){
    const grid=document.getElementById("grid");
    grid.innerHTML="";

    for(let r=3;r>=0;r--){
        for(let c=0;c<4;c++){

            const div=document.createElement("div");
            div.className="cell";

            if(!visited.has(key(r,c))){
                div.classList.add("hidden");
                div.innerText="?";
            }else{

                if(data.position[0]==r && data.position[1]==c){
                    div.classList.add("player");
                    div.innerText="🧍";
                }else{
                    div.innerText=perceptIcon(data,r,c);
                }

            }
            grid.appendChild(div);
        }
    }
}

function perceptIcon(data,r,c){
    if(data.percepts.includes("glitter") && data.position[0]==r && data.position[1]==c)
        return "💰";
    if(data.percepts.includes("breeze")) return "💨";
    if(data.percepts.includes("stench")) return "👃";
    return "";
}

newGame();
