// ====== MODAL CANTIK ======
const modal = document.createElement('div');
modal.id = 'session-modal';
modal.innerHTML = `
    <div id="modal-overlay" style="position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:9999; backdrop-filter:blur(4px);">
        <div style="background:white; padding:24px; border-radius:16px; max-width:400px; width:90%; box-shadow:0 20px 25px -5px rgba(0,0,0,0.2); animation:slideUp 0.3s ease-out;">
            
            <!-- Header dengan icon -->
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="width:48px; height:48px; background:#FEF3C7; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                </div>
                <h3 style="font-size:20px; font-weight:600; color:#1F2937; margin:0;">Session Akan Berakhir</h3>
            </div>
            
            <!-- Countdown -->
            <p style="color:#4B5563; margin-bottom:24px; font-size:16px;">
                Sesi Anda akan berakhir dalam 
                <span id="countdown" style="font-weight:700; color:#D97706; font-size:24px; display:block; text-align:center; margin:10px 0;">5</span>
                detik
            </p>
            
            <!-- Tombol -->
            <div style="display:flex; gap:12px;">
                <button id="extendBtn" style="flex:1; background:#0047AB; color:white; padding:12px; border:none; border-radius:8px; font-weight:500; cursor:pointer; transition:background 0.2s;">
                    Lanjutkan Sesi
                </button>
                <button id="logoutBtn" style="flex:1; background:#E5E7EB; color:#374151; padding:12px; border:none; border-radius:8px; font-weight:500; cursor:pointer; transition:background 0.2s;">
                    Logout
                </button>
            </div>
        </div>
    </div>
`;

// Tambah animasi
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    #extendBtn:hover { background: #003380; }
    #logoutBtn:hover { background: #D1D5DB; }
`;
document.head.appendChild(style);

modal.style.display = 'none';
document.body.appendChild(modal);

// ====== TIMER ======
let warningTimer, logoutTimer;

function startTimers() {
    if (window.location.pathname === '/login/') return;
    
    clearTimeout(warningTimer);
    clearTimeout(logoutTimer);
    
    const sessionMenit = 1; // 1 menit buat test
    const warningDetik = 5;
    
    const warningTime = (sessionMenit * 60 - warningDetik) * 1000;
    const logoutTime = sessionMenit * 60 * 1000;
    
    warningTimer = setTimeout(() => {
        console.log('⚠️ WARNING MUNCUL');
        modal.style.display = 'block';
        
        let detik = warningDetik;
        const counter = document.getElementById('countdown');
        
        // HENTIKAN INTERVAL LAMA KALAU ADA
        if (countdownInterval) {
            clearInterval(countdownInterval);
        }
        
        countdownInterval = setInterval(() => {  // <-- SIMPAN KE VARIABLE GLOBAL
            detik--;
            if (counter) counter.textContent = detik;
            
            if (detik <= 0) {
                clearInterval(countdownInterval);
                modal.style.display = 'none';
                window.location.href = '/login/?expired=1';
            }
        }, 1000);
        
    }, warningTime);
    
    logoutTimer = setTimeout(() => {
        console.log('🔄 LOGOUT OTOMATIS');
        window.location.href = '/login/?expired=1';
    }, logoutTime);
}

// ====== EVENT LISTENER ======
document.addEventListener('DOMContentLoaded', startTimers);

// Extend session
let countdownInterval; // <-- TAMBAHKAN VARIABLE GLOBAL

document.addEventListener('click', function(e) {
    if (e.target.id === 'extendBtn') {
        // HENTIKAN COUNTDOWN
        if (countdownInterval) {
            clearInterval(countdownInterval);
        }
        
        modal.style.display = 'none';
        fetch('/api/extend-session/');
        startTimers();
    }
});

// Logout manual
document.addEventListener('click', function(e) {
    if (e.target.id === 'logoutBtn') {
        window.location.href = '/login/?expired=1';
    }
});

// Reset timer setiap aktivitas
['click', 'keypress', 'mousemove', 'scroll'].forEach(event => {
    document.addEventListener(event, startTimers);
});