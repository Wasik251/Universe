let audioCtx = null;

function getCtx() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
}

function playSound() {
    try {
        const ctx = getCtx();
        if (ctx.state === 'suspended') ctx.resume();
        const now = ctx.currentTime;
        playTone(ctx, 660, now, 0.08, 'triangle');
        playTone(ctx, 990, now + 0.1, 0.1, 'triangle');
    } catch (e) {}
}

function playTone(ctx, freq, start, duration, type) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type || 'sine';
    osc.frequency.setValueAtTime(freq, start);
    gain.gain.setValueAtTime(0.18, start);
    gain.gain.exponentialRampToValueAtTime(0.001, start + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(start);
    osc.stop(start + duration + 0.02);
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button, .btn, a.btn').forEach(el => {
        el.addEventListener('click', () => playSound());
    });
});
