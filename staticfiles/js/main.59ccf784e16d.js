// Main JavaScript functionality for Safe Traveller

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Theme management
function initializeTheme() {
    const theme = localStorage.getItem('theme') || 
                 (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    if (theme === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
}

function toggleTheme(theme) {
    fetch('/users/toggle-theme/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({theme: theme})
    });
    
    localStorage.setItem('theme', theme);
    
    if (theme === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
}

// PWA Installation
let deferredPrompt;

function initializePWA() {
    // Register service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js')
            .then(() => console.log('Service Worker registered'))
            .catch((error) => console.log('Service Worker registration failed:', error));
    }
    
    // Handle install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        const installBtn = document.getElementById('install-btn');
        if (installBtn) {
            installBtn.style.display = 'block';
            installBtn.addEventListener('click', installApp);
        }
    });
    
    // Handle successful installation
    window.addEventListener('appinstalled', () => {
        console.log('PWA was installed');
        const installBtn = document.getElementById('install-btn');
        if (installBtn) {
            installBtn.style.display = 'none';
        }
        deferredPrompt = null;
    });
}

function installApp() {
    const installBtn = document.getElementById('install-btn');
    if (installBtn) {
        installBtn.style.display = 'none';
    }
    
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
            } else {
                console.log('User dismissed the install prompt');
            }
            deferredPrompt = null;
        });
    }
}

// Chat functionality
class ChatManager {
    constructor() {
        this.sessionId = null;
        this.isOpen = false;
        this.initializeElements();
        this.bindEvents();
    }
    
    initializeElements() {
        this.floatingBtn = document.getElementById('floating-chat');
        this.chatPopup = document.getElementById('chat-popup');
        this.closeBtn = document.getElementById('close-chat');
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-chat');
        this.messagesContainer = document.getElementById('chat-messages');
    }
    
    bindEvents() {
        if (this.floatingBtn) {
            this.floatingBtn.addEventListener('click', () => this.openChat());
        }
        
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.closeChat());
        }
        
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (this.chatInput) {
            this.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (this.isOpen && 
                !this.chatPopup.contains(e.target) && 
                !this.floatingBtn.contains(e.target)) {
                this.closeChat();
            }
        });
    }
    
    openChat() {
        if (this.chatPopup) {
            this.chatPopup.classList.add('active');
            this.isOpen = true;
            
            // Focus input
            if (this.chatInput) {
                setTimeout(() => this.chatInput.focus(), 300);
            }
        }
    }
    
    closeChat() {
        if (this.chatPopup) {
            this.chatPopup.classList.remove('active');
            this.isOpen = false;
        }
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            const response = await fetch('/translate/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTyping();
            
            if (data.status === 'success') {
                this.addMessage(data.response, 'ai');
                this.sessionId = data.session_id;
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTyping();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
    }
    
    addMessage(text, type) {
        if (!this.messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `p-3 rounded-lg max-w-xs break-words ${
            type === 'user' 
                ? 'bg-blue-600 text-white ml-auto' 
                : 'bg-gray-200 dark:bg-slate-700 text-gray-900 dark:text-gray-100'
        }`;
        messageDiv.textContent = text;
        
        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    showTyping() {
        if (!this.messagesContainer) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'p-3 rounded-lg max-w-xs bg-gray-200 dark:bg-slate-700';
        typingDiv.innerHTML = '<div class="flex space-x-1"><div class="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div><div class="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style="animation-delay: 0.1s"></div><div class="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style="animation-delay: 0.2s"></div></div>';
        
        this.messagesContainer.appendChild(typingDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}

// Location services
class LocationManager {
    constructor() {
        this.currentPosition = null;
        this.watchId = null;
    }
    
    async getCurrentPosition() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation is not supported'));
                return;
            }
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.currentPosition = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    };
                    resolve(this.currentPosition);
                },
                (error) => {
                    reject(error);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000 // 5 minutes
                }
            );
        });
    }
    
    startWatching() {
        if (!navigator.geolocation) return;
        
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                this.currentPosition = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                
                // Dispatch custom event
                window.dispatchEvent(new CustomEvent('locationUpdate', {
                    detail: this.currentPosition
                }));
            },
            (error) => {
                console.error('Location watch error:', error);
            },
            {
                enableHighAccuracy: true,
                timeout: 30000,
                maximumAge: 60000 // 1 minute
            }
        );
    }
    
    stopWatching() {
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
    }
}

// Audio management
class AudioManager {
    constructor() {
        this.audioContext = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
    }
    
    async initialize() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (error) {
            console.error('Audio context initialization failed:', error);
        }
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                }
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm'
            });
            
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                window.dispatchEvent(new CustomEvent('recordingComplete', {
                    detail: { audioBlob }
                }));
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            return true;
        } catch (error) {
            console.error('Recording start failed:', error);
            return false;
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            this.isRecording = false;
        }
    }
    
    playAudio(audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play().catch(error => {
            console.error('Audio playback failed:', error);
        });
    }
    
    speakText(text, language = 'en') {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = language;
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            speechSynthesis.speak(utterance);
        }
    }
}

// Notification manager
class NotificationManager {
    constructor() {
        this.permission = 'default';
        this.checkPermission();
    }
    
    async checkPermission() {
        if ('Notification' in window) {
            this.permission = Notification.permission;
            
            if (this.permission === 'default') {
                this.permission = await Notification.requestPermission();
            }
        }
    }
    
    showNotification(title, options = {}) {
        if (this.permission === 'granted') {
            const notification = new Notification(title, {
                icon: '/static/images/icon-192.png',
                badge: '/static/images/icon-192.png',
                ...options
            });
            
            setTimeout(() => notification.close(), 5000);
            
            return notification;
        }
    }
    
    showWeatherAlert(message) {
        this.showNotification('Weather Alert', {
            body: message,
            icon: '/static/images/weather-icon.png'
        });
    }
    
    showTravelTip(message) {
        this.showNotification('Travel Tip', {
            body: message,
            icon: '/static/images/tip-icon.png'
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Initialize PWA
    initializePWA();
    
    // Initialize managers
    window.chatManager = new ChatManager();
    window.locationManager = new LocationManager();
    window.audioManager = new AudioManager();
    window.notificationManager = new NotificationManager();
    
    // Initialize audio context on user interaction
    document.addEventListener('click', function initAudio() {
        window.audioManager.initialize();
        document.removeEventListener('click', initAudio);
    }, { once: true });
    
    // Start location watching if on map page
    if (window.location.pathname.includes('map')) {
        window.locationManager.startWatching();
    }
    
    console.log('Safe Traveller initialized successfully');
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (window.locationManager) {
        window.locationManager.stopWatching();
    }
    
    if (window.audioManager && window.audioManager.isRecording) {
        window.audioManager.stopRecording();
    }
});

// Export for global access
window.SafeTraveller = {
    getCookie,
    toggleTheme,
    installApp
};