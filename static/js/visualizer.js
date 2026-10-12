/**
 * Arc Reactor & Audio Waveform Visualizer
 * Renders an Iron Man style HUD Arc Reactor with real-time waveform oscillations.
 */
class ArcReactorVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        
        this.state = 'idle'; // idle | listening | processing | speaking
        this.rotationAngle = 0;
        this.counterRotation = 0;
        this.pulseSize = 0;
        this.particles = [];
        this.barsCount = 64;
        this.audioLevels = new Array(this.barsCount).fill(5);

        this.initCanvasSize();
        window.addEventListener('resize', () => this.initCanvasSize());
        this.animate();
    }

    initCanvasSize() {
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        this.width = rect.width || 460;
        this.height = rect.height || 460;
        this.canvas.width = this.width * dpr;
        this.canvas.height = this.height * dpr;
        this.ctx.scale(dpr, dpr);
    }

    setState(newState) {
        this.state = newState;
    }

    getThemeColors() {
        const style = getComputedStyle(document.body);
        return {
            primary: style.getPropertyValue('--primary').trim() || '#00f0ff',
            glow: style.getPropertyValue('--primary-glow').trim() || 'rgba(0, 240, 255, 0.5)',
            secondary: style.getPropertyValue('--secondary').trim() || '#0088ff'
        };
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        const ctx = this.ctx;
        const w = this.width;
        const h = this.height;
        const cx = w / 2;
        const cy = h / 2;
        const colors = this.getThemeColors();

        ctx.clearRect(0, 0, w, h);

        // Rotation increments based on state
        const speed = this.state === 'listening' ? 0.025 : (this.state === 'speaking' ? 0.018 : 0.008);
        this.rotationAngle += speed;
        this.counterRotation -= speed * 0.7;

        // 1. Outer Hologram Radar Ring with Ticks
        this.drawRadarRing(cx, cy, 210, colors);

        // 2. Segmented Rotating Gear Arcs
        this.drawSegmentedArc(cx, cy, 180, this.rotationAngle, 8, colors.primary);
        this.drawSegmentedArc(cx, cy, 155, this.counterRotation, 12, colors.secondary);

        // 3. Audio Waveform Spectrum Ring
        this.drawWaveformRing(cx, cy, 125, colors);

        // 4. Inner Orbit Rings
        this.drawInnerOrbits(cx, cy, 95, colors);

        // 5. Energy Particle Pulses
        this.drawEnergyPulses(cx, cy, colors);
    }

    drawRadarRing(cx, cy, radius, colors) {
        const ctx = this.ctx;
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        ctx.stroke();

        // Tick marks around circle
        const totalTicks = 72;
        for (let i = 0; i < totalTicks; i++) {
            const angle = (i * (Math.PI * 2)) / totalTicks;
            const isMajor = i % 6 === 0;
            const innerR = radius - (isMajor ? 8 : 4);
            const x1 = cx + Math.cos(angle) * radius;
            const y1 = cy + Math.sin(angle) * radius;
            const x2 = cx + Math.cos(angle) * innerR;
            const y2 = cy + Math.sin(angle) * innerR;

            ctx.beginPath();
            ctx.strokeStyle = isMajor ? colors.primary : 'rgba(255, 255, 255, 0.18)';
            ctx.lineWidth = isMajor ? 1.5 : 0.8;
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
        ctx.restore();
    }

    drawSegmentedArc(cx, cy, radius, angleOffset, segments, color) {
        const ctx = this.ctx;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(angleOffset);

        const arcLen = (Math.PI * 2) / segments;
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 8;
        ctx.shadowColor = color;

        for (let i = 0; i < segments; i++) {
            if (i % 2 === 0) {
                const start = i * arcLen;
                const end = start + arcLen * 0.7;
                ctx.beginPath();
                ctx.arc(0, 0, radius, start, end);
                ctx.stroke();
            }
        }
        ctx.restore();
    }

    drawWaveformRing(cx, cy, radius, colors) {
        const ctx = this.ctx;
        ctx.save();

        let stateColor = colors.primary;
        if (this.state === 'listening') stateColor = '#ffaa00';
        else if (this.state === 'speaking') stateColor = '#00ffaa';
        else if (this.state === 'processing') stateColor = '#d600ff';

        ctx.shadowBlur = 10;
        ctx.shadowColor = stateColor;
        ctx.strokeStyle = stateColor;

        const time = Date.now() * 0.005;

        for (let i = 0; i < this.barsCount; i++) {
            const angle = (i * (Math.PI * 2)) / this.barsCount;
            let barHeight = 4;

            if (this.state === 'speaking' || this.state === 'listening') {
                barHeight = 6 + Math.abs(Math.sin(time + i * 0.4) * 22) + Math.abs(Math.cos(time * 0.8 + i) * 12);
            } else if (this.state === 'processing') {
                barHeight = 4 + Math.abs(Math.sin(time * 2 + i * 0.6) * 14);
            } else {
                barHeight = 3 + Math.abs(Math.sin(time * 0.5 + i * 0.2) * 5);
            }

            const x1 = cx + Math.cos(angle) * radius;
            const y1 = cy + Math.sin(angle) * radius;
            const x2 = cx + Math.cos(angle) * (radius + barHeight);
            const y2 = cy + Math.sin(angle) * (radius + barHeight);

            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
        ctx.restore();
    }

    drawInnerOrbits(cx, cy, radius, colors) {
        const ctx = this.ctx;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(this.counterRotation * 1.5);

        ctx.strokeStyle = colors.primary;
        ctx.lineWidth = 1;
        ctx.shadowBlur = 6;
        ctx.shadowColor = colors.primary;

        // Dotted inner orbit
        ctx.setLineDash([4, 6]);
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, Math.PI * 2);
        ctx.stroke();

        ctx.restore();
    }

    drawEnergyPulses(cx, cy, colors) {
        const ctx = this.ctx;
        this.pulseSize = (this.pulseSize + 0.8) % 110;
        const alpha = Math.max(0, 1 - (this.pulseSize / 110));

        ctx.save();
        ctx.strokeStyle = colors.primary;
        ctx.globalAlpha = alpha * 0.35;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(cx, cy, 65 + this.pulseSize, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }
}
