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
            data.games.forEach(element => {
                const newDiv = document.createElement('div');
                newDiv.classList.add('style-div','roboto-medium');
                newDiv.textContent = element;
                document.body.appendChild(newDiv);
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