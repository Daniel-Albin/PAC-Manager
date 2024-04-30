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

var dropdownCounter = 0;
function spawnDropdown(name, url, username, password) {
    dropdownCounter++;

    var newDropdown = document.createElement('div');
    newDropdown.classList.add('dropdown');

    var button = document.createElement('button');
    button.classList.add('vault-entry')
    button.textContent = name;
    button.onclick = (function(counter) {
        return function() {
            toggleTempDropdown('temp-id-' + counter);
        };
    })(dropdownCounter);

    var dropdownOptions = document.createElement('div');
    dropdownOptions.id = 'temp-id-' + dropdownCounter;
    dropdownOptions.classList.add('dropdown-content');

    dropdownOptions.innerHTML = `
        <input class="inputDropdownOptions" type="password" value="${url}" disabled>
        <input class="inputDropdownOptions" type="password" value="${username}" disabled>
        <input class="inputDropdownOptions" type="password" value="${password}" disabled>
        <button class="save-button" onclick="updateCredentials('temp-id-' + counter);" style="width: 18%; font-size: 18px;">Save</button> 
        <button class="edit-button" onclick="toggleEditMode()" style="width: 18%; font-size: 18px;">Edit</button>
        <button class="delete-button" onclick="deleteCredentials('temp-id-' + counter)" style="width: 18%; font-size: 18px;">Delete</button>
        <button class="strength-checker-button" onclick="checkStrength('temp-id-' + counter)" style="width: 25%; font-size: 18px;">Strength Checker</button>
        <button class="generate-button" onclick="generatePassword('temp-id-' + counter)" style="width: 18%; font-size: 18px;">Generate</button>
    `;

    newDropdown.appendChild(button);
    newDropdown.appendChild(dropdownOptions);

    document.querySelector(".password-vault").appendChild(newDropdown);
}

// Function to toggle dropdown visibility
function toggleDropdown(id) {
    var dropdownContent = document.getElementById(id);
    dropdownContent.style.display === "none" ? dropdownContent.style.display = "block" : dropdownContent.style.display = "none";
}   

function togglePlusDropdown() {
    var dropdownContent = document.getElementById("dropdownOptions");
    dropdownContent.style.display === "none" ? dropdownContent.style.display = "block" : dropdownContent.style.display = "none";
}   

function toggleTempDropdown(dropdownId) {
    var dropdownContent = document.getElementById(dropdownId);
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
        input.style.backgroundColor = "lightgray";
        input.type = "password"
        } else {
        input.style.backgroundColor = "gold";
        input.type = "text"
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

    if (!name || !username || !password){
        alert("You must have a name, username, and password.");
        return;
    }
    else{
        // Prepare the data object to be sent in the fetch request
        var data = {
            name: name,
            url: url,
            username: username,
            password: password
        };

        // Make a POST request to Flask route with collected data
        fetch('/addTo-Vault', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())

        // Disable input fields after save
        var inputs = document.querySelectorAll("#inputDropdownOptions input");
        inputs.forEach(function(input) {
            input.disabled = true;
        });
    }
}

function updateCredentials(id) {
    // Get the input values from the dropdown text boxes
    var url = document.getElementById("inputDropdownURL-" + id).value;
    var username = document.getElementById("inputDropdownUName-" + id).value;
    var password = document.getElementById("inputDropdownPWord-" + id).value;

    if (!username || !password){
        alert("You must have a Username and Password.");
        return;
    }
    else{
        // Prepare the data object to be sent in the fetch request
        var data = {
            url: url,
            id: id,
            username: username,
            password: password
        };

        // Make a POST request to Flask route with collected data
        fetch('/update-Vault', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())

        // Disable input fields after save
        var inputs = document.querySelectorAll("#inputDropdownOptions input");
        inputs.forEach(function(input) {
            input.disabled = true;
        });
    }
}

function deleteCredentials(id) {

    var data = {
        id: id
    };

    // Make a POST request to Flask route with collected data
    fetch('/deleteFromVault', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())

    // Disable input fields after save
    var inputs = document.querySelectorAll("#inputDropdownOptions input");
    inputs.forEach(function(input) {
        input.disabled = true;
    });
}

function generatePlusPassword() {
    fetch('/password_gen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        var passwordInput = document.getElementById("inputDropdownPWord");
        passwordInput.value = data.password;
    });
    alert("Password generated!");
}

function checkPlusStrength() {
    var password = document.getElementById("inputDropdownPWord").value;
    var data = {
        password: password
    };
    fetch('/password_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.strength));
}

// Function to generate password
function generatePassword(id) {
    fetch('/password_gen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        var passwordInput = document.getElementById("inputDropdownPWord-" + id);
        passwordInput.value = data.password;
    });
}

// Function to check strength
function checkStrength(id) {
    var password = document.getElementById("inputDropdownPWord-" + id).value;
    var data = {
        password: password
    };
    fetch('/password_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.strength));
}

function searchBar() {
    var searchInput = document.getElementById("search-bar").value.toLowerCase();;
    console.log(searchInput)
    var passwords = document.querySelectorAll(".vault-entry");
    
    passwords.forEach(password => {
        var passwordData = password.innerText.toLowerCase();
        if (passwordData.includes(searchInput)) {
            password.style.display = "block";
        } else {
            password.style.display = "none";
        }
    });
}
