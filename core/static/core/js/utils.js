/**
 * Mostra uma notificação para o usuário com base na resposta recebida de uma
 * requisição AJAX.
 *
 * @param {string} result - O resultado da requisição AJAX ("success", "error", "warning", "info").
 * @param {string} message - A mensagem a ser exibida na notificação.
 * @returns {void}
 */
function showNotification(result, message) {
    if (!window.notyf) {
        console.error("Notyf não inicializado");
        return;
    }

    switch (result) {
        case "success":
            notyf.success(message);
            break;

        case "error":
            notyf.error(message);
            break;

        case "warning":
            notyf.open({
                type: "warning",
                message: message,
            });
            break;

        case "info":
            notyf.open({
                type: "info",
                message: message,
            });
            break;

        default:
            notyf.success(message);
    }
}

/**
 * Converte uma string formatada como número em um número real.
 * 
 * Se a string fornecida estiver vazia ou não puder ser convertida em um número,
 * retorna 0. Esta função remove pontos e substitui vírgulas por pontos antes de 
 * fazer a conversão.
 *
 * @param {string} value - A string que representa o número formatado.
 * @returns {number} O número convertido ou 0 se a conversão não for possível.
 */

function toNumber(value) {
    if (!value) return 0;
    let number = Number(value.replace(/\./g, '').replace(/\,/g, '.'));
    if (isNaN(number)) return 0;
    return number;
}


/**
 * Converte uma string formatada como "dd/mm/yyyy" em um objeto Date ou
 * retorna uma string vazia se a data não for válida.
 *
 * @param {string} value - A string formatada como "dd/mm/yyyy".
 * @returns {string} A data em formato ISO "yyyy-mm-dd" ou uma string vazia.
 */
function toDate(value) {
    if (!value) return '';
    const [day, month, year] = value.split('/').map(Number);
    if (day > 0 && month > 0 && year > 0) {
        const date = new Date(year, month - 1, day);
        if (!isNaN(date)) {
            return date.toISOString().split('T')[0];
        } else {
            return '';
        }
    }
}

/**
 * Formata um valor de acordo com o tipo informado.
 * 
 * O tipo pode ser: 'currency', 'm2', 'number', 'percent', 'percent2', 'datetime' ou 'date'.
 * Se o tipo for 'currency', o valor é formatado como moeda brasileira com o número de casas decimais informadas.
 * Se o tipo for 'm2', o valor é formatado como número com o número de casas decimais informadas e seguido de 'm²'.
 * Se o tipo for 'number', o valor é formatado como número com o número de casas decimais informadas.
 * Se o tipo for 'percent', o valor é formatado como porcentagem com o número de casas decimais padrão.
 * Se o tipo for 'percent2', o valor é formatado como porcentagem com o número de casas decimais informadas.
 * Se o tipo for 'datetime', o valor é formatado como data e hora no formato brasileiro.
 * Se o tipo for 'date', o valor é formatado como data no formato brasileiro.
 * 
 * Se o tipo for nulo ou vazio, o valor é retornado sem formatação.
 * 
 * @param {string|number} value - O valor a ser formatado.
 * @param {string} type - O tipo de formatação.
 * @param {number} decimalPlaces - O número de casas decimais a serem formatadas.
 * @returns {string} O valor formatado.
 */
function formatValue(value, type, decimalPlaces = 2) {
    let formattedValue = value;

    if (type) {
        switch (type) {
            case 'currency':
                formattedValue = Number(value) || 0;
                formattedValue = formattedValue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: decimalPlaces });
                break;
            case 'm2':
                formattedValue = Number(value) || 0;
                formattedValue = formattedValue.toLocaleString('pt-BR', { minimumFractionDigits: decimalPlaces });
                formattedValue = `${formattedValue} m²`
                break;
            case 'number':
                formattedValue = Number(value) || 0;
                formattedValue = formattedValue.toLocaleString('pt-BR', { minimumFractionDigits: decimalPlaces });
                break;
            case 'percent':
                formattedValue = Number(value) || 0;
                formattedValue = formattedValue.toLocaleString('pt-BR', { style: 'percent' });
                break;
            case 'percent2':
                formattedValue = Number(value) || 0;
                formattedValue = formattedValue.toLocaleString('pt-BR', { style: 'percent', minimumFractionDigits: decimalPlaces });
                break;
            case 'datetime':
                const date = new Date(value);
                if (!isNaN(date.getTime())) {
                    formattedValue = date.toLocaleString('pt-br');
                }
                break;
            case 'date':
                if (!value) return '';
                const [year, month, day] = value.split('-').map(Number);
                if (day > 0 && month > 0 && year > 0) {
                    const date = new Date(year, month - 1, day);

                    if (!isNaN(date.getTime())) {
                        formattedValue = date.toLocaleDateString('pt-br')
                    }

                }
                break;
            case 'cnpj':
                if (!value.length === 14) return '';
                formattedValue = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5");
                break;
        }

        return formattedValue;
    }
}

/**
 * Compara dois valores, ignorando acentos.
 * 
 * Essa função remove acentos de uma string, normaliza a string
 * com o formato NFD e converte a string para minúscula.
 * 
 * @param {string} a - O primeiro valor a ser comparado.
 * @param {string} b - O segundo valor a ser comparado.
 * @returns {boolean} true se os valores forem iguais, false caso contrário.
 */
function compareIgnoringAccents(a, b) {
    const normalize = str =>
        str
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();

    return normalize(a) === normalize(b);
}