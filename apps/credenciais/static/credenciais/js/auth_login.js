// ================================
// Eventos
// ================================

// Limpar erro
document.querySelector('#login').addEventListener('input', clearError);
document.querySelector('#password').addEventListener('input', clearError);

// Exibir senha
document.querySelector('#togglePassword').addEventListener('click', togglePasswordVisibility);

// ================================
// Funções
// ================================

// Enviar formulário
function afterSubmit(form, data) {
    try {
        if (data.result == 'success') {
            window.location.reload();
        } else {
            showMessage(data.msg);
        }
    } catch (error) {
        console.error("sendForm:", error);
        showMessage('Não foi possível realizar o login. Tente novamente.');
    }
};

// Exibir mensagem de erro
function showMessage(msg) {
    const feedbackEl = document.querySelector('#feedback');
    feedbackEl.querySelector('.callout').textContent = msg;
    feedbackEl.style.display = 'block';
}

// Limpar erro
function clearError(event) {
    const feedbackEl = document.querySelector('#feedback');
    feedbackEl.style.display = 'none';
    feedbackEl.querySelector('.callout').textContent = '';
}

// Exibir senha
function togglePasswordVisibility() {
    const passwordEl = document.querySelector('#password');
    const toggleButton = document.querySelector('#togglePassword');
    if (passwordEl.type === 'password') {
        passwordEl.type = 'text';
        toggleButton.innerHTML = '<i class="fa fa-eye-slash"></i>';
    } else {
        passwordEl.type = 'password';
        toggleButton.innerHTML = '<i class="fa fa-eye"></i>';
    }
}