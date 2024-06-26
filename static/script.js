function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999; path=/';
}

function applyTheme(theme) {
    document.documentElement.className = theme;
    setCookie("theme", theme, 7);
}

function darkModeOn() {
    document.body.classList.add('dark-mode');
    setCookie("dark_mode", true, 7);
}

function darkModeOff() {
    document.body.classList.remove('dark-mode');
    setCookie("dark_mode", false, 7);
}

document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();
    var username = getCookie("username");
    if (!username) {
        username = prompt("Enter your username:");
        if (username) {
            setCookie("username", username, 7);  // Store cookie for 7 days
        } else {
            username = "user";
        }
    }

    var currentTheme = getCookie("theme") || "light-theme";
    applyTheme(currentTheme);

    if (getCookie("dark_mode") === "true") {
        document.body.classList.add('dark-mode');
    }

    function createMessageElement(data, isFollowed = false) {
        const chatMessages = document.querySelector('.chat-messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', data.username === username ? 'sent' : 'received');

        if (!isFollowed) {
            messageElement.innerHTML = `
                <div class="header">
                    <span class="username">${data.username}</span>
                    <span class="time">${data.time}</span>
                </div>
                <span class="text">${data.message}</span>
            `;
        } else {
            messageElement.classList.add('followed');
            messageElement.innerHTML = `
                <span class="text">${data.message}</span>
            `;
        }

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    socket.on('message', function(data) {
        createMessageElement(data);
    });

    socket.on('followed_message', function(data) {
        createMessageElement(data, true);
    });

    socket.on('change_theme', function(themeCommand) {
        if (themeCommand === '1') {
            applyTheme('light-theme');
        } else if (themeCommand === '2') {
            applyTheme('pink-theme');
        } else if (themeCommand === '3') {
            applyTheme('blue-theme');
        }
    });

    socket.on('dark_mode', function() {
        darkModeOn();
    });

    socket.on('dark_mode_off', function() {
        darkModeOff();
    });

    // Socket.IO event listener for receiving music playback command
    socket.on('play_music', function(data) {
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.style.display = 'block';
        audioPlayer.src = data.url;
        audioPlayer.play();
    });

    // Socket.IO event listener for receiving pause music command
    socket.on('pause_music', function() {
        const audioPlayer = document.getElementById('audioPlayer');
        if (!audioPlayer.paused) {
            audioPlayer.pause();
        }
    });

    // Socket.IO event listener for receiving pause music command
    socket.on('unpause_music', function() {
        const audioPlayer = document.getElementById('audioPlayer');
        if (audioPlayer.paused) {
            audioPlayer.play();
        }
    });

    // Socket.IO event listener for toggling loop music command
    socket.on('loop_music', function() {
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.loop = !audioPlayer.loop;  // Toggle loop state
    });
    // Socket.IO event listener for handling music download failure
    socket.on('music_download_failed', function(data) {
        alert(data.message);
    });


    socket.on('users_online', function(count) {
        document.getElementById('users-online').innerText = `Users online: ${count}`;
    });

    document.querySelector('.chat-input').addEventListener('submit', function(e) {
        e.preventDefault();
        const messageInput = this.elements['message'];
        const message = messageInput.value;
        socket.send({ username: username, message: message });
        messageInput.value = '';
        messageInput.focus();  // Keep the input field focused
    });

    // Visibility API to track page visibility
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            socket.emit('page_visible');
        } else {
            socket.emit('page_hidden');
        }
    });
});