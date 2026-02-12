const BiometriaHome = {
    actions: {},
};

// =========================
// Eventos
// =========================

// Inicialização
document.addEventListener('DOMContentLoaded', initialize);

// Ao abrir modal, initialize Choices.js
document
    .querySelector('#modal-colaborador')
    .addEventListener('shown.bs.modal', initModalBiometria);

// Ao fechar modal, fechar a camêra
document
    .querySelector("#modal-colaborador")
    .addEventListener("hidden.bs.modal", closeModalBiometria);

// =========================
// Inicialização
// =========================

async function initialize() {
    try {
        await loadColaborador();
    } catch (error) {
        console.log('Erro de inicialização', error);
        showNotification("error", "Não foi possível listar os usuarios");
    }
}


// =========================
// Funções
// =========================

// Carregar relação de usuarios
async function loadColaborador() {
    const tableColaboradorEl = document.querySelector('#table_colaborador');
    const url = tableColaboradorEl.dataset.list;
    const urlDetail = tableColaboradorEl.dataset.detail;

    tableColaboradorEl._tabulator = new Tabulator(tableColaboradorEl, {
        ajaxURL: url,
        columns: [
            {
                title: 'Nome',
                field: 'nome',
                formatter: (cell) => `<a href="${urlDetail.replace('0', cell.getRow().getData().id)}">${cell.getValue()}</a>`,
                headerSort: false,
                responsive: 0,
            },
            {
                title: 'CNPJ',
                field: 'cnpj',
                formatter: (cell) => formatValue(cell.getValue(), "cnpj"),
                headerSort: false,
                responsive: 1,
            },
            {
                title: 'Status',
                field: 'get_status_display',
                headerSort: false,
                responsive: 0,
            },
            {
                title: 'Cidade',
                field: 'get_cidade_display',
                headerSort: false,
                responsive: 1,
            },
        ]
    });
}

async function initModalBiometria() {

    // Configurar câmera
    const canvasElement = document.querySelector("#canvas");
    const videoElement = document.querySelector("#video");
    initPicoCore(canvasElement);
    await startCamera(videoElement);
    startLoop(videoElement, PicoFace.processfn);
}

function closeModalBiometria() {
    const videoElement = document.querySelector("#video");

    stopLoop();
    stopCamera(videoElement);
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

    return data;
}

// Hook de submissão de formulário
function afterSubmit(form, data) {
    const modal = bootstrap.Modal.getInstance(document.querySelector('#modal-colaborador'));

    showNotification(data.result, data.msg);

    if (data.result == 'error') return;

    initialize();
    modal.hide();
    form.classList.remove('was-validated');
    form.reset();
}