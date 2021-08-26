const BASE_URL = `httpp:/127.0.0.1:8000/`;
//EXTRA
formReset = (form) => {
	$("html", "body").animate({ scrollTop: 0 }, "slow");

	$(form)[0].reset();
	showAllFields();
	setHiddenFields();
};
const showModal = (modal) => $(form).modal("show");

const setInputValue = (fields, data) =>
	fields.forEach((field) => $(`#${field}`).val(data.data[field]));

const setFieldsReadOnly = (fields, bool) =>
	fields.forEach((field) => $(`#${field}`).prop("disabled", bool));
const setReadOnlyFields = (readOnlyFields) =>
	readOnlyFields.forEach((field) => $(`#${field}`).prop("disabled", true));

const showAllFields = (fields) =>
	fields.forEach((field) => $(`#group-${field}`).show());
const setHiddenFields = (fieldsHidden) =>
	fieldsHidden.forEach((field) => $(`#group-${field}`).hide());

const newHandler = () => {
	formReset();
	setFieldsReadOnly(false);
	setReadOnlyFields();
};

const renderButtons = (aData) => {
	let buttons =
		"" +
		`<button type="button" onClick="return viewData('${aData["id"]}')" class="btn btn-info"><i class="fa fa-eye"></i></button> ` +
		`<button type="button" onClick="return editData('${aData["id"]}')" class="btn btn-success"><i class="fa fa-pencil-alt"></i></button> ` +
		`<button type="button" onClick="return deleteData('${aData["id"]}')" class="btn btn-danger"><i class="fa fa-trash"></i></button>`;
	return buttons;
};

const setState = (state, data, readOnlyFields, modal) => {
	showAllFields();
	setInputValue(data);
	$("#group-btnAdd").hide();

	if (state === "view") {
		setFieldsReadOnly(readOnlyFields, true);
		$("#group-btnUpdate").hide();
	}

	if (state === "edit") {
		setFieldsReadOnly(readOnlyFields, false);
		setReadOnlyFields();

		$("#group-btnUpdate").show();
	}

	showModal(modal);
};