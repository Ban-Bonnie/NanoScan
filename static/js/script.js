// =========================
// GLOBAL VARIABLES
// =========================
let content = document.getElementById("card-content");
let student_details = document.getElementById("student-id-card");
let student_image = document.getElementById("student-image");
let flash = document.getElementById("flash");
let schedule_element = document.querySelector("#scheduleModal .schedule-modal-content .schedule-table-wrapper");
let scanNowBtn = document.getElementById("scan-now-btn");

// =========================
// MAIN FUNCTION - Fetch User Data
// =========================
function autoFetchUser() {
    content.classList.remove("id-card-default");
    flash.textContent = "";
    disableScanner(true);
    showLoader();

    if (!flash || !schedule_element) {
        console.error("One or more elements are missing.");
        disableScanner(false);
        return;
    }

    fetch('/fetch-user')
    .then(response => {
        if (!response.ok) {
            hideLoader();
            disableScanner(false);
            if (response.status === 404) {
                console.log("User is not registered");
                clearCard("USER NOT REGISTERED");
                return null;
            }
            if (response.status === 400) {
                console.log("No RFID Scanner Timeout");
                clearCard("No RFID Detected");
                return null;
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
            return;
        }

        if (!data) return;

        console.log("✅ Data received:", data);

        if (data.error) {
            clearCard(`${data.error}`);
            schedule_element.innerHTML = "";
            return;
        }

        let user = data.user;
        let userSchedule = data.userSchedule;

        if (user) {
            hideLoader();
            let student_details = document.getElementById("student-id-card");
            let student_image = document.getElementById("student-image");
            document.getElementById(`section-label`).textContent=`${user.section} `;
            student_details.innerHTML = `
                <p id="name" class="fw-bold fs-5">${user.first_name} ${user.last_name}</p>
                <p id="id-no" class="fw-semibold fs-6">ID NO. ${user.id_no}</p>
                <p id="program" class="fs-6">${user.program}</p>
                <p id="section" class="fs-6">${user.section}</p>
            `;
            student_image.src = user.profile_pic ? user.profile_pic : 'static/img/default-avatar.jpg';
        }

        if (Array.isArray(userSchedule) && userSchedule.length > 0) {
            let scheduleHTML = `
                <table>
                    <tr>
                        <th>Subject</th>
                        <th>Day</th>
                        <th>Time</th>
                        <th>Teacher</th>
                        <th>Room</th>
                    </tr>`;

            userSchedule.forEach(schedule => {
                scheduleHTML += `
                    <tr>
                        <td>${schedule.subject_name}</td>
                        <td>${schedule.day_of_week}</td>
                        <td>${schedule.start_time} - ${schedule.end_time}</td>
                        <td>${schedule.subject_teacher}</td>
                        <td>${schedule.room}</td>
                    </tr>`;
            });

            scheduleHTML += `</table>`;
            schedule_element.innerHTML = scheduleHTML;
        } else {
            schedule_element.innerHTML = "<p style='color: red;'>No schedule found.</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        disableScanner(false);
    });
}

// =========================
// UI HANDLING FUNCTIONS
// =========================
function clearCard(message) {
    content.classList.add("id-card-default");
    content.innerHTML = `<h2 onclick="autoFetchUser()">${message}</h2>`  
    disableScanner(false);
}

function showLoader() {
    content.innerHTML = `    
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
    content.classList.add("id-card-loader"); 
}

function hideLoader() {
    content.classList.remove("id-card-loader");
    content.classList.add("id-card");
    content.innerHTML = `
            <h5 id="school" class="text-center">Phinma University of Iloilo</h5>
            <div class="content">
                <img id="student-image" alt="profile pic" class="picture-box">
                <div id="student-id-card" class="info">
                    <p id="name" class="fw-bold fs-5"></p>
                    <p id="id-no" class="fw-semibold fs-6"></p>
                    <p id="program" class="fs-6"></p>
                    <p id="section" class="fs-6"></p>
                </div>
            </div>`;   
}

// =========================
// SCANNER CONTROL FUNCTION
// =========================
function disableScanner(state) {
    if (scanNowBtn) {
        scanNowBtn.disabled = state; 
    }
}


