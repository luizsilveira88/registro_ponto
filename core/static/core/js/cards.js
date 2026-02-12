//====================================
// Popular cards assincronamente
//====================================

/**
 * Popula o card com os dados obtidos da URL, buscando os elementos HTML com identificador de prefixo "display_"
 * @param {string} url - A URL da qual buscar os dados para popular o card.
 * @param {HTMLElement} cardElement - O elemento do card a ser populado. 
 * @returns {Promise<object>} - Retorna uma Promise que resolve para os dados obtidos da URL.
 */
async function populateCard(url, cardElement) {
    const response = await fetch(url);
    const data = await response.json();

    for (const [key, value] of Object.entries(data.data)) {
        const fields = cardElement.querySelectorAll(`.display_${key}`);

        for (const field of fields) {
            if (!field) continue;

            if (value === true || value === false) {
                field.innerHTML = value
                    ? '<i class="fa fa-check text-success me-2"></i>Sim'
                    : '<i class="fa fa-times text-danger me-2"></i>Não';
            } else {
                field.textContent = value ?? '';
            }
        }
    }

    return data;
}