function fetchUser() {
    fetch('/fetch-user')
    .then(response => response.json())
    .then(data => {
        console.log(data);  
        let user = data.user;
        if (user) {
            document.getElementById("data").innerHTML = `
                
                <p><strong>Name:</strong> ${user[1]} ${user[2]}</p>
                <p><strong>Student Phone:</strong> ${user[4]}</p>
                <p><strong>Section:</strong> ${user[6]}</p>
                <p><strong>RFID Tag:</strong> ${user[5]}</p>
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
