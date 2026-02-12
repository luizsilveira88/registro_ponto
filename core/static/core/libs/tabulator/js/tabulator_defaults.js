// Traduções
const tabulatorLangs = {
	"pt-br": {
		columns: {
			name: "Nome",
		},
		data: {
			loading: "Carregando",
			error: "Erro",
		},
		groups: {
			item: "item",
			items: "itens",
		},
		pagination: {
			page_size: "Tamanho da página",
			page_title: "Show Page",
			first: "Primeira",
			first_title: "Primeira Página",
			last: "Última",
			last_title: "Última Página",
			prev: "Anterior",
			prev_title: "Página Anterior",
			next: "Próxima",
			next_title: "Próxima Página",
			all: "Todos",
			counter: {
				showing: "Exibindo",
				of: "de",
				rows: "linhas",
				pages: "páginas",
			},
		},
		headerFilters: {
			default: "filtrar coluna...",
			columns: {
				name: "filtrar nome...",
			},
		},
	},
};

// Configurações padrão de linguagem
Tabulator.defaultOptions.locale = "pt-br";
Tabulator.defaultOptions.langs = tabulatorLangs;

// Headers para JSON
Tabulator.defaultOptions.headers = {
	Accept: "application/json",
};

// Outros padrões
Tabulator.defaultOptions.layout = "fitColumns";
Tabulator.defaultOptions.placeholder = "Nenhum registro encontrado";
Tabulator.defaultOptions.ajaxConfig = "GET";
Tabulator.defaultOptions.pagination = true;
Tabulator.defaultOptions.paginationMode = "remote";
Tabulator.defaultOptions.paginationSize = 10;
Tabulator.defaultOptions.sortMode = "remote";
Tabulator.defaultOptions.filterMode = "remote";
Tabulator.defaultOptions.responsiveLayout = true;
Tabulator.defaultOptions.paginationSizeSelector = [10, 25, 50, 100, true];
Tabulator.defaultOptions.columnDefaults = {
	vertAlign: "middle",
};

// Pesquisar
const searchInputs = document.querySelectorAll(".tabulator-search");
searchInputs.forEach((searchInput) => {
	let searchTimeout = null;
	const table = document.querySelector(`${searchInput.dataset.target}`);

	if (!table) {
		return;
	}

	searchInput.addEventListener("input", (e) => {
		clearTimeout(searchTimeout);

		searchTimeout = setTimeout(() => {
			const value = e.target.value;

			if (value) {
				table._tabulator.setFilter([
					{ field: "_global", type: "like", value },
				]);
			} else {
				table._tabulator.clearFilter();
			}
		}, 300);
	});
});
