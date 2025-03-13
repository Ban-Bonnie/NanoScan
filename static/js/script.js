
function fetchUser() { /* TEMPORARY */
    fetch('/fetch-user')
    .then(response => response.json())
    .then(data => {
        console.log(data);  
        let user = data.user
        if (user) {
            document.getElementById("data").innerHTML = `
                <strong>ID:</strong> ${user[0]}<br>
                <strong>First Name:</strong> ${user[1]}<br>
                <strong>Last Name:</strong> ${user[2]}<br>
                <strong>Phone 1:</strong> ${user[3]}<br>
                <strong>Phone 2:</strong> ${user[4]}<br>
                <strong>RFID Tag:</strong> ${user[5]}<br>
                <strong>Section:</strong> ${user[6]}
            `;
        } else {
            document.getElementById("data").textContent = "User not found.";
        }
    })
    .catch(error => console.error('Error:', error));
    
}

