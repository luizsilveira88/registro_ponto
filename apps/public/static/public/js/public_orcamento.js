/** 
 * Elemento Estáticos 
 * */

// Inicialização
document.addEventListener('DOMContentLoaded', initOrcamento);

// Enviar formMessageulário
document.querySelector('#send').addEventListener('click', sendForm);

/***
 * Funções Principais
 */

// Enviar formulário
function sendForm(event) {
    const errorMessage = document.querySelector('#error-message');
    errorMessage.style.display = 'none';

    try {
        const form = document.querySelector('form');

        if (form.checkValidity()) {
            const formData = new FormData(form);
            const url = '/public/orcamento/save/';

            formData.set('cnpj', unMaskValue(formData.get('cnpj')));
            formData.set('telefone', unMaskValue(formData.get('telefone')));
            formData.set('whatsapp', unMaskValue(formData.get('whatsapp')));

            sendAjaxRequest(url, 'POST', formData, (response) => {
                if (response.result == 'success') {
                    renderSuccess();
                } else {
                    console.error('Erro no envio:', response);
                    renderError();
                }
            })
        } else {
            form.classList.add('was-validated');
        }

    } catch (error) {
        console.log('sendForm', error);
        renderError();
    }
}

// Exibir mensagem de erro

function renderError() {
    const errorMessage = document.querySelector('#error-message');
    errorMessage.style.display = 'block';
    errorMessage.classList.add('wow', 'fadeInUp');
}

// Exibir tela de sucesso
function renderSuccess() {
    const formMessage = document.querySelector('#form-message');
    const verifyMessage = document.querySelector('#success-message');

    formMessage.style.opacity = '1';
    formMessage.style.transition = 'opacity 0.5s ease-in-out';

    setTimeout(() => {
        formMessage.style.opacity = '0';
    }, 100);

    setTimeout(() => {
        formMessage.style.display = 'none';
        verifyMessage.style.display = 'block';
        verifyMessage.classList.add('wow', 'fadeInUp');
        new WOW().init();
    }, 600);
}

// Máscara de valor
function initVMasker() {
    // CNPJ
    VMasker(document.querySelector('#cnpj')).maskPattern("99.999.999/9999-99");

    // Telefone e Whastapp
    let telMask = ['(99) 9999-99999', '(99) 99999-9999'];
    [document.querySelector('#telefone'), document.querySelector('#whatsapp')].forEach((tel) => {
        VMasker(tel).maskPattern(telMask[0]);
        tel.addEventListener('input', inputHandler.bind(undefined, telMask, 14), false);
    });
}

/**
 * Funções auxiliares
 */

function inputHandler(masks, max, event) {
    let c = event.target;
    let v = c.value.replace(/\D/g, '');
    let m = c.value.length > max ? 1 : 0;
    VMasker(c).unMask();
    VMasker(c).maskPattern(masks[m]);
    c.value = VMasker.toPattern(v, masks[m]);
}

// Remove formatação dos valores
function unMaskValue(value) {
    if (!value) return 0;
    let string = value.replace(/[.,\/\-\(\) ]/g, '');
    return string;
}

/**
 * Inicialização
 */

function initOrcamento() {
    initVMasker();
}