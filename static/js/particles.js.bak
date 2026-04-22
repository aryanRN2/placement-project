// static/js/particles.js

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    // Settings
    const particleSpacing = 45; // Slightly less dense
    const particleRadius = 1.2; // Slightly smaller dots
    const mouseRadius = 150; 
    const repelForce = 5; 
    const returnSpeed = 0.05; 

    // Google-esque color palette
    const colors = [
        '#4285F4', // Blue
        '#EA4335', // Red
        '#FBBC05', // Yellow
        '#34A853', // Green
        '#8E24AA', // Purple
        '#1a1a1a'  // Dark Gray
    ];

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
        constructor(x, y, isShape = false) {
            this.isShape = isShape;
            this.homeX = x;
            this.homeY = y;
            
            if (this.isShape) {
                // Shape particles start randomly on screen, then form the shape and become still
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.driftSpeed = 0; 
                this.driftRadius = 0;
            } else {
                // Background particles start at their grid points and drift widely
                this.x = x;
                this.y = y;
                this.driftSpeed = 0.0002 + Math.random() * 0.0005; 
                this.driftRadius = 50 + Math.random() * 150; 
            }
            
            this.vx = 0;
            this.vy = 0;
            // Randomly select a color from the palette for this particle
            this.color = colors[Math.floor(Math.random() * colors.length)];
            
            // Random drift settings for constant organic motion
            this.randomOffset = Math.random() * Math.PI * 2;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, particleRadius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
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

            // Calculate a drifting target home instead of a fixed home
            const time = Date.now();
            const targetX = this.homeX + Math.cos(time * this.driftSpeed + this.randomOffset) * this.driftRadius;
            const targetY = this.homeY + Math.sin(time * this.driftSpeed + this.randomOffset) * this.driftRadius;

            // Return to drifting target (spring/easing)
            this.vx += (targetX - this.x) * returnSpeed;
            this.vy += (targetY - this.y) * returnSpeed;

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
        
        if (window.PARTICLE_SHAPE === 'login' || window.PARTICLE_SHAPE === 'register') {
            // Draw shape on hidden canvas to extract pixel data
            const tCanvas = document.createElement('canvas');
            tCanvas.width = width;
            tCanvas.height = height;
            const tCtx = tCanvas.getContext('2d');

            tCtx.save();
            if (window.PARTICLE_SHAPE === 'login') {
                // Position on right side of screen
                tCtx.translate(width * 0.70, height * 0.5);
            } else {
                // Position on left side of screen for register
                tCtx.translate(width * 0.30, height * 0.5);
            }
            // Scale up massively
            const scale = Math.min(width, height) / 30; 
            tCtx.scale(scale, scale);
            // Center the 24x24 icon
            tCtx.translate(-12, -12);

            tCtx.lineWidth = 3;
            tCtx.strokeStyle = 'white';
            tCtx.lineCap = 'round';
            tCtx.lineJoin = 'round';

            if (window.PARTICLE_SHAPE === 'login') {
                // Circular Login/Enter Icon
                const p1 = new Path2D('M 9 4 A 9 9 0 1 1 9 20');
                const p2 = new Path2D('M 2 12 H 13');
                const p3 = new Path2D('M 9 8 L 13 12 L 9 16');
                
                tCtx.stroke(p1);
                tCtx.stroke(p2);
                tCtx.stroke(p3);
            } else if (window.PARTICLE_SHAPE === 'register') {
                // Document with Pencil Icon
                const p1 = new Path2D('M 5 3 C 4 3 3 4 3 5 V 21 C 3 22 4 23 5 23 H 11'); 
                const p2 = new Path2D('M 5 3 H 17 C 18 3 19 4 19 5 V 10'); 
                const p3 = new Path2D('M 7 7 H 15'); 
                const p4 = new Path2D('M 7 11 H 15'); 
                const p5 = new Path2D('M 7 15 H 12'); 
                const p6 = new Path2D('M 7 19 H 10'); 
                const p7 = new Path2D('M 12 22 L 14 17 L 20 11 L 23 14 L 17 20 Z'); 
                const p8 = new Path2D('M 14 17 L 17 20'); 
                const p9 = new Path2D('M 19 12 L 22 15'); 
                
                tCtx.stroke(p1);
                tCtx.stroke(p2);
                tCtx.stroke(p3);
                tCtx.stroke(p4);
                tCtx.stroke(p5);
                tCtx.stroke(p6);
                tCtx.stroke(p7);
                tCtx.stroke(p8);
                tCtx.stroke(p9);
            }
            tCtx.restore();

            const imgData = tCtx.getImageData(0, 0, width, height).data;
            const spacing = 5; // Density of particles in the shape
            
            for (let y = 0; y < height; y += spacing) {
                for (let x = 0; x < width; x += spacing) {
                    const index = (y * width + x) * 4;
                    const alpha = imgData[index + 3];
                    if (alpha > 128) {
                        // Valid pixel spot, add small random jitter
                        const jx = x + (Math.random() - 0.5) * spacing;
                        const jy = y + (Math.random() - 0.5) * spacing;
                        particles.push(new Particle(jx, jy, true));
                    }
                }
            }
            
            // Add sparse background particles
            for (let y = 0; y < height; y += particleSpacing * 2.5) {
                for (let x = 0; x < width; x += particleSpacing * 2.5) {
                    particles.push(new Particle(x, y, false));
                }
            }

        } else {
            // Default Grid
            for (let y = 0; y < height; y += particleSpacing) {
                for (let x = 0; x < width; x += particleSpacing) {
                    particles.push(new Particle(x, y, false));
                }
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
