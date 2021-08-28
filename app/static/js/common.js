const BASE_URL = `http://127.0.0.1:8000/`;

const notification = (type, title, message)=> {
    return toastr[type](message,title);
};

// let token = localStorage.getItem("TOKEN");
// Append headers to Ajax attributes
// $.ajaxSetup(
//     {
//         headers:
//         {
//             Accept: "application/json",
//             Authorization: "Bearer " + token,
//         },
//     });

// trim input fields except file, select, textarea
trimInputFields = () => 
{
    var allInputs = $("input:not(:file())");
    allInputs.each(function () 
    {
        $(this).val($.trim($(this).val()));
    });
};

// FOR PICTURE
readURL = (input) => {
	var url = input.value;
	var ext = url.substring(url.lastIndexOf(".") + 1).toLowerCase();
	if (
		input.files &&
		input.files[0] &&
		(ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")
	) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$("#photo_url_placeholder").attr("src", e.target.result);
		};

		reader.readAsDataURL(input.files[0]);
	} else {
		//$("#img").attr("src", "/assets/no_preview.png");
	}
};


// FOR MODAL FORM

formReset = () => {
	$("html", "body").animate({ scrollTop: 0 }, "slow");

	$(form)[0].reset();
	showAllFields();
	setHiddenFields();
};

const showModal = () => $(modal).modal("show");
const setInputValue = (data) =>{
console.log(data);
	fields.forEach((field) => $(`#${field}`).val(data[field]));

}
const setFieldsReadOnly = (bool) =>
	fields.forEach((field) => $(`#${field}`).prop("disabled", bool));
const setReadOnlyFields = () =>
	readOnlyFields.forEach((field) => $(`#${field}`).prop("disabled", true));

const showAllFields = () =>
	fields.forEach((field) => $(`#group-${field}`).show());
const setHiddenFields = () =>
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

const setState = (state, data) => {
	console.log(state)
	showAllFields();
	setInputValue(data);
	$("#group-btnAdd").hide();

	if (state === "view") {
		setFieldsReadOnly(true);
		$("#group-btnUpdate").hide();
	}

	if (state === "edit") {
		setFieldsReadOnly(false);
		setReadOnlyFields();

		$("#group-btnUpdate").show();
	}

	showModal();

};