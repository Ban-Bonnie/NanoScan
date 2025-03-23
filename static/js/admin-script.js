let content = document.getElementById("card-content");
let flash = document.getElementById("flash");
let scanNowBtn = document.getElementById(`register-student-btn`);


function fetchrfid() {
    disableScanner(true);
    showLoader();  // Display loading indicator
    fetch('/register-rfid')
    .then(response => {
        if (!response.ok) {
          // Handle non-OK responses by throwing an error with a message from the response
          return response.json().then(errData => {
            throw new Error(errData.error || 'Unknown error occurred');
          });
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        let rfid = data.rfid;
        if (rfid) {
          document.getElementById("tag_no").value = rfid; // Set RFID in the hidden field
          let modal = new bootstrap.Modal(document.getElementById('register-rfid'));
          
          // Ensure content is initialized properly if you're updating it
          let content = document.getElementById('content'); // Assuming content is an element you want to update
          if (content) {
            content.innerHTML = '';  // Clear content if necessary
          }
          
          closeLoader();  // Hide the loader
          modal.show();   // Show the modal with RFID data
        }
    })
    .catch(error => {
        console.error('Error:', error.message);  // Log error details
        closeLoader();  // Ensure loader is hidden
        let flash = document.getElementById('flash');  // Assuming 'flash' is where you display errors
        if (flash) {
          flash.innerHTML = `${error.message}`; // Display error message to user
        }
    })
    .finally(() => {
        content.classList.add("id-card-default");
        disableScanner(false);

    });
}
  

function showLoader(){
    content.classList.add("id-card-loader");
    content.classList.remove("id-card-default");
    content.innerHTML=`    
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
    content.innerHTML = `<h2 onclick="fetchrfid()" id="flash"></h2>`;
}

// =========================
// SCANNER CONTROL FUNCTION
// =========================
function disableScanner(state) {
    if (scanNowBtn) {
        scanNowBtn.disabled = state; 
    }
}