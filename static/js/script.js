function fetchUser() {
    fetch('/fetch-user')
    .then(response => response.json())
    .then(data => {
        console.log(data);  
        let user = data.user;
        if (user) {
            document.getElementById("data").innerHTML = `
                <p><strong>ID:</strong> ${user[0]}</p>
                <p><strong>First Name:</strong> ${user[1]}</p>
                <p><strong>Last Name:</strong> ${user[2]}</p>
                <p><strong>Student Phone:</strong> ${user[3]}</p>
                <p><strong>Parent Phone :</strong> ${user[4]}</p>
                <p><strong>RFID Tag:</strong> ${user[5]}</p>
                <p><strong>Section:</strong> ${user[6]}</p>
            `;
        } else {
            document.getElementById("data").innerHTML = "<p style='color: red;'>User not found.</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("data").innerHTML = "<p style='color: red;'>Error fetching data.</p>";
    });
}
