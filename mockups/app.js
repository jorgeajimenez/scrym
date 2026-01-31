// Tab Switching Logic
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and views
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));

        // Add active class to clicked button and target view
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
    });
});

// Send to QB Logic
window.sendToQB = function(code) {
    const overlay = document.getElementById('qb-comms-overlay');
    const display = document.getElementById('wristband-display');
    
    display.textContent = code;
    overlay.classList.remove('hidden');

    // Auto-hide after 2 seconds
    setTimeout(() => {
        overlay.classList.add('hidden');
    }, 2000);
}

// Simulation Loop (Just for visual life)
setInterval(() => {
    const clock = document.querySelector('.play-clock');
    if(clock) {
        let [min, sec] = clock.textContent.split(':').map(Number);
        if (sec > 0) {
            sec--;
            clock.textContent = `${min}:${sec < 10 ? '0' + sec : sec}`;
            if (sec < 10) clock.style.color = '#ef4444'; // Red alert
        }
    }
}, 1000);
