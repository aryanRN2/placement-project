// static/js/easter_egg.js

document.addEventListener('DOMContentLoaded', () => {
    let clickCount = 0;
    let lastClickTime = 0;
    const clickThreshold = 5; // Number of clicks required
    const timeLimit = 2000; // Time limit in milliseconds (2 seconds)
    let isExploding = false;

    // Listen for clicks on the whole document
    document.addEventListener('click', (e) => {
        // Only count clicks that are roughly on the "background" to avoid interfering with normal UI
        // We consider background as body, html, or main containers that don't have interactive elements
        const isBackground = e.target.tagName === 'BODY' || e.target.tagName === 'HTML' || e.target.classList.contains('container');
        
        if (!isBackground) return;

        const currentTime = new Date().getTime();

        // Reset if it's been too long since the last click
        if (currentTime - lastClickTime > timeLimit / clickThreshold) {
            clickCount = 0;
        }

        clickCount++;
        lastClickTime = currentTime;

        if (clickCount >= clickThreshold && !isExploding) {
            isExploding = true;
            clickCount = 0; // Reset
            
            const canvasExists = document.getElementById('particleCanvas');
            if (canvasExists) {
                // Trigger swirl phase in particles.js
                window.easterEggPhase = 1;
                window.swirlStartTime = Date.now();
                window.swirlCenterX = window.innerWidth / 2;
                window.swirlCenterY = window.innerHeight / 2;
                window.swirlSpeed = 0.02;
                
                // Wait 3 seconds for the swirl to accelerate, then burst!
                setTimeout(() => {
                    window.easterEggPhase = 2; // Tell particles.js to hide its particles
                    triggerEasterEgg(window.innerWidth / 2, window.innerHeight / 2);
                }, 3000);
            } else {
                // No existing particles, burst immediately from mouse position
                triggerEasterEgg(e.clientX, e.clientY);
            }
        }
    });

    function triggerEasterEgg(startX, startY) {
        isExploding = true;
        
        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.id = 'easterEggCanvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none'; // Let clicks pass through
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        const colors = ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#8E24AA', '#1a1a1a'];
        const particleCount = window.innerWidth < 600 ? 100 : 250;

        // Initialize particles
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 15 + 5; // Fast initial speed
            particles.push({
                x: startX || window.innerWidth / 2,
                y: startY || window.innerHeight / 2,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: Math.random() * 4 + 2,
                color: colors[Math.floor(Math.random() * colors.length)],
                alpha: 1,
                decay: Math.random() * 0.015 + 0.005, // How fast they fade
                gravity: 0.2 // Slight downward pull
            });
        }

        function animate() {
            if (!isExploding) return;
            
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let activeParticles = 0;

            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                if (p.alpha <= 0) continue;

                activeParticles++;

                // Physics
                p.vy += p.gravity;
                p.x += p.vx;
                p.y += p.vy;
                p.alpha -= p.decay;

                // Draw
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = Math.max(0, p.alpha);
                ctx.fill();
                ctx.globalAlpha = 1.0;
            }

            if (activeParticles > 0) {
                requestAnimationFrame(animate);
            } else {
                // Cleanup
                isExploding = false;
                document.body.removeChild(canvas);
                
                // Jump to the source page if not already there!
                if (window.location.pathname !== '/source') {
                    window.location.href = '/source';
                }
            }
        }

        animate();
    }
});
