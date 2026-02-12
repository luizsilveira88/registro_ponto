// =========================
// Elementos Globais
// =========================

const ColaboradorIndex = {
    datatable: null,
    tomselect: null,
}

// =========================
// Eventos
// =========================

// Inicialização
document.addEventListener('DOMContentLoaded', initColaborador);

// Pesquisar usuarios
document.querySelector('#search-colaborador').addEventListener('keyup', searchColaborador);

// Adicionar colaborador
document.querySelector('.btn-add').addEventListener('click', addColaborador);

// Salvar Colaborador
document.querySelector('#btn-save').addEventListener('click', saveColaborador);

// Pesquisar CNPJ
// document.querySelector('#btn_cnpj').addEventListener('click', searchCNPJ);


// Monitar eventos na tabela de usuarios
document.querySelector('#table_colaborador').addEventListener('click', (event) => {
    // Editar colaborador
    const btnEdit = event.target.closest('.btn-edit');
    if (btnEdit && btnEdit.matches('.btn-edit')) {
        editColaborador(btnEdit);
    }
})

// =========================
// Inicialização
// =========================

async function initColaborador() {
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
    const tableColaboradorEl = $('#table_colaborador');

    if (ColaboradorIndex.datatable) {
        ColaboradorIndex.datatable.ajax.reload();
    } else {
        ColaboradorIndex.datatable = tableColaboradorEl.DataTable({
            dom: 'rtp',
            ordering: false,
            autoWidth: false,
            ajax: {
                url: $('#table_colaborador').data('url'),
                dataSrc: 'data'
            },
            columnDefs: [
                {
                    targets: [0, 1, 2],
                    className: 'text-start'
                },
                {
                    targets: [3],
                    className: 'text-end'
                }
            ],
            columns: [
                {
                    data: 'nome',
                    render: function (row, type, data) {
                        const url = jsVars.url.colaborador.detail.replace('0', data.id);
                        return `<a href="${url}">${data.nome}</a>`;
                    }
                },
                {
                    data: null,
                    render: function (row, type, data) {
                        return formatValue(data.cnpj, 'cnpj');
                    }
                },
                {
                    data: 'get_status_display',
                },
                {
                    render: function (row, type, data) {
                        return renderButtons(data);
                    }
                }
            ],
        });
    }
}

// Carregar relação de grupos econômicos
async function loadGrupoEconomico() {
    const grupoEconomicoEl = document.querySelector('#grupo_economico');

    try {
        const response = await receiveAjaxRequest(jsVars.url.grupoEconomico.findAll);
        if (response.result == 'success') {
            if (ColaboradorIndex.tomselect) {
                // Já existe: limpa e recarrega as opções
                ColaboradorIndex.tomselect.clearOptions();
                response.data.forEach((grupoEconomico) => {
                    ColaboradorIndex.tomselect.addOption({ value: grupoEconomico.id, text: grupoEconomico.nome });
                });
                ColaboradorIndex.tomselect.refreshOptions(false);
                ColaboradorIndex.tomselect.clear(); // <-- limpa seleção
            } else {
                // Primeira vez: popula o <select> e cria Tom Select
                let html = '';
                response.data.forEach((grupoEconomico) => {
                    html += `<option value="${grupoEconomico.id}">${grupoEconomico.nome}</option>`;
                });
                grupoEconomicoEl.insertAdjacentHTML('beforeend', html);

                ColaboradorIndex.tomselect = new TomSelect('#grupo_economico', {
                    create: function (input) {
                        return {
                            value: input,
                            text: `Adicionar "${input}"`
                        };
                    },
                    createOnBlur: true,
                    persist: false,
                    maxItems: 1,
                    plugins: ['remove_button'],
                });

                ColaboradorIndex.tomselect.clear(); // <-- limpa seleção após criação
            }

        } else {
            throw 'Erro ao carregar grupos econômicos';
        }
    } catch (error) {
        console.error('Erro ao carregar grupos econômicos:', error);
    }
}

// Pesquisar produto na tabela de usuarios
function searchColaborador(event) {
    const query = event.target.value;
    const tableColaboradorEl = document.querySelector('#table_colaborador');
    const dataTable = $.fn.DataTable.isDataTable(tableColaboradorEl) ? $(tableColaboradorEl).DataTable() : null;
    if (typeof query !== 'string') {
        showNotification('error', 'A consulta deve ser formada apenas por textos.');
        return;
    }
    dataTable.search(query).draw();
}

// Adicionar colaborador
function addColaborador() {
    const modalEl = document.querySelector('#modal-colaborador');
    let modalInstance = bootstrap.Modal.getOrCreateInstance(modalEl);
    // resetForm();
    modalInstance.show();
}

// Limpar campos dos formulário
function resetForm() {
    document.querySelector('#colaborador_id').value = '';
    document.querySelector('#modal-colaborador form').reset();
}

// Salvar
function saveColaborador() {
    const modalEl = document.querySelector('#modal-colaborador');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    const form = modalEl.querySelector('form');

    if (form.checkValidity()) {
        const formData = new FormData(form);
        formData.append('csrf_token', jsVars.csrfToken);

        // Grupo Econômico
        if (ColaboradorIndex.tomselect) {
            const grupoEconomico = ColaboradorIndex.tomselect.getValue();
            formData.set('grupo_economico', grupoEconomico);
        }

        sendAjaxRequest(jsVars.url.colaborador.save, 'POST', formData, (response) => {
            showNotification(response.result, response.msg);

            if (response.result == 'success') {
                initColaborador();
                modalInstance.hide();
                form.classList.remove('was-validated');
                resetForm();
            }
        })
    } else {
        form.classList.add('was-validated');
    }
}

// Editar
async function editColaborador(btn) {
    try {
        const colaborador_id = btn.dataset.id;

        // Recuperar dados do colaborador
        const url = jsVars.url.colaborador.getById.replace(0, colaborador_id);
        const response = await receiveAjaxRequest(url);

        if (response.result == 'success') {
            const modalEl = document.querySelector('#modal-colaborador');
            let modalInstance = bootstrap.Modal.getOrCreateInstance(modalEl);

            document.querySelector('#colaborador_id').value = response.data.id;
            document.querySelector('#nome').value = response.data.nome;
            document.querySelector('#rede').value = response.data.rede?.id;
            document.querySelector('#cnpj').value = response.data.cnpj;
            document.querySelector('#email').value = response.data.email;
            document.querySelector('#whatsapp').value = response.data.whatsapp;
            document.querySelector('#estado').value = response.data.estado?.id;
            document.querySelector('#observacao').value = response.data.observacao;
            document.querySelector('#tester').checked = response.data.tester;

            // Limpa seleção atual
            ColaboradorIndex.tomselect.clear(true);

            const grupo = response.data.grupo_economico;
            if (grupo) {
                // Verifica se a opção já existe no Tom Select
                if (!ColaboradorIndex.tomselect.options.hasOwnProperty(grupo.id)) {
                    ColaboradorIndex.tomselect.addOption({ value: grupo.id, text: grupo.nome });
                }
                ColaboradorIndex.tomselect.setValue(grupo.id);
            }

            modalInstance.show();
        } else {
            throw 'Erro ao carregar dados';
        }
    } catch (error) {
        console.error('Erro ao editar colaborador:', error);
    }
}

// Buscar CNPJ
async function searchCNPJ() {
    const cnpj = document.querySelector('#cnpj').value;
    const url = jsVars.url.colaborador.getDataByCNPJ.replace(0, cnpj);
    const response = await receiveAjaxRequest(url);

    const nomeEl = document.querySelector('#nome');
    const emailEl = document.querySelector('#email');
    const whatsappEl = document.querySelector('#whatsapp');

    if (response.result == 'success') {
        nomeEl.value = response.data.company?.name || '';
        emailEl.value = response.data.emails?.[0].address || '';
        whatsappEl.value = response.data.phones?.[0]
            ? `${response.data.phones[0].area}${response.data.phones[0].number}`
            : '';
    } else {
        showNotification(response.result, response.msg);
        nomeEl.value = '';
        emailEl.value = '';
        whatsappEl.value = '';
    }
}

// =========================
// Renderização
// =========================

// Renderizar botões
function renderButtons(data) {
    return `
        <div class="btn-group dropdown">
            <button class="btn btn-icon btn-clean me-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fas fa-ellipsis-h"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end" role="menu">
                <li>
                    <button class="btn btnlink dropdown-item btn-edit" data-id="${data.id}">
                        <i class="fas fa-pen me-2"></i>Editar
                    </button>
                </li>
            </ul>
        </div>
    `;
}

