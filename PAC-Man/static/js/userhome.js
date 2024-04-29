function saveDropdownData() {
    var name = document.getElementById("inputDropdownName").value;
    var url = document.getElementById("inputDropdownURL").value;
    var username = document.getElementById("inputDropdownUName").value;
    var password = document.getElementById("inputDropdownPWord").value;

    spawnDropdown(name, url, username, password);
}

function clearData(){
    document.getElementById("inputDropdownName").value = "";
    document.getElementById("inputDropdownURL").value = "";
    document.getElementById("inputDropdownUName").value = "";
    document.getElementById("inputDropdownPWord").value = "";
}

function spawnDropdown(name, url, username, password) {

    var newDropdown = document.createElement('div');
    newDropdown.classList.add('dropdown');

    var button = document.createElement('button');
    button.textContent = name;
    button.onclick = toggleDropdown;

    var dropdownOptions = document.createElement('div');
    dropdownOptions.classList.add('dropdown-content');

    dropdownOptions.innerHTML = `
        <input class="inputDropdownOptions" type="text" placeholder="${url}" disabled>
        <input class="inputDropdownOptions" type="text" placeholder="${username}" disabled>
        <input class="inputDropdownOptions" type="text" placeholder="${password}" disabled>
        <button class="save-button" onclick="saveCredentials()" style="width: 18%; font-size: 18px;">Save</button> 
        <button onclick="toggleEditMode()" style="width: 18%; font-size: 18px;">Edit</button>
        <button class="delete-button" style="width: 18%; font-size: 18px;">Delete</button>
        <button class="strength-checker-button" onclick="checkStrength()" style="width: 25%; font-size: 18px;">Strength Checker</button>
        <button class="generate-button" onclick="generatePassword()" style="width: 18%; font-size: 18px;">Generate</button>
    `;

    newDropdown.appendChild(button);
    newDropdown.appendChild(dropdownOptions);

    document.querySelector(".password-vault").appendChild(newDropdown);
}

// Function to toggle dropdown visibility
function toggleDropdown(id) {
    var dropdownContent = document.getElementById(id);
    console.log(dropdownContent);
    dropdownContent.style.display === "none" ? dropdownContent.style.display = "block" : dropdownContent.style.display = "none";
}   

function togglePlusDropdown() {
    var dropdownContent = document.getElementById("dropdownOptions");
    console.log(dropdownContent);
    dropdownContent.style.display === "none" ? dropdownContent.style.display = "block" : dropdownContent.style.display = "none";
}   

// Function to toggle edit mode
var editModeActive = false;
function toggleEditMode() {
    var dropdownButton = document.querySelector(".dropdown button");
    var inputs = document.querySelectorAll(".dropdown-content input");
    dropdownButton.classList.toggle("edit-mode");
    inputs.forEach(function(input) {
        input.disabled = !input.disabled;
        if (editModeActive) {
        input.style.backgroundColor = "lightgray"; // Reset to default background color
        } else {
        input.style.backgroundColor = "gold"; // Set background color on first click
        }
    });
    editModeActive = !editModeActive;
}

// Function to save credentials
function saveCredentials() {
    // Get the input values from the dropdown text boxes
    var name = document.getElementById("inputDropdownName").value;
    var url = document.getElementById("inputDropdownURL").value;
    var username = document.getElementById("inputDropdownUName").value;
    var password = document.getElementById("inputDropdownPWord").value;

    // Prepare the data object to be sent in the fetch request
    var data = {
        name: name,
        url: url,
        username: username,
        password: password
    };

    // Make a POST request to Flask route with collected data
    fetch('/PAC-Vault', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => console.log(data)); //Print the response (test)

    // Disable input fields after save
    var inputs = document.querySelectorAll("#inputDropdownOptions input");
    inputs.forEach(function(input) {
        input.disabled = true;
    });
}

// Function to save credentials for plus button
function savePlusCredentials() {
    var inputs = document.querySelectorAll("#plusDropdownOptions input");
    inputs.forEach(function(input) {
        input.disabled = true;
    });
    var dropdownButton = document.querySelectorAll(".dropdown button")[1];
    dropdownButton.classList.remove("edit-mode");
}

// Function to generate password
function generatePassword() {
    fetch('/password_gen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        var passwordInput = document.querySelector("#inputDropdownOptions[type='password']");
        passwordInput.value = data.password;
    });
    alert("Password generated!");
}

// Function to check strength
function checkStrength() {
    var passwordInput = document.querySelector("#inputDropdownOptions[type='passwod']");
    fetch('/password_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: passwordInput.value })
    })
    .then(response => response.json())
    .then(data => console.log(data));
    alert("Checking password strength...");
}