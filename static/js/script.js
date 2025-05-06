//  Dummy Credentials for Testing Login
const dummyUser = { email: "test@example.com", password: "Test@1234" };

// Check if dummy credentials exist; if not, add them
if (!localStorage.getItem("users")) {
    localStorage.setItem("users", JSON.stringify([dummyUser]));
}

//  SIGNUP FUNCTION
function signup() {
    const email = document.getElementById("signup-email").value.trim().toLowerCase();
    const username = document.getElementById("signup-username").value.trim();
    const password = document.getElementById("signup-password").value;

    if (!email || !username || !password) {
        alert("Please fill in all fields.");
        return;
    }

    let users = JSON.parse(localStorage.getItem("users")) || [];

    if (users.some(user => user.email === email)) {
        alert("Email already registered. Please log in.");
        return;
    }

    users.push({ email, username, password });
    localStorage.setItem("users", JSON.stringify(users));

    alert("Signup successful! Redirecting to login...");
    window.location.href = "/";
}

//  LOGIN FUNCTION
function login() {
    const email = document.getElementById("login-email").value.trim().toLowerCase();
    const password = document.getElementById("login-password").value;

    if (!email || !password) {
        document.getElementById("error-message").innerText = "Please enter both email and password.";
        return;
    }

    let users = JSON.parse(localStorage.getItem("users")) || [];
    console.log("Stored users:", users); // Debug log
    
    let user = users.find(user => user.email === email && user.password === password);
    
    if (user) {
        localStorage.setItem("loggedIn", "true");
        localStorage.setItem("currentUser", JSON.stringify(user));
        window.location.href = "/home";
    } else {
        document.getElementById("error-message").innerText = "Invalid email or password!";
    }
}

//  CHECK LOGIN STATUS
document.addEventListener("DOMContentLoaded", function () {
    const path = window.location.pathname;

    if (path.includes("/home") && localStorage.getItem("loggedIn") !== "true") {
        window.location.href = "/";
    }
});

//  LOGOUT FUNCTION
function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "/";
}

// FLIGHT SEARCH FUNCTION
async function searchFlights() {
    const origin = document.getElementById("origin").value.toUpperCase();
    const destination = document.getElementById("destination").value.toUpperCase();
    const date = document.getElementById("date").value;

    if (!origin || !destination) {
        alert("Please fill in origin and destination.");
        return;
    }

    showLoader();

    try {
        const response = await fetch(`/search_flights?origin=${origin}&destination=${destination}`);
        const allFlights = await response.json();
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        if (!allFlights.length) {
            resultsDiv.innerHTML = "<p>No flights found for the selected route.</p>";
            return;
        }

        const shownAirlines = new Set();
        const filteredFlights = [];

        for (const flight of allFlights) {
            const key = flight.airline;
            if (!shownAirlines.has(key)) {
                const economy = allFlights.find(f => f.airline === key && f.class === "Economy");
                const business = allFlights.find(f => f.airline === key && f.class === "Business");

                if (economy) filteredFlights.push(economy);
                if (business) filteredFlights.push(business);

                shownAirlines.add(key);
            }
            if (filteredFlights.length >= 6) break;
        }

        if (filteredFlights.length < 6) {
            const additionalFlights = allFlights.filter(f => !filteredFlights.includes(f));
            while (filteredFlights.length < 6 && additionalFlights.length > 0) {
                const randomIndex = Math.floor(Math.random() * additionalFlights.length);
                filteredFlights.push(additionalFlights.splice(randomIndex, 1)[0]);
            }
        }

        const sampleAmenities = ["Extra Legroom", "Premium Meals", "Lounge Access", "Recliner Seats", "Free Wifi", "Priority Boarding"];
        const userDate = new Date(date);

        if (!filteredFlights.length) {
            resultsDiv.innerHTML = "<p>Less than 6 flights available for the selected route.</p>";
        }

        filteredFlights.forEach((flight, index) => {
            const dep = new Date(flight.departureTime);
            const arr = new Date(flight.arrivalTime);
            dep.setFullYear(userDate.getFullYear(), userDate.getMonth(), userDate.getDate());
            arr.setFullYear(userDate.getFullYear(), userDate.getMonth(), userDate.getDate());

            const flightCard = document.createElement("div");
            flightCard.classList.add("flight-card");
            if (index >= 6) flightCard.style.display = "none";

            let amenities = "";
            if (flight.class === "Business") {
                const selected = sampleAmenities.sort(() => 0.5 - Math.random()).slice(0, 4);
                amenities = `
                    <div class="amenities">
                        <strong>Amenities:</strong>
                        <ul>${selected.map(item => `<li>✔️ ${item}</li>`).join("")}</ul>
                    </div>
                `;
            }

            flightCard.innerHTML = `
                <div class="flight-info">
                    <h3>${flight.airline}</h3>
                    <p><i class="fas fa-plane"></i> Flight: <strong>${flight.flightNumber}</strong></p>
                    <p><i class="fas fa-map-marker-alt"></i> ${flight.origin} → ${flight.destination}</p>
                    <p><i class="fas fa-clock"></i> Departure: ${dep.toLocaleString()}</p>
                    <p><i class="fas fa-clock"></i> Arrival: ${arr.toLocaleString()}</p>

                    <p><i class="fas fa-chair"></i> Class: ${flight.class}</p>
                    <p><i class="fas fa-users"></i> Available Seats: ${flight.seatsAvailable}</p>
                    <p class="price"><i class="fas fa-tag"></i> <strong>₹${flight.price} / $${(flight.price / 83).toFixed(2)}</strong></p>
                    ${amenities}
                </div>
            `;
            resultsDiv.appendChild(flightCard);
        });

    } catch (error) {
        console.error("Error loading flights:", error);
        document.getElementById("results").innerHTML = `<p>Error loading flights: ${error.message}</p>`;
    } finally {
        setTimeout(hideLoader, 600);
    }
}



//  REPORTS

function downloadReport() {
    const element = document.getElementById("results");

    if (!element.innerHTML.trim()) {
        alert("No results to export.");
        return;
    }

    const opt = {
        margin:       5,
        filename:     'Flight_Report.pdf',
        image:        { type: 'jpeg', quality: 1 },
        html2canvas:  { 
            scale: 2,
            useCORS: true,
            backgroundColor: '#ffffff',
            scrollY: 0
        },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
    };

    html2pdf().set(opt).from(element).save();
}





//  GOOGLE LOGIN FUNCTION
function handleCredentialResponse(response) {
    const responsePayload = JSON.parse(atob(response.credential.split('.')[1]));

    console.log("Google User ID: " + responsePayload.sub);
    console.log("Email: " + responsePayload.email);

    // Store user login status
    localStorage.setItem("loggedIn", "true");
    window.location.href = "/home";
}

//  Initialize Google Login (Replace `YOUR_GOOGLE_CLIENT_ID`)
window.onload = function () {
    google.accounts.id.initialize({
        client_id: "699848347465-aovk1tbfmf4ss5jm97gs6p6v4akm4qj1.apps.googleusercontent.com", // 🔹 Replace with your actual Google Client ID
        callback: handleCredentialResponse
    });

    google.accounts.id.renderButton(
        document.getElementById("g_id_signin"),
        { theme: "outline", size: "large" }
    );

    google.accounts.id.prompt(); // Automatically trigger login prompt if applicable
};

//  Toggle Dark Mode
const darkToggle = document.getElementById("dark-toggle");
if (darkToggle) {
    darkToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
    });

    // On Load: Check Dark Mode Preference
    window.addEventListener("DOMContentLoaded", () => {
        const darkPref = localStorage.getItem("darkMode") === "true";
        if (darkPref) document.body.classList.add("dark-mode");
    });
}

//  Show Loader on Flight Search
function showLoader() {
    const loader = document.createElement("div");
    loader.classList.add("loader-overlay");
    loader.innerHTML = `<div class="loader"></div>`;
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.querySelector(".loader-overlay");
    if (loader) loader.remove();
}

//  Override searchFlights to add loader (optional)
const originalSearchFlights = searchFlights;
searchFlights = async function () {
    showLoader();
    await originalSearchFlights();
    setTimeout(hideLoader, 600); // short delay to keep UX smooth
};

//  Scroll to Blogs
const blogLink = document.getElementById("scroll-to-blogs");
if (blogLink) {
    blogLink.addEventListener("click", () => {
        const blogSection = document.getElementById("blog-section");
        if (blogSection) blogSection.scrollIntoView({ behavior: "smooth" });
    });
}

// 🌙 DARK MODE TOGGLE
const toggleBtn = document.getElementById("darkModeToggle");
toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    // Optionally save dark mode state in localStorage
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("darkMode", isDark);
});

// ✅ Load saved mode on page load
document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
});
