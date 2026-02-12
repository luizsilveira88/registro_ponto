// =========================
// Eventos
// =========================

// Inicialização
document.addEventListener('DOMContentLoaded', initialize);

// Ao abrir o modal, popular o form
document.querySelector('#modal-colaborador').addEventListener('show.bs.modal', setupModalColaborador);

// Ao abrir o modal, popular o form
document.querySelector('#modal-configuracao').addEventListener('show.bs.modal', setupModalConfiguracao);

// =========================
// Inicialização
// =========================

function initialize() {
    try {
        loadCardDadosPrincipais();
        loadCardConfiguracoes();

    } catch (error) {
        console.error('Erro de inicialização', error);
    }
}


// =========================
// Funções
// =========================

// Carregar dados principais do colaborador
async function loadCardDadosPrincipais() {
    const cardDadosPrincipais = document.querySelector('#card-dados-principais');
    const url = cardDadosPrincipais.dataset.url;

    const data = await populateCard(url, cardDadosPrincipais);

    const titleEl = document.querySelector('#title');
    if (titleEl && data.data.nome) {
        titleEl.textContent = data.data.nome;
    }
}

// Carregar configurações do colaborador
async function loadCardConfiguracoes() {
    const cardConfiguracoes = document.querySelector('#card-configuracoes');
    const url = cardConfiguracoes.dataset.url;

    populateCard(url, cardConfiguracoes);
}

// Configurar modal de colaborador
function setupModalColaborador() {
    const modalEl = document.querySelector('#modal-colaborador');
    const form = modalEl.querySelector('form');
    const url = form.dataset.url;
    const prefix = 'id';
    populateForm(url, form, prefix);
}

// Configurar modal de configuração
function setupModalConfiguracao() {
    const modalEl = document.querySelector('#modal-configuracao');
    const form = modalEl.querySelector('form');
    const url = form.dataset.url;
    const prefix = 'id';
    populateForm(url, form, prefix);
}

// =========================
// Hooks
// =========================

// Prepara imagem para envio
async function beforeSubmit(form, data) {
    const videoElement = document.querySelector("#video");
    const canvas = captureFrame(videoElement);
    const blob = await canvasToBlob(canvas);
    data.append("image", blob, "biometric.jpg");


    console.log(data);

    return data;
}

// Hook após submissão do formulário
function afterSubmit(form, response) {
    showNotification(response.result, response.msg);

    if (response.result == 'error') return;

    const modalEl = form.closest('.modal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();

    switch (form.id) {
        case 'form-colaborador':
            loadCardDadosPrincipais();
            break;
        case 'form-configuracao':
            loadCardConfiguracoes();
            break;
    }
}