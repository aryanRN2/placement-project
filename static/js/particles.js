// static/js/particles.js

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    // Settings
    const particleSpacing = 40; // Space between particles in the grid
    const particleRadius = 1.5;
    const mouseRadius = 150; // How close mouse needs to be to repel
    const repelForce = 5; // How strongly to repel
    const returnSpeed = 0.05; // How quickly particles return home

    let mouse = {
        x: undefined,
        y: undefined
    };

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        initParticles();
    }

    class Particle {
        constructor(x, y) {
            this.homeX = x;
            this.homeY = y;
            this.x = x;
            this.y = y;
            this.vx = 0;
            this.vy = 0;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, particleRadius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(39, 168, 177, 1.0)'; // Set opacity (the last number) to 1.0 for solid color
            ctx.fill();
        }

        update() {
            // Mouse Repulsion
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < mouseRadius) {
                // Force gets stronger closer to the mouse
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (mouseRadius - distance) / mouseRadius;

                // Pushing away
                this.vx -= forceDirectionX * force * repelForce;
                this.vy -= forceDirectionY * force * repelForce;
            }

            // Return home (spring/easing)
            this.vx += (this.homeX - this.x) * returnSpeed;
            this.vy += (this.homeY - this.y) * returnSpeed;

            // Apply friction/dampening
            this.vx *= 0.8;
            this.vy *= 0.8;

            this.x += this.vx;
            this.y += this.vy;

            this.draw();
        }
    }

    function initParticles() {
        particles = [];
        // Create a grid of particles
        for (let y = 0; y < height; y += particleSpacing) {
            for (let x = 0; x < width; x += particleSpacing) {
                particles.push(new Particle(x, y));
            }
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
        }
    }

    // Event Listeners
    window.addEventListener('resize', () => {
        // Simple debounce for resize
        clearTimeout(window.resizeTimer);
        window.resizeTimer = setTimeout(resize, 200);
    });

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    window.addEventListener('mouseout', () => {
        mouse.x = undefined;
        mouse.y = undefined;
    });

    // Initialize
    resize();
    animate();
});
