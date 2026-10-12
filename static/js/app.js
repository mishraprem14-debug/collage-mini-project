/**
 * JARVIS 2.0 ULTRA — Core Application Controller
 * Handles Speech Recognition, WebSockets, Sound Synthesis, Telemetry & UI Interactions.
 */

// Audio Synthesizer for Sci-Fi Sound FX (Zero external dependencies)
class SoundFXSynthesizer {
    constructor() {
        this.enabled = true;
        this.ctx = null;
    }

    initCtx() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
    }

    play(type) {
        if (!this.enabled) return;
        this.initCtx();
        if (!this.ctx) return;

        const ctx = this.ctx;
        if (ctx.state === 'suspended') ctx.resume();

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);

        const now = ctx.currentTime;

        if (type === 'wake') {
            // Futuristic double chirp
            osc.type = 'sine';
            osc.frequency.setValueAtTime(520, now);
            osc.frequency.exponentialRampToValueAtTime(1040, now + 0.15);
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
            osc.start(now);
            osc.stop(now + 0.22);
        } else if (type === 'success') {
            // High-tech chord chime
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(880, now);
            osc.frequency.setValueAtTime(1320, now + 0.1);
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
            osc.start(now);
            osc.stop(now + 0.35);
        } else if (type === 'click') {
            // Crisp cybernetic tick
            osc.type = 'sine';
            osc.frequency.setValueAtTime(1800, now);
            gain.gain.setValueAtTime(0.08, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
            osc.start(now);
            osc.stop(now + 0.05);
        } else if (type === 'error') {
            // Low warning pulse
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.exponentialRampToValueAtTime(110, now + 0.25);
            gain.gain.setValueAtTime(0.18, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
            osc.start(now);
            osc.stop(now + 0.28);
        }
    }
}

// Main Controller
document.addEventListener('DOMContentLoaded', () => {
    const visualizer = new ArcReactorVisualizer('visualizerCanvas');
    const sfx = new SoundFXSynthesizer();

    // DOM Elements
    const micButton = document.getElementById('micCoreButton');
    const backendListenBtn = document.getElementById('backendListenBtn');
    const commandInput = document.getElementById('commandInput');
    const sendBtn = document.getElementById('sendBtn');
    const liveTranscriptText = document.getElementById('liveTranscriptText');
    const transcriptState = document.getElementById('transcriptState');
    const statusLabel = document.getElementById('statusLabel');
    const statusIndicator = document.getElementById('statusIndicator');
    const logContainer = document.getElementById('logContainer');
    const themeSelect = document.getElementById('themeSelect');
    const sfxToggleBtn = document.getElementById('sfxToggleBtn');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const clearLogBtn = document.getElementById('clearLogBtn');
    const exportLogBtn = document.getElementById('exportLogBtn');
    const volumeSlider = document.getElementById('volumeSlider');
    const muteBtn = document.getElementById('muteBtn');

    // Telemetry Elements
    const cpuValue = document.getElementById('cpuValue');
    const cpuBar = document.getElementById('cpuBar');
    const cpuCores = document.getElementById('cpuCores');
    const ramValue = document.getElementById('ramValue');
    const ramBar = document.getElementById('ramBar');
    const ramDetail = document.getElementById('ramDetail');
    const batteryValue = document.getElementById('batteryValue');
    const batteryBar = document.getElementById('batteryBar');
    const batteryState = document.getElementById('batteryState');
    const volumeValue = document.getElementById('volumeValue');
    const uptimeValue = document.getElementById('uptimeValue');
    const osValue = document.getElementById('osValue');
    const hudClock = document.getElementById('hudClock');
    const hudDate = document.getElementById('hudDate');

    // Modal Elements
    const screenshotModal = document.getElementById('screenshotModal');
    const modalScreenshotImg = document.getElementById('modalScreenshotImg');
    const modalDownloadBtn = document.getElementById('modalDownloadBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');

    let isListening = false;
    let recognition = null;
    let ws = null;

    // Theme Management
    const savedTheme = localStorage.getItem('jarvis-theme') || 'theme-cyan';
    document.body.className = savedTheme;
    themeSelect.value = savedTheme;

    themeSelect.addEventListener('change', (e) => {
        document.body.className = e.target.value;
        localStorage.setItem('jarvis-theme', e.target.value);
        sfx.play('click');
    });

    // SFX Toggle
    sfxToggleBtn.addEventListener('click', () => {
        sfx.enabled = !sfx.enabled;
        sfxToggleBtn.textContent = sfx.enabled ? '🔊' : '🔇';
        sfxToggleBtn.style.opacity = sfx.enabled ? '1' : '0.5';
    });

    // Fullscreen Toggle
    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(() => {});
        } else {
            document.exitFullscreen().catch(() => {});
        }
    });

    // Initialize Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micButton.classList.add('listening');
            visualizer.setState('listening');
            updateStatus('LISTENING...', '#ffaa00');
            transcriptState.textContent = 'LISTENING TO AUDIO STREAM...';
            liveTranscriptText.textContent = 'Listening to your voice...';
            sfx.play('wake');
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            const current = finalTranscript || interimTranscript;
            if (current) {
                liveTranscriptText.textContent = `"${current}"`;
            }
            if (finalTranscript) {
                recognition.stop();
                handleExecuteCommand(finalTranscript.trim());
            }
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            stopListeningState();
            liveTranscriptText.textContent = `Speech detection notice: ${event.error}. You can also type commands.`;
        };

        recognition.onend = () => {
            stopListeningState();
        };
    } else {
        console.warn('Web Speech API not supported in this browser. Falling back to backend microphone.');
        transcriptState.textContent = 'WEB SPEECH NOT SUPPORTED (USING PC MIC)';
    }

    function startListening() {
        if (recognition) {
            try {
                recognition.start();
            } catch (err) {
                console.warn('Recognition start error:', err);
            }
        } else {
            listenViaBackend();
        }
    }

    function stopListeningState() {
        isListening = false;
        micButton.classList.remove('listening');
        if (visualizer.state === 'listening') {
            visualizer.setState('idle');
            updateStatus('SYSTEM STANDBY', 'var(--primary)');
            transcriptState.textContent = 'VOICE RECOGNITION READY';
        }
    }

    micButton.addEventListener('click', () => {
        if (!isListening) {
            startListening();
        } else {
            if (recognition) recognition.stop();
            stopListeningState();
        }
    });

    // Backend Microphone Trigger
    backendListenBtn.addEventListener('click', () => {
        listenViaBackend();
    });

    async function listenViaBackend() {
        sfx.play('wake');
        visualizer.setState('listening');
        micButton.classList.add('listening');
        updateStatus('PC MIC LISTENING...', '#ffaa00');
        liveTranscriptText.textContent = 'Listening through computer microphone... Speak now.';
        
        try {
            const resp = await fetch('/api/listen', { method: 'POST' });
            const data = await resp.json();
            stopListeningState();
            
            if (data.transcription) {
                liveTranscriptText.textContent = `"${data.transcription}"`;
                addLogEntry('user', `Voice Command: "${data.transcription}"`);
                handleCommandResponse(data);
            } else if (data.error) {
                liveTranscriptText.textContent = data.error;
                addLogEntry('system', `Microphone Notice: ${data.error}`);
                sfx.play('error');
            }
        } catch (e) {
            stopListeningState();
            liveTranscriptText.textContent = 'Error connecting to backend microphone.';
            sfx.play('error');
        }
    }

    // Command Dispatch
    async function handleExecuteCommand(commandText) {
        if (!commandText || !commandText.trim()) return;

        sfx.play('click');
        commandInput.value = '';
        addLogEntry('user', `Command: "${commandText}"`);

        visualizer.setState('processing');
        updateStatus('ANALYZING DIRECTIVE...', '#d600ff');
        transcriptState.textContent = 'NEURAL PARSER PROCESSING';
        liveTranscriptText.textContent = `Processing directive: "${commandText}"...`;

        try {
            const resp = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: commandText, speak_response: true })
            });

            const data = await resp.json();
            handleCommandResponse(data);
        } catch (err) {
            console.error('Command API error:', err);
            visualizer.setState('idle');
            updateStatus('COMMAND ERROR', 'var(--danger)');
            addLogEntry('system', `Failed to execute: ${err.message}`);
            sfx.play('error');
        }
    }

    function handleCommandResponse(data) {
        const speech = data.speech || data.display || 'Order executed.';
        const targetUrl = (data.url && data.action !== 'screenshot') ? data.url : null;

        if (targetUrl) {
            liveTranscriptText.innerHTML = `${speech} &nbsp; <a href="${targetUrl}" target="_blank" class="hud-inline-link">🚀 Open Tab ↗</a>`;
        } else {
            liveTranscriptText.textContent = speech;
        }

        addLogEntry('jarvis', speech, targetUrl);
        sfx.play('success');

        // CRITICAL: Automatically open website/YouTube tab in browser
        if (targetUrl) {
            console.log('Navigating browser to URL:', targetUrl);
            try {
                const win = window.open(targetUrl, '_blank');
                if (win) {
                    win.focus();
                }
            } catch (err) {
                console.warn('Browser window.open notice:', err);
            }
        }

        // Visualizer Speaking Animation
        visualizer.setState('speaking');
        micButton.classList.add('speaking');
        updateStatus('JARVIS RESPONDING', '#00ffaa');

        // Check if screenshot was returned
        if (data.action === 'screenshot' && data.url) {
            modalScreenshotImg.src = data.url;
            modalDownloadBtn.href = data.url;
            screenshotModal.classList.add('active');
        }

        // Return to idle after speech finishes (estimate ~70ms per character)
        const duration = Math.min(8000, Math.max(2000, speech.length * 65));
        setTimeout(() => {
            visualizer.setState('idle');
            micButton.classList.remove('speaking');
            updateStatus('SYSTEM STANDBY', 'var(--primary)');
            transcriptState.textContent = 'READY FOR DIRECTIVES';
        }, duration);
    }

    sendBtn.addEventListener('click', () => {
        handleExecuteCommand(commandInput.value);
    });

    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            handleExecuteCommand(commandInput.value);
        }
    });

    // Suggestion Chips
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-query');
            handleExecuteCommand(query);
        });
    });

    // Direct Action Dock Buttons
    document.querySelectorAll('.dock-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const cmd = btn.getAttribute('data-cmd');
            handleExecuteCommand(cmd);
        });
    });

    // Volume Slider & Mute
    volumeSlider.addEventListener('input', (e) => {
        volumeValue.textContent = `${e.target.value}%`;
    });

    volumeSlider.addEventListener('change', async (e) => {
        sfx.play('click');
        try {
            await fetch('/api/volume', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ level: parseInt(e.target.value) })
            });
            addLogEntry('system', `Master Volume adjusted to ${e.target.value}%`);
        } catch (err) {
            console.error('Volume change error:', err);
        }
    });

    muteBtn.addEventListener('click', () => {
        handleExecuteCommand('mute');
    });

    // Close Modal
    closeModalBtn.addEventListener('click', () => {
        screenshotModal.classList.remove('active');
    });

    screenshotModal.addEventListener('click', (e) => {
        if (e.target === screenshotModal) {
            screenshotModal.classList.remove('active');
        }
    });

    // Log Activity Helpers
    function addLogEntry(type, text, url = null) {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;

        const badge = document.createElement('div');
        badge.className = 'log-badge';
        badge.textContent = type === 'user' ? 'USER DIRECTIVE' : (type === 'jarvis' ? 'JARVIS CORE' : 'SYS NOTIFY');

        const content = document.createElement('div');
        content.className = 'log-content';

        const p = document.createElement('p');
        p.textContent = text;
        content.appendChild(p);

        if (url) {
            const link = document.createElement('a');
            link.className = 'log-url-link';
            link.href = url;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.innerHTML = `🌐 OPEN LINK: <span>${url}</span> ↗`;
            content.appendChild(link);
        }

        const time = document.createElement('span');
        time.className = 'log-time';
        time.textContent = new Date().toLocaleTimeString();

        content.appendChild(time);
        entry.appendChild(badge);
        entry.appendChild(content);

        logContainer.appendChild(entry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    clearLogBtn.addEventListener('click', () => {
        logContainer.innerHTML = '';
        addLogEntry('system', 'Neural history log cleared.');
        sfx.play('click');
    });

    exportLogBtn.addEventListener('click', () => {
        const text = logContainer.innerText;
        const blob = new Blob([text], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `jarvis_log_${Date.now()}.txt`;
        a.click();
        sfx.play('click');
    });

    function updateStatus(label, color) {
        statusLabel.textContent = label;
        statusLabel.style.color = color;
        statusIndicator.style.backgroundColor = color;
        statusIndicator.style.boxShadow = `0 0 10px ${color}`;
    }

    // Telemetry Update
    function updateTelemetry(stats) {
        if (!stats) return;

        // CPU
        cpuValue.textContent = `${stats.cpu_percent}%`;
        cpuBar.style.width = `${Math.min(100, stats.cpu_percent)}%`;
        if (stats.cpu_count) cpuCores.textContent = `Logical Cores: ${stats.cpu_count}`;

        // RAM
        ramValue.textContent = `${stats.ram_percent}%`;
        ramBar.style.width = `${Math.min(100, stats.ram_percent)}%`;
        ramDetail.textContent = `${stats.ram_used_gb} GB / ${stats.ram_total_gb} GB`;

        // Battery
        if (stats.battery) {
            batteryValue.textContent = `${stats.battery.percent}%`;
            batteryBar.style.width = `${stats.battery.percent}%`;
            batteryState.textContent = stats.battery.power_plugged ? 'Status: AC Charging' : 'Status: On Battery';
        }

        // Volume
        if (stats.volume_percent !== undefined) {
            volumeValue.textContent = `${stats.volume_percent}%`;
            if (document.activeElement !== volumeSlider) {
                volumeSlider.value = stats.volume_percent;
            }
        }

        // System Info
        if (stats.uptime) uptimeValue.textContent = stats.uptime;
        if (stats.os_name) osValue.textContent = stats.os_name;
        if (stats.time_str) hudClock.textContent = stats.time_str;
        if (stats.date_str) hudDate.textContent = stats.date_str;
    }

    // Connect WebSocket
    function connectTelemetryWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;

        ws = new WebSocket(wsUrl);

        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                if (msg.type === 'telemetry') {
                    updateTelemetry(msg.data);
                }
            } catch (err) {
                console.error('WS parse error:', err);
            }
        };

        ws.onclose = () => {
            console.log('WS disconnected. Reconnecting in 3 seconds...');
            setTimeout(connectTelemetryWebSocket, 3000);
        };

        ws.onerror = () => {
            ws.close();
        };
    }

    connectTelemetryWebSocket();

    // Fallback Poll
    setInterval(async () => {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            try {
                const resp = await fetch('/api/system-stats');
                const stats = await resp.json();
                updateTelemetry(stats);
            } catch (e) {}
        }
    }, 2000);
});
