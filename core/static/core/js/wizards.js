//====================================
// Controle de tabs para Wizards
//====================================

// =================================
// Eventos
// =================================

// Monitor quando o botão de próximo com validação é clicado
document
	.querySelectorAll("[data-next-tab-with-validate]")
	.forEach(function (btn) {
		btn.addEventListener("click", nextTabWithValidate);
	});

document.querySelectorAll("[data-previous-tab]").forEach(function (btn) {
	btn.addEventListener("click", previousTab);
});

document.querySelectorAll("[data-next-tab]").forEach(function (btn) {
	btn.addEventListener("click", nextTab);
});

// =================================
// Funções
// =================================

// Avança para a próxima tab se os inputs forem válidos
function nextTabWithValidate(event) {
	const currentPane = event.target.closest(".tab-pane");
	const nextPane = document.querySelector(
		event.target.dataset.nextTabWithValidate
	);
	const nextTab = document.querySelector(`.nav-link[href="#${nextPane.id}"]`);

	if (validateInputs(currentPane) && nextPane) {
		const nextTabBs = new bootstrap.Tab(nextTab);
		nextTabBs.show();
		nextTab.classList.remove("disabled");
	}
}

// Valida os inputs de uma tab
function validateInputs(currentTab) {
	const inputs = currentTab.querySelectorAll("input, select, textarea");

	let isValid = true;

	inputs.forEach((input) => {
		if (!input.checkValidity()) {
			isValid = false;
			input.classList.add("is-invalid");
		} else {
			input.classList.remove("is-invalid");
		}
	});

	return isValid;
}

// Volta para a tab anterior
function previousTab(event) {
	const previousPane = document.querySelector(
		event.target.dataset.previousTab
	);
	const previousTab = document.querySelector(
		`.nav-link[href="#${previousPane.id}"]`
	);

	const previousTabBs = new bootstrap.Tab(previousTab);
	previousTabBs.show();
}

// Avança para a próxima tab
function nextTab(event) {
	const nextPane = document.querySelector(event.target.dataset.nextTab);
	const nextTab = document.querySelector(`.nav-link[href="#${nextPane.id}"]`);

	const nextTabBs = new bootstrap.Tab(nextTab);
	nextTabBs.show();
}

// Reseta as tabs para o estado inicial, desabilitando todas exceto a primeira
function resetTabs(element) {
	element
		.querySelectorAll(".nav-link")
		.forEach((link) => link.classList.add("disabled"));
	const mainTab = element.querySelector(".main-tab");
	mainTab.classList.remove("disabled");
	const mainTabBs = new bootstrap.Tab(mainTab);
	mainTabBs.show();
}
