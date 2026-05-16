function U() {
    let fileInput = document.getElementById('f');
    let log = document.getElementById('l');
    
    if (fileInput.files.length === 0) {
        log.innerHTML = "<span style='color:red;'>⚠️ Pehle file select karle bhai!</span>";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    log.innerHTML = "⏳ Deploying... Please wait...";

    fetch('/deploy', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        log.innerHTML = "<span style='color:#00ff41;'>✅ " + data.status + "</span>";
    })
    .catch(error => {
        console.error('Error:', error);
        log.innerHTML = "<span style='color:red;'>❌ Connection Failed!</span>";
    });
}

