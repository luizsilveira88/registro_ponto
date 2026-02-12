// ================================
// Eventos
// ================================

// Monitorar o evento de submit do formulário
document.addEventListener("submit", handleFormSubmit);

// ================================
// Funções
// ================================

/**
 * Manipula o evento de submit do formulário
 * @param {Event} event Evento de submit
 * @returns {void}
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;

    if (form.dataset.async) {
        if (form.checkValidity()) {
            let formData = new FormData();

            // Percorrer os campos do formulário tratando os dados, se necessário
            form.querySelectorAll(
                "input:not([type=checkbox]):not([type=radio]), select, textarea",
            ).forEach((input) => {
                const name = input.name;
                if (!name) return; // Pula se o campo não tem nome

                const format = input.dataset.format;

                if (input.tagName === "SELECT" && input.multiple) {
                    // Para campos select[multiple]
                    Array.from(input.selectedOptions).forEach((option) => {
                        formData.append(name, option.value);
                    });
                } else if (format) {
                    switch (format) {
                        case "date":
                            const dateRaw = toDate(input.value);
                            formData.append(name, dateRaw);
                            break;
                        case "datetime":
                            const dateTimeRaw = toDateTime(input.value);
                            formData.append(name, dateTimeRaw);
                            break;
                        default:
                            formData.append(name, input.value);
                    }
                } else {
                    formData.append(name, input.value);
                }
            });

            // Percorrer campos checkbox/radio
            form.querySelectorAll(
                "input[type=checkbox], input[type=radio]",
            ).forEach((checkbox) => {
                const name = checkbox.name;
                if (!name) return;
                if (checkbox.checked) {
                    formData.append(name, checkbox.value);
                }
            });

            const hookBefore = form.dataset.hookBefore;
            if (!hookBefore) {
                if (typeof window.beforeSubmit === "function") {
                    formData = await beforeSubmit(form, formData);
                }
            } else {
                if (typeof window[hookBefore] === "function") {
                    formData = await window[hookBefore](form, formData);
                }
            }

            // Preparar headers para o AJAX
            const ajaxHeaders = {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                Accept: "application/json",
            };

            // Enviar os dados do formulário via AJAX
            fetch(form.action, {
                method: (form.dataset.method ?? form.method).toUpperCase(),
                headers: ajaxHeaders,
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    const hookAfter = form.dataset.hookAfter;
                    if (!hookAfter) {
                        // Executar hook padrão
                        if (typeof window.afterSubmit === "function") {
                            afterSubmit(form, data);
                        }
                    } else {
                        // Executar hook personalizado (hookAfter)
                        if (typeof window[hookAfter] === "function") {
                            window[hookAfter](form, data);
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
