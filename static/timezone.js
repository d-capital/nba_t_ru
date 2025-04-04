// Get the user's timezone
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

// Log it to ensure it's correct
console.log("User Time Zone:", userTimeZone);

// Send it to the backend
const sendTimeZoneToBackend = async () => {
    try {
        const response = await fetch('/api/get_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'timeZone': userTimeZone }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Server Response:", data);
            const tableBody = document.querySelector("#nba-schedule tbody");
            tableBody.innerHTML = "";
            data.games.forEach(game => {
                const row = document.createElement("tr");
                    row.innerHTML = `
                        <td class="logocell">${game.home_team} <img style="width: 50px;height: 50px;" src = ${game.home_team_logo}> vs ${game.away_team} <img style="width: 50px;height: 50px;" src = ${game.away_team_logo}></td>
                        <td>${new Date(game.time).toLocaleTimeString()}</td>
                        <td>${game.venue}</td>
                    `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Failed to send timezone:", response.statusText);
        }
    } catch (error) {
        console.error("Error sending timezone:", error);
    }
};

// Call the function to send the timezone
sendTimeZoneToBackend();