function autoFetchUser() {
    let student_details = document.getElementById("student-id-card");
    let student_image = document.getElementById("student-image");
    let flash = document.getElementById("flash");
    let schedule_element = document.querySelector("#scheduleModal .schedule-modal-content .schedule-table-wrapper");

    if (!student_details || !student_image || !flash || !schedule_element) {
        console.error("One or more elements are missing.");
        return;
    }

    fetch('/fetch-user')
    .then(response => {
        if (!response.ok) {
            if (response.status === 404) {
                console.log("User is not registered");
                flash.innerHTML = "USER NOT REGISTERED"
                return null; // Stop further execution
            }
            if (response.status === 400) {
                console.log("No RFID detected");
                return null;
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        
        /* Redirect To admin if admin */
        if (data.redirect) {
            window.location.href = data.redirect;  
            return; 
        }

        if (!data) return; // Stop execution if user is not found

        console.log("✅ Data received:", data);

        if (data.error) {
            flash.innerHTML = `<p style='color: red;'>${data.error}</p>`;
            schedule_element.innerHTML = "";
            return;
        }

        let user = data.user;
        let userSchedule = data.userSchedule;

        if (user) {
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
    });
}
