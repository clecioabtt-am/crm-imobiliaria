const API_BASE = "";

// Auth helpers
function setToken(t){ localStorage.setItem("token", t); }
function getToken(){ return localStorage.getItem("token"); }
function logout(){ localStorage.removeItem("token"); window.location="login.html"; }

async function api(path, method="GET", body=null){
  const headers = { "Content-Type":"application/json" };
  const token = getToken();
  if(token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });
  if(res.status === 401){ if(!location.pathname.endsWith("login.html")) logout(); }
  const data = await res.json().catch(()=> ({}));
  if(!res.ok){
    throw new Error(data.detail || ("Erro HTTP " + res.status));
  }
  return data;
}

function requireAuth(){
  if(!getToken()) window.location="login.html";
}

function navHtml(){
  return `
  <div class="card nav">
    <a href="dashboard.html">Dashboard</a>
    <a href="leads.html">Leads</a>
    <a href="properties.html">Imóveis</a>
    <a href="deals.html">Negócios</a>
    <a href="tasks.html">Tarefas</a>
    <button class="btn outline" onclick="logout()">Sair</button>
  </div>`;
}
