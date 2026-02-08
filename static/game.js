let data=null

async function newGame(){
 await fetch("/start")
 update()
}

async function move(d){
 await fetch("/move",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({direction:d})})
 update()
}

async function shoot(){
 await fetch("/shoot",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({direction:"up"})})
 update()
}

async function auto(){
 await fetch("/auto")
 update()
}

async function update(){
 const r=await fetch("/state")
 data=await r.json()

 draw()
 document.getElementById("info").innerText=data.percepts.join(" ")+" "+data.message+" Score:"+data.score

 if(data.game_over){
  document.getElementById("modal").classList.remove("hidden")
  document.getElementById("endTitle").innerText=data.message
 }
}

function draw(){
 const g=document.getElementById("grid")
 g.innerHTML=""
 for(let r=3;r>=0;r--){
  for(let c=0;c<4;c++){
   const d=document.createElement("div")
   d.className="cell"
   if(data.position[0]==r && data.position[1]==c){
     d.classList.add("player")
     d.innerText="🙂"
   }
   g.appendChild(d)
  }
 }
}

newGame()
