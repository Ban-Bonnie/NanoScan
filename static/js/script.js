function autoFetchUser() {
    let student_details = document.getElementById("data");
    let schedule_element = document.getElementById("schedule");

    fetch('/fetch-user')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);

        if (data.error) {
            student_details.innerHTML = `<p style='color: red;'>${data.error}</p>`;
            schedule_element.innerHTML = "";
            return;
        }

        let user = data.user;
        let userSchedule = data.userSchedule;

        // Display user details
        if (user) {
            student_details.innerHTML = `
                <img src="${user.profile_pic || 'static/img/default-avatar.jpg'}" alt="Profile Picture" width="100" height="100" style="border-radius: 50%;">
                <p><strong>Name:</strong> ${user.first_name} ${user.last_name}</p>
                <p><strong>ID No.:</strong> ${user.id_no}</p>
                <p><strong>Section:</strong> ${user.section}</p>
                <p><strong>RFID Tag:</strong> ${user.tag_no}</p>
            `;
        } else {
            student_details.innerHTML = "<p style='color: red;'>User not found.</p>";
        }

        // Display user schedule
        if (userSchedule && userSchedule.length > 0) {
            let scheduleHTML = `
                <h3>Class Schedule</h3>
                <table border="1">
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
                    </tr>
                `;
            });

            scheduleHTML += "</table>";
            schedule_element.innerHTML = scheduleHTML;
        } else {
            schedule_element.innerHTML = "<p style='color: red;'>No schedule found.</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    
        // If it's a 400 error (no RFID detected), do nothing
        if (error.message.includes("400")) return;
    
        student_details.innerHTML = `<p style='color: red;'>User is not registered</p>`;
        schedule_element.innerHTML = "";
        schedule_element.innerHTML = "<p style='color: red;'>No schedule found.</p>";
    });
}
