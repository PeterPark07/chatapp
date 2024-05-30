function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
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

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    setCookie("dark_mode", document.body.classList.contains('dark-mode'), 7);
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

    socket.on('message', function(data) {
        const chatMessages = document.querySelector('.chat-messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', data.username === username ? 'sent' : 'received');
        messageElement.innerHTML = `
            <div class="header">
                <span class="username">${data.username}</span>
                <span class="time">${data.time}</span>
            </div>
            <span class="text">${data.message}</span>
        `;

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
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

    socket.on('toggle_dark_mode', function() {
        toggleDarkMode();
    });

    socket.on('users_online', function(count) {
        document.getElementById('users-online').innerText = `Users online: ${count}`;
    });

    document.querySelector('.chat-input').addEventListener('submit', function(e) {
        e.preventDefault();
        const messageInput = this.elements['message'];
        const message = messageInput.value;
        socket.send({username: username, message: message});
        messageInput.value = '';
        messageInput.focus();  // Keep the input field focused
    });
});