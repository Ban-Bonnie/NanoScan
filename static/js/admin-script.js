function fetchrfid() {
    document.getElementById("flash").innerHTML = "";
    let loader = document.getElementById("loader");
    showLoader();

    fetch('/register-rfid')
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => { throw new Error(errData.error); });
        }
        closeLoader();
        return response.json();
    })
    .then(data => {
        console.log(data);
        let rfid = data.rfid;
        if (rfid) {
            document.getElementById("tag_no").value = rfid; // Set hidden RFID field
            let modal = new bootstrap.Modal(document.getElementById('register-rfid'));
            document.getElementById("loader").innerHTML=``; 
            closeLoader();
            modal.show(); // Open modal
        }
    })
    .catch(error => {
        console.error('Error:', error.message);  // Log error properly
        closeLoader();
        document.getElementById("flash").innerHTML = `<p style='color: red;'>${error.message}</p>`;
    });

    function showLoader(){
        loader.innerHTML=`    
        <div class="loader">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="orbit-container">
                <div class="orbit-dot"></div>
                <div class="orbit-dot"></div>
                <div class="orbit-dot"></div>
                <div class="orbit-dot"></div>
            </div>
        </div>
        `;
    }

    function closeLoader(){
        loader.innerHTML = `<p id="flash"></p>`;
    }
}

