let state = null;

async function newGame(){
    const res = await fetch("/new");
    state = await res.json();
    draw();
}

async function move(dir){
    const res = await fetch("/move",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({direction:dir})
    });
    state = await res.json();
    draw();
}

async function grab(){
    const res = await fetch("/grab",{method:"POST"});
    state = await res.json();
    draw();
}

async function shoot(){
    const res = await fetch("/shoot",{method:"POST"});
    state = await res.json();
    draw();
}

async function climb(){
    const res = await fetch("/climb",{method:"POST"});
    state = await res.json();
    draw();
}

function draw(){
    const grid=document.getElementById("grid");
    grid.innerHTML="";
    for(let i=0;i<4;i++){
        for(let j=0;j<4;j++){
            let cell=document.createElement("div");
            cell.className="cell";
            if(state.player[0]==i && state.player[1]==j)
                cell.innerText="🙂";
            grid.appendChild(cell);
        }
    }
}

newGame();
