let visited=new Set();

function key(r,c){return r+"-"+c}

async function start(){
 await fetch("/start");
 update();
}

async function move(d){
 await fetch("/move",{method:"POST",
 headers:{"Content-Type":"application/json"},
 body:JSON.stringify({direction:d})});
 update();
}

async function update(){
 const r=await fetch("/state");
 const d=await r.json();

 visited.add(key(d.position[0],d.position[1]));

 draw(d);
 document.getElementById("score").innerText="Score: "+d.score;
 document.getElementById("sense").innerText=d.percepts.join(" ");
}

function draw(d){
 const g=document.getElementById("grid");
 g.innerHTML="";
 for(let r=3;r>=0;r--){
  for(let c=0;c<4;c++){
   const div=document.createElement("div");
   div.className="cell";
   if(!visited.has(key(r,c))) div.classList.add("hidden");
   if(d.position[0]==r&&d.position[1]==c){
    div.classList.add("player");
    div.innerText="🧍";
   }
   g.appendChild(div);
  }
 }
}

async function autoPlay(){
 await fetch("/auto");
 update();
}

start();
