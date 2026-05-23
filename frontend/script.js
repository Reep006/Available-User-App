const usersContainer = document.getElementById("usersContainer");

const totalUsers = document.getElementById("totalUsers");

const availableUsers = document.getElementById("availableUsers");

const unavailableUsers = document.getElementById("unavailableUsers");

const loader = document.getElementById("loader");

const API_URL = "http://127.0.0.1:5000";

async function fetchUsers() {

    loader.style.display = "block";

    try {

        const response = await fetch(`${API_URL}/users`);

        const users = await response.json();

        usersContainer.innerHTML = "";

        let availableCount = 0;

        users.forEach(user => {

            if(user.available){
                availableCount++;
            }

            const card = document.createElement("div");

            card.className = "user-card";

            card.innerHTML = `
                <img src="${user.image}" alt="${user.name}">

                <h2>${user.name}</h2>

                <p class="role">${user.role}</p>

                <div class="status ${user.available ? "available" : "unavailable"}">
                    ${user.available ? "Available" : "Unavailable"}
                </div>

                <br>

                <button
                    class="toggle-btn ${user.available ? "btn-unavailable" : "btn-available"}"
                    onclick="toggleAvailability('${user.id}')"
                >
                    ${user.available ? "Mark Unavailable" : "Mark Available"}
                </button>
            `;

            usersContainer.appendChild(card);
        });

        totalUsers.textContent = users.length;

        availableUsers.textContent = availableCount;

        unavailableUsers.textContent = users.length - availableCount;

    } catch (error) {

        usersContainer.innerHTML = `
            <h2 style="text-align:center;">
                Failed to load users
            </h2>
        `;

        console.log(error);

    }

    loader.style.display = "none";
}

async function toggleAvailability(id){

    try{

        await fetch(`${API_URL}/toggle/${id}`, {
            method: "PUT"
        });

        fetchUsers();

    }catch(error){

        console.log(error);
    }
}

fetchUsers();