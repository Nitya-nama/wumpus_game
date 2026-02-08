let visited=new Set()
let shoot=false

function k(r,c){return r+"-"+c}

document.addEventListener("DOMContentLoaded",()=>{
 newGame()
})

async function newGame(){
 visited.clear()

 document.getElementById("modal").classList.add("hidden")

 await fetch("/start")
 update()
}

async function move(d){
 if(shoot){
  await fetch("/shoot",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({direction:d})})
  shoot=false
 }else{
  await fetch("/move",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({direction:d})})
 }
 update()
}

function shootMode(){shoot=!shoot}

async function autoPlay(){
 await fetch("/auto")
 update()
}

async function update(){

 const r = await fetch("/state")
 const d = await r.json()

 /* ---- normal update ---- */
 visited.add(k(d.position[0],d.position[1]))
 draw(d)

 document.getElementById("score").innerText = "🏆 "+d.score+" 🏹 "+d.arrow
 const icons={
  breeze:"💨",
  stench:"👃",
  glitter:"✨"
}

let perceptText=d.percepts.map(p=>icons[p]||p).join(" ")

document.getElementById("sense").innerText =
  (perceptText+" "+(d.message||"")).trim()


 /* ---- WIN / LOSE MODAL ---- */
const modal = document.getElementById("modal")

if(d.game_over && modal.classList.contains("hidden")){
    modal.classList.remove("hidden")

    if(d.score > 0)
        document.getElementById("modalTitle").innerText="🏆 YOU ESCAPED!"
    else
        document.getElementById("modalTitle").innerText="💀 GAME OVER"

    document.getElementById("modalMsg").innerText="Final Score: "+d.score
}


 /* ---- AI REASONING ---- */
 explainAI(d)
}


function draw(d){
 const g=document.getElementById("grid")
 g.innerHTML=""
 for(let r=3;r>=0;r--){
  for(let c=0;c<4;c++){
   const div=document.createElement("div")
   div.className="cell"
   const key=k(r,c)
    if(d.position[0]==r && d.position[1]==c){
        div.classList.add("player")
        if(d.percepts.includes("breeze")) div.classList.add("breeze")
        if(d.percepts.includes("stench")) div.classList.add("stench")
        div.innerText="🧍"
    }
    else if(d.safe && d.safe.some(p=>p[0]==r && p[1]==c)){
        div.classList.add("safe")
    }
    else if(!visited.has(key)){
        div.classList.add("unknown")
    }
   g.appendChild(div)
  }
 }
}

function toggleTheme(){
 document.body.classList.toggle("light")
}

function explainAI(d){

 let text=""

 if(d.percepts.length===0){
     text="No stench, no breeze → adjacent cells are SAFE."
 }
 else{

     if(d.percepts.includes("breeze"))
         text+="Breeze sensed → pit in neighbouring cell. "

     if(d.percepts.includes("stench"))
         text+="Stench sensed → Wumpus nearby. "

     if(d.percepts.includes("breeze") && d.percepts.includes("stench"))
         text+="High danger zone → agent avoids unknown tiles."
     else
         text+="Agent marks risky cells and explores safe frontier."
 }

 document.getElementById("aiText").innerText=text
}
