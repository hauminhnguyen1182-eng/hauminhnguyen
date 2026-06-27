class AudioPlayer {
    constructor() {
        this.audio = new Audio();
        this.isPlaying = false;
    }

    async generateTTS(text, lang = 'en') {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, lang })
        });

        if (response.ok) {
            const blob = await response.blob();
            this.audio.src = URL.createObjectURL(blob);
            return true;
        }
        return false;
    }

    play() {
        this.audio.play();
        this.isPlaying = true;
    }

    pause() {
        this.audio.pause();
        this.isPlaying = false;
    }

    toggle() {
        this.isPlaying ? this.pause() : this.play();
    }
}

function addListenButton(articleId, text) {
    const article = document.getElementById(articleId);
    if (!article) return;

    const btn = document.createElement('button');
    btn.className = 'listen-btn';
    btn.innerHTML = '🔊 Listen';
    btn.onclick = async () => {
        btn.innerHTML = '⏳ Generating...';
        const player = new AudioPlayer();
        const success = await player.generateTTS(text);
        if (success) {
            btn.innerHTML = '⏸ Pause';
            player.play();
            btn.onclick = () => {
                player.toggle();
                btn.innerHTML = player.isPlaying ? '⏸ Pause' : '🔊 Listen';
            };
        } else {
            btn.innerHTML = '❌ Error';
        }
    };

    article.prepend(btn);
}