// Almacenamiento de estado
let flashMessageQueue = [];

// Función para mostrar mensajes
function displayFlashMessages() {
    const container = document.getElementById("flash-messages");
    container.innerHTML = "";
    
    flashMessageQueue.forEach(([category, message]) => {
        const div = document.createElement("div");
        div.className = `alert alert__${category}`;
        div.innerHTML = `
            <span>${message}</span>
            <button class="close" onclick="this.parentElement.remove();">×</button>
        `;
        container.appendChild(div);
    });
    
    // Confirmar al servidor que los mensajes fueron mostrados
    if (flashMessageQueue.length > 0) {
        fetch('/clear_flash_messages', { method: 'POST' });
        flashMessageQueue = [];
    }
}

// Función para cargar mensajes cuando sea necesario
function loadFlashMessages() {
    fetch('/get_flashed_messages')
        .then(response => response.json())
        .then(messages => {
            if (messages.length > 0) {
                flashMessageQueue = messages;
                displayFlashMessages();
            }
        });
}

// Llamar después de acciones
document.querySelectorAll('.btn__info').forEach(btn => {
    btn.addEventListener('click', () => {
        setTimeout(loadFlashMessages, 500);
    });
});

// Función de cierre manual de alert
function cerrarAlert(boton) {
    const alerta = boton.closest('.alert');
    if (alerta) {
        alerta.remove();
    }
}

// Auto-cierre después de 7 segundos
function configurarAutoCierre() {
    document.querySelectorAll('.alert:not([data-persist])').forEach(alerta => {
        setTimeout(() => {
            if (document.body.contains(alerta)) {
                alerta.remove();
            }
        }, 7000);
    });
}

// Observador para alertas dinámicas
const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
            configurarAutoCierre();
        }
    });
});

observer.observe(document.body, { childList: true, subtree: true });


document.addEventListener('DOMContentLoaded', configurarAutoCierre);


// Quitar formato 'active' de las opciones al ir al inicio
document.querySelector('.sidebar__logo a')?.addEventListener('click', () => {
  document.querySelectorAll('.sidebar__options--link').forEach(item => item.classList.remove('active'));
});