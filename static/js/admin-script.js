function fetchrfid() {
    fetch('/register-rfid')
    .then(response => response.json())
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
        console.error('Error:', error);
        document.getElementById("flash").innerHTML = "<p style='color: red;'>Error fetching data.</p>";
    });
}
