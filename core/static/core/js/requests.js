/**
 * Envia uma requisição AJAX com o formulário especificado.
 * 
 * @param {string} url URL para a qual enviar a requisição.
 * @param {string} method Método da requisição (GET, POST, PUT, DELETE, etc.).
 * @param {FormData} formData FormData com os dados do formulário.
 * @param {function} callback Função callback que receberá a resposta da requisição em formato JSON.
 */
async function sendAjaxRequest(url, method, formData, callback) {
    return fetch(url, {
        method: method,
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrf_token')
        }
    })
        .then(async (response) => {
            let data;

            try {
                data = await response.json();
            } catch (e) {
                data = {
                    result: 'error',
                    msg: 'Resposta não é um JSON válido',
                    raw: await response.text()
                };
            }

            if (!response.ok) {
                return {
                    result: 'error',
                    msg: `Erro HTTP: ${response.status} ${response.statusText}`,
                    ...data
                };
            }

            return data;
        })
        .then((data) => {
            if (callback) callback(data);
            return data;
        })
        .catch((error) => {
            const errData = {
                result: 'error',
                msg: 'Erro inesperado ao processar a requisição',
                error: error.message || error
            };
            if (callback) callback(errData);
            return errData;
        });
}


/**
 * Envia uma requisição AJAX GET para a URL especificada e retorna a resposta em formato JSON.
 * Caso a resposta seja inválida, lança um erro com a mensagem do status HTTP.
 * Caso um erro ocorra durante a requisição, retorna um array vazio e escreve o erro no console.
 * 
 * @param {string} url URL para a qual enviar a requisição.
 * @returns {Promise<Array<any>>} Uma promessa que retorna um array com a resposta em formato JSON.
 */
async function receiveAjaxRequest(url) {
    try {
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            return {
                result: 'error',
                msg: `Erro HTTP: ${response.status} ${response.statusText}`
            };
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('receiveAjaxRequest:', error);

        return {
            result: 'error',
            msg: 'Erro inesperado ao processar a resposta',
            error: error.message || error
        };
    }
}
