document.getElementById('playlist-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const city = document.getElementById('city').value;
    const mood = document.getElementById('mood').value;

    fetch('/generate_playlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city, mood: mood })
    })
    .then(response => response.json())
    .then(data => {
        const playlist = data.playlist;
        const playlistElement = document.getElementById('playlist');
        playlistElement.innerHTML = '';
        playlist.forEach(song => {
            const li = document.createElement('li');
            li.textContent = song;
            playlistElement.appendChild(li);
        });
    });
});
 
