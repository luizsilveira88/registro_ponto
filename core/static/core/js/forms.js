// ================================
// Eventos
// ================================

// Monitorar o evento de submit do formulário
document.addEventListener("submit", handleFormSubmit);

// Botão de busca de CNPJ
const btnBuscarCnpj = document.querySelectorAll(".btn-search-cnpj").forEach(btn => {
    btn.addEventListener("click", searchCnpj);
});

// ================================
// Funções
// ================================

/**
 * Manipula o evento de submit do formulário
 * @param {Event} event Evento de submit
 * @returns {void}
 */
function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    let formData = "";

    if (form.dataset.async) {
        if (form.checkValidity()) {
            const formDataRaw = new FormData();

            // Percorrer os campos do formulário tratando os dados, se necessário
            form.querySelectorAll(
                "input:not([type=checkbox]):not([type=radio]), select, textarea"
            ).forEach((input) => {
                const name = input.name;
                if (!name) return; // Pula se o campo não tem nome

                const format = input.dataset.format;

                if (input.tagName === "SELECT" && input.multiple) {
                    // Para campos select[multiple]
                    Array.from(input.selectedOptions).forEach((option) => {
                        formDataRaw.append(name, option.value);
                    });
                } else if (format) {
                    switch (format) {
                        case "date":
                            const dateRaw = toDate(input.value);
                            formDataRaw.append(name, dateRaw);
                            break;
                        case "datetime":
                            const dateTimeRaw = toDateTime(input.value);
                            formDataRaw.append(name, dateTimeRaw);
                            break;
                        default:
                            formDataRaw.append(name, input.value);
                    }
                } else {
                    formDataRaw.append(name, input.value);
                }
            });

            // Percorrer campos checkbox/radio
            form.querySelectorAll(
                "input[type=checkbox], input[type=radio]"
            ).forEach((checkbox) => {
                const name = checkbox.name;
                if (!name) return;
                if (checkbox.checked) {
                    formDataRaw.append(name, checkbox.value);
                }
            });

            if (typeof window.beforeSubmit === "function") {
                formData = beforeSubmit(form, formDataRaw);
            } else {
                formData = formDataRaw;
            }

            // Enviar os dados do formulário via AJAX
            fetch(form.action, {
                method: (form.dataset.method ?? form.method).toUpperCase(),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    const callback = form.dataset.callback;
                    if (!callback) {
                        // Executar hook padrão
                        if (typeof window.afterSubmit === "function") {
                            afterSubmit(form, data);
                        }
                    } else {
                        // Executar hook personalizado (callback)
                        if (typeof window[callback] === "function") {
                            window[callback](form, data);
                        }
                    }
                })
                .catch((error) => {
                    console.error("Erro:", error);
                });
        } else {
            form.classList.add("was-validated");
        }
    } else {
        form.submit();
    }
}


/**
 * Popula o formulário com os dados obtidos da URL
 * @param {string} url - A URL da qual buscar os dados para popular o formulário.
 * @param {HTMLElement} form - O elemento do formulário a ser populado.
 * @param {string} prefix - O prefixo a ser usado para buscar os campos do formulário.
 */
function populateForm(url, form, prefix) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            Object.entries(data.data).forEach(([key, value]) => {
                const fields = form.querySelectorAll(`#${prefix}_${key}`);
                for (const field of fields) {
                    if (!field) continue;

                    if (value === true || value === false) {
                        field.checked = value;
                    } else {
                        field.value = value ?? '';
                    }
                }
            });
        })
}

async function searchCnpj(event) {
    const button = event.currentTarget;
    const input = button.previousElementSibling;
    const cnpj = input.value.replace(/\D/g, '');

    const url = button.dataset.url;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ cnpj }),
    });
    const json = await response.json();

    const data = json.result == 'success' ? json.data : null;

    // Chamar o hook
    if (typeof window.afterGetCnpj === "function") {
        afterGetCnpj(data, event);
    }
}

function selectByTextContains(element, text) {
    for (const option of element.options) {
        if (compareIgnoringAccents(option.textContent.toLowerCase(), text.toLowerCase())) {
            option.selected = true;
            break;
        }
    }
}

/**
 * Retorna o valor de um cookie com o nome especificado.
 *
 * @param {string} name - O nome do cookie a ser buscado.
 * @returns {string|null} O valor do cookie, ou null se o cookie não for encontrado.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
