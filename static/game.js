let state=null;

async function api(url,method="GET",data=null){
    let res=await fetch(url,{
        method,
        headers:{"Content-Type":"application/json"},
        body:data?JSON.stringify(data):null
    });
    state=await res.json();
    draw();
}

function draw(){
    const grid=document.getElementById("grid");
    grid.innerHTML="";

    for(let i=0;i<4;i++){
        for(let j=0;j<4;j++){

            let c=document.createElement("div");
            c.className="cell";

            let visited=state.visited.some(p=>p[0]==i&&p[1]==j);

            if(!visited){
                c.innerText="?"
            }else{
                let p=state.percepts;

                if(state.player[0]==i && state.player[1]==j){
                    c.innerText="🧑";
                }else{
                    let icons="";
                    if(p.breeze) icons+="💨";
                    if(p.stench) icons+="💀";
                    if(p.glitter) icons+="✨";
                    c.innerText=icons||"";
                }
            }

            grid.appendChild(c);
        }
    }

    document.getElementById("score").innerText=state.score;
}
