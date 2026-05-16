async function U(){
    let file = document.getElementById('f').files[0];
    let logs = document.getElementById('l');
    let fd = new FormData(); fd.append('file', file);
    logs.innerHTML = "Deploying...";
    let res = await fetch('/deploy', {method:'POST', body:fd});
    let data = await res.json();
    logs.innerHTML = data.status + " Bot: " + data.bot;
}
