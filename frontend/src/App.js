import React, { useState } from "react";

function App() {

const [hcpName,setHcpName] = useState("");
const [interactionType,setInteractionType] = useState("Meeting");
const [date,setDate] = useState("");
const [topics,setTopics] = useState("");
const [sentiment,setSentiment] = useState("Neutral");
const [followUp,setFollowUp] = useState("");

const [aiText,setAiText] = useState("");

const askAI = async () => {

try {

const response = await fetch("http://127.0.0.1:8000/ai-log",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
text:aiText
})
});

const data = await response.json();

setHcpName(data.hcpName || "");
setInteractionType(data.interactionType || "Meeting");
setTopics(data.topics || "");
setSentiment(data.sentiment || "Neutral");
setFollowUp(data.followUp || "");

} catch(error){

console.error(error);
alert("AI request failed");

}

};

const logInteraction = () => {

const data = {
hcpName,
interactionType,
date,
topics,
sentiment,
followUp
};

console.log("Logged Interaction:",data);
alert("Interaction Logged");

};

return (

<div style={page}>

<div style={formCard}>

<h2>Log HCP Interaction</h2>

<input
style={input}
placeholder="HCP Name"
value={hcpName}
onChange={(e)=>setHcpName(e.target.value)}
/>

<select
style={input}
value={interactionType}
onChange={(e)=>setInteractionType(e.target.value)}

>

<option>Meeting</option>
<option>Call</option>
<option>Email</option>
</select>

<input
type="date"
style={input}
value={date}
onChange={(e)=>setDate(e.target.value)}
/>

<textarea
style={input}
placeholder="Topics Discussed"
value={topics}
onChange={(e)=>setTopics(e.target.value)}
/>

<select
style={input}
value={sentiment}
onChange={(e)=>setSentiment(e.target.value)}
>
<option>Positive</option>
<option>Neutral</option>
<option>Negative</option>
</select>

<textarea
style={input}
placeholder="Follow-up Actions"
value={followUp}
onChange={(e)=>setFollowUp(e.target.value)}
/>

<button style={button} onClick={logInteraction}>
Log Interaction
</button>

</div>

<div style={aiCard}>

<h3>AI Assistant</h3>

<p>Describe the interaction and AI will auto-fill the form</p>

<textarea
style={chat}
placeholder="Example: Met Dr Sharma and discussed Product X..."
value={aiText}
onChange={(e)=>setAiText(e.target.value)}
/>

<button style={aiButton} onClick={askAI}>
Ask AI
</button>

</div>

</div>

);

}

const page = {
height:"100vh",
display:"flex",
justifyContent:"center",
alignItems:"center",
gap:"40px",
background:"#e6f4ea",
fontFamily:"Inter, sans-serif"
};

const formCard = {
width:"420px",
padding:"30px",
borderRadius:"12px",
background:"white",
boxShadow:"0 10px 25px rgba(0,0,0,0.1)"
};

const aiCard = {
width:"350px",
padding:"25px",
borderRadius:"12px",
background:"white",
boxShadow:"0 10px 25px rgba(0,0,0,0.1)"
};

const input = {
width:"100%",
padding:"12px",
marginTop:"12px",
borderRadius:"8px",
border:"1px solid #ddd"
};

const button = {
width:"100%",
marginTop:"15px",
padding:"12px",
background:"#3b82f6",
color:"white",
border:"none",
borderRadius:"8px",
cursor:"pointer"
};

const aiButton = {
width:"100%",
marginTop:"12px",
padding:"12px",
background:"#10b981",
color:"white",
border:"none",
borderRadius:"8px",
cursor:"pointer"
};

const chat = {
width:"100%",
height:"120px",
marginTop:"10px",
padding:"10px",
borderRadius:"8px",
border:"1px solid #ddd"
};

export default App;
