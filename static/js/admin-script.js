let content = document.getElementById("card-content");
let flash = document.getElementById("flash");
let scanNowBtn = document.getElementById(`register-student-btn`);

/* Scanner */
function fetchrfid() {
    disableScanner(true);
    showLoader();  
    fetch('/register-rfid')
    .then(response => {
        if (!response.ok) {
         
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
          document.getElementById("tag_no").value = rfid; 
          let modal = new bootstrap.Modal(document.getElementById('register-rfid'));
          
          
          let content = document.getElementById('content'); 
          if (content) {
            content.innerHTML = '';  
          }
          
          closeLoader();  
          modal.show();   
        }
    })
    .catch(error => {
        console.error('Error:', error.message);  
        closeLoader();  
        let flash = document.getElementById('flash');  
        if (flash) {
          flash.innerHTML = `${error.message}`; 
        }
    })
    .finally(() => {
        content.classList.add("id-card-default");
        disableScanner(false);

    });
}

/* Student Filters Functionality */ 
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchStudent");
    const filterSelect = document.getElementById("filterProgram");
    const tableBody = document.getElementById("studentsTable");

    function filterTable() {
        const searchText = searchInput.value.toLowerCase();
        const selectedProgram = filterSelect.value;
        
        Array.from(tableBody.getElementsByTagName("tr")).forEach(row => {
            const name = row.cells[1].textContent.toLowerCase();
            const program = row.cells[5].textContent;

            const matchesSearch = name.includes(searchText);
            const matchesFilter = selectedProgram === "" || program === selectedProgram;

            row.style.display = matchesSearch && matchesFilter ? "" : "none";
        });
    }

    searchInput.addEventListener("input", filterTable);
    filterSelect.addEventListener("change", filterTable);
});

/* Loaders */
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