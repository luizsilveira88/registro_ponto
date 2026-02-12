// =========================
// Elementos Globais
// =========================

const ColaboradorDetail = {
    dadosPrincipais: [],
    permissoes: [],
    promocoes: [],
}

// =========================
// Elementos Estáticos
// =========================

// Inicialização
document.addEventListener('DOMContentLoaded', initColaboradorDetail);

// Editar Permissões
document.querySelector('#btn-edit-permissoes').addEventListener('click', showModalPermissoes);

// Gerar Voucher
document.querySelector('#btn-codigo-promocional').addEventListener('click', savePromocao);

// =========================
// Carregamentos
// =========================

async function loadDadosPrincipais() {
    try {
        const response = await receiveAjaxRequest(jsVars.url.colaborador.getById);
        ColaboradorDetail.dadosPrincipais = response.data;

        fillFieldsRecursively(ColaboradorDetail.dadosPrincipais);
    } catch (error) {
        console.error(error);
    }
}

async function loadPermissoes() {
    try {
        const response = await receiveAjaxRequest(jsVars.url.colaborador.getPermissionsById);
        ColaboradorDetail.permissoes = response.data;

        let html = '';
        ColaboradorDetail.permissoes.forEach(permissao => {
            html += `
                <div class="mb-3">
                    <i class="fa fa-check me-2"></i> ${permissao.name}
                </div>
            `;
        })

        const permissoesEl = document.querySelector('#permissoes');
        permissoesEl.innerHTML = html;
    } catch (error) {
        console.error(error);
    }
}

async function loadPromocoes() {
    try {
        const response = await receiveAjaxRequest(jsVars.url.promocao.findByColaborador.replace(0, ColaboradorDetail.dadosPrincipais.id));
        ColaboradorDetail.promocoes = response.data;

        if (!ColaboradorDetail.promocoes.length) {
            return;
        }

        const promocoesEl = document.querySelector('#promocoes');
        promocoesEl.innerHTML = '';

        ColaboradorDetail.promocoes.forEach(promocao => {
            const html = `
                <div class="mb-3 border-bottom">
                    <div class="mb-1">Código promocional: ${promocao.codigo}</div>
                    <div class="mb-1">Dias promocionais: ${promocao.validade_dias}</div>
                    <div class="mb-1">Data de inicio: ${promocao.inicio || 'Não iniciou'}</div>
                    <div class="mb-1">Status: ${promocao.get_status_display}</div>
                </div>
            `
            promocoesEl.insertAdjacentHTML('beforeend', html);
        })
    } catch (error) {
        console.error(error);

    }
}

// =========================
// Funções
// =========================

function showModalPermissoes() {
    // Buscar as permissões do colaborador e preencher o modal
    ColaboradorDetail.permissoes.forEach(permissao => {
        const input = document.querySelector(`[value="${permissao.id}"]`);
        if (input) {
            input.checked = true;
        }
    })

    const modalEl = document.querySelector('#modal-permissoes');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
}

function afterSubmit(form, response) {
    showNotification(response.result, response.msg);
    const modalEl = form.closest(".modal");
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.hide();

    loadDadosPrincipais();
    loadPermissoes();
}

async function savePromocao() {
    const url = jsVars.url.promocao.save;
    const formData = new FormData();
    formData.append('csrf_token', jsVars.csrfToken);
    formData.append('colaborador', ColaboradorDetail.dadosPrincipais.id);
    sendAjaxRequest(url, 'POST', formData, async (response) => {
        showNotification(response.result, response.msg);

        if (response.result == 'success') {
            await loadDadosPrincipais();
            loadPromocoes();
        }
    })
}

// =========================
// Inicialização
// =========================

async function initColaboradorDetail() {
    try {
        await loadDadosPrincipais();
        loadPermissoes();
        loadPromocoes();
    } catch (error) {
        console.error(error);
    }
}