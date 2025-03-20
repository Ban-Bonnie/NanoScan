function fetchrfid() {
    document.getElementById("flash").innerHTML = "";
    fetch('/register-rfid')
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => { throw new Error(errData.error); });
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        let rfid = data.rfid;
        if (rfid) {
            document.getElementById("tag_no").value = rfid; // Set hidden RFID field
            let modal = new bootstrap.Modal(document.getElementById('register-rfid')); 
            modal.show(); // Open modal
        }
    })
    .catch(error => {
        console.error('Error:', error.message);  // Log error properly
        
        document.getElementById("flash").innerHTML = `<p style='color: red;'>${error.message}</p>`;
    });
}

