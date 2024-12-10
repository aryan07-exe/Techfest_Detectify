function startDetection() {
    fetch('/start_detection', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Detection started') {
                document.getElementById('status').innerText = "Detection is Running...";
            } else {
                alert(data.status);
            }
        })
        .catch(error => console.error('Error:', error));
}

function stopDetection() {
    fetch('/stop_detection', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Detection stopped') {
                location.reload(); // Refresh the page to reset everything
            } else {
                alert(data.status);
            }
        })
        .catch(error => console.error('Error:', error));
}
