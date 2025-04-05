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
                        <td class="logocell">${game.home_team} <img style="width: 50px;height: 50px;" src = "/static/logos/${game.home_team_logo}.svg"> vs ${game.away_team} <img style="width: 50px;height: 50px;" src = "/static/logos/${game.away_team_logo}.svg"></td>
                        <td>${new Date(game.time).toLocaleTimeString()}</td>
                        ${game.video_link ? `<td><a href="${game.video_link}" target="_blank">Watch</a></td>`: `<td>No broadcast</td>`}
                    `;
                tableBody.appendChild(row);
                let date = new Date(game.time);
                let now = new Date();
                if(game.video_link && now > date){
                    iframe = `
                        <div style="left: 0; width: 100%; height: 0; position: relative; padding-bottom: 56.25%;">
                            <iframe 
                                src="https://vkvideo.ru/video_ext.php?oid=${game.oid}&id=${game.id}" 
                                style="top: 0; left: 0; width: 100%; height: 100%; position: absolute; border: 0;" 
                                allowfullscreen scrolling="no" 
                                allow="encrypted-media;">
                            </iframe>
                        </div>
                    `
                    const row2 = document.createElement("tr");
                    row2.innerHTML = iframe;
                    tableBody.appendChild(row2)
                }
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