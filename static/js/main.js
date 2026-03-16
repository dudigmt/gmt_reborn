// Custom Modal for Session Warning
const SessionModal = {
    modal: null,
    
    init() {
        // Only initialize if we're not on login page
        if (window.location.pathname === '/login/') return;
        
        // Create modal element
        this.modal = document.createElement('div');
        this.modal.id = 'session-modal';
        this.modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden';
        this.modal.innerHTML = `
            <div class="bg-white rounded-xl shadow-2xl max-w-md w-full mx-4 transform transition-all">
                <div class="p-6">
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
                            <i class="fa-solid fa-triangle-exclamation text-yellow-600 text-xl"></i>
                        </div>
                        <h3 class="text-xl font-semibold text-gray-800">Session akan berakhir</h3>
                    </div>
                    
                    <p class="text-gray-600 mb-6">
                        Sesi Anda akan berakhir dalam <span id="session-countdown" class="font-bold text-yellow-600">30</span> detik.
                        <br>Apakah Anda ingin melanjutkan?
                    </p>
                    
                    <div class="flex gap-3">
                        <button id="extend-session" class="flex-1 bg-cobalt hover:bg-cobalt/80 text-white py-2.5 rounded-lg font-medium transition-colors">
                            Lanjutkan Sesi
                        </button>
                        <button id="logout-now" class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 py-2.5 rounded-lg font-medium transition-colors">
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.modal);
        
        // Bind events
        document.getElementById('extend-session').addEventListener('click', () => this.extend());
        document.getElementById('logout-now').addEventListener('click', () => this.logout());
        
        // Start timers only on dashboard
        if (window.location.pathname !== '/login/') {
            resetTimers();
        }
    },
    
    show(countdown = 30) {
        this.modal.classList.remove('hidden');
        this.startCountdown(countdown);
    },
    
    hide() {
        this.modal.classList.add('hidden');
        if (this.countdownInterval) {
            clearInterval(this.countdownInterval);
        }
    },
    
    startCountdown(seconds) {
        const counter = document.getElementById('session-countdown');
        let remaining = seconds;
        
        this.countdownInterval = setInterval(() => {
            remaining--;
            counter.textContent = remaining;
            
            if (remaining <= 0) {
                clearInterval(this.countdownInterval);
                this.logout();
            }
        }, 1000);
    },
    
    extend() {
        fetch('/api/extend-session/')
            .then(() => {
                this.hide();
                resetTimers();
            });
    },
    
    logout() {
        window.location.href = '/login/';
    }
};

// Session check with heartbeat - ONLY ON DASHBOARD
function checkSession() {
    // Skip if on login page
    if (window.location.pathname === '/login/') return;
    
    fetch('/api/check-session/')
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/login/';
            }
        })
        .catch(() => {
            window.location.href = '/login/';
        });
}

// Auto logout warning
let warningTimer;
let logoutTimer;

function resetTimers() {
    // Skip if on login page
    if (window.location.pathname === '/login/') return;
    
    clearTimeout(warningTimer);
    clearTimeout(logoutTimer);
    
    // Show warning after 1770 seconds (29.5 minutes)
    warningTimer = setTimeout(() => {
        SessionModal.show(30);
    }, 1770000);
    
    // Force logout after 1800 seconds (30 minutes)
    logoutTimer = setTimeout(() => {
        window.location.href = '/login/';
    }, 1800000);
}

// Initialize modal
document.addEventListener('DOMContentLoaded', () => {
    SessionModal.init();
});

// Reset timers on user activity - ONLY ON DASHBOARD
['click', 'keypress', 'scroll', 'mousemove'].forEach(event => {
    document.addEventListener(event, () => {
        if (window.location.pathname !== '/login/') {
            resetTimers();
        }
    });
});

// Check session every 60 seconds - ONLY ON DASHBOARD
setInterval(() => {
    if (window.location.pathname !== '/login/') {
        checkSession();
    }
}, 60000);
