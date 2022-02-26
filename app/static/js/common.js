const formatDateTime = dt => moment(dt).format(`MMMM D, YYYY hh:mm:ss`);
const formatDate = d => moment(d).format(`MMMM D, YYYY`);

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

	$("#photo_url_placeholder").attr("src", `https://i.stack.imgur.com/y9DpT.jpg`);
	$("#detailed_result_placeholder").attr("href", `#`);
	$(form)[0].reset();
	showAllFields();
	setHiddenFields();
};

const showModal = () => $(modal).modal("show");
const hideModal = () => $(modal).modal("hide");
const setInputValue = (data) =>{
	if(Object.keys(data).includes('lab_request')){
		data.lab_request_no = data.lab_request.lab_request_no;
		if(!fields.includes('lab_request_no'))
			fields.push('lab_request_no');
	}
	if(Object.keys(data).includes('lab_test')){
		data.lab_test_name = data.lab_test.name;
		if(!fields.includes('lab_test_name'))
			fields.push('lab_test_name');
	}
	if(Object.keys(data).includes('treatment_type')){
		data.treatment_type_name = data.treatment_type.name;
		if(!fields.includes('treatment_type_name'))
			fields.push('treatment_type_name');
	}
	if(Object.keys(data).includes('physician')){
		data.physician_name = `${data.physician.user_profile.last_name}, ${data.physician.user_profile.first_name} ${data.physician.user_profile.middle_name || ''} ${data.physician.user_profile.suffix_name ? ', ' + data.physician.user_profile.suffix_name : ''}`
		if(!fields.includes('physician_name'))
			fields.push('physician_name');
	}
	if(fields.includes('last_name') && fields.includes('first_name')){
		data.full_name = `${data.last_name}, ${data.first_name} ${data.middle_name || ''} ${data.suffix_name ? ', ' + data.suffix_name : ''}`
		if(!fields.includes('full_name'))
			fields.push('full_name');
	}
	fields.forEach((field) => {
		$(`#${field}`).val(data[field]);
		$(`#${field}View`).html(data[field]);
	});
}
const setFieldsPlainText = (bool) => {
	fields.forEach((field) => $(`#${field}`).toggleClass("form-control-plaintext", bool));
	fields.forEach((field) => $(`#${field}`).toggleClass("form-control", !bool));
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
	setFieldsPlainText(false);
	setFieldsReadOnly(false);
	setReadOnlyFields();
	$("#detailed_result_placeholder").hide();
};

const setState = (state, data) => {

	$("#photo_url_placeholder").attr("src", `${BASE_URL}static/upload/${data.photo_url}`);
	$("#detailed_result_placeholder").hide();
	if(data.detailed_result !== undefined){
		$("#detailed_result_placeholder").attr("href", `${BASE_URL}static/upload/${data.detailed_result}`);
		$("#detailed_result_placeholder").show();
	}

	if(Object.keys(data).includes('outpatient')){
		if(patient_fields !== undefined){
			window.temp_fields = window.fields
			window.fields = window.patient_fields
		}
		if(data.outpatient != null){
			setInputValue(data.outpatient);
			let age = Math.floor(moment().diff(data.outpatient.birth_date, 'years', true));
			$('#ageView').html(age);
		}
		window.fields = window.temp_fields
	}
	if(Object.keys(data).includes('inpatient')){
		if(patient_fields !== undefined){
			window.temp_fields = window.fields
			window.fields = window.patient_fields
		}
		if(data.inpatient != null){
			setInputValue(data.inpatient);
			let age = Math.floor(moment().diff(data.inpatient.birth_date, 'years', true));
			$('#ageView').html(age);

		}
		window.fields = window.temp_fields
	}
	// TODO: REFACTOR

	showAllFields();
	setInputValue(data);

	$("#group-btnAdd").hide();

	if (state === "view") {
		setFieldsPlainText(true);
		setFieldsReadOnly(true);
		$("#group-btnUpdate").hide();
	}

	if (state === "edit") {
		setFieldsPlainText(false);
		setFieldsReadOnly(false);
		setReadOnlyFields();

		$("#group-btnUpdate").show();
	}

	showModal();

};

const renderButtons = (aData, title, additionalButtons = '') => {
	let buttons =
		`
		<div class="text-center dropdown">
      <div class="btn btn-sm btn-default" data-toggle="dropdown" role="button">
        <i class="fas fa-ellipsis-v"></i>
      </div>

	<div class="dropdown-menu dropdown-menu-right">

        <div class="dropdown-item d-flex" role="button" onClick="return viewData('${aData.id}')">
			<div style="width:2rem">
				<i class="fa fa-eye"> </i>
			</div>
			<div>View ${title}</div>
		</div>

        <div class="dropdown-item d-flex" role="button" onClick="return editData('${aData.id}')">
			<div style="width:2rem">
				<i class="fa fa-edit"> </i>
			</div>
			<div>Edit ${title}</div>
		</div>
		`;
		buttons += aData.is_active == "ACTIVE" 
			? `
				<div 
					class="dropdown-item d-flex" 
					role="button" 
					onClick="return deleteData('${aData.id}')
				">
					<div style="width:2rem">
						<i class="fa fa-trash-alt"> </i>
					</div>
					<div>Delete ${title}</div>
				</div>
			` : `
				<div 
					class="dropdown-item d-flex" 
					role="button" 
					onClick="return reactivateData('${aData.id}')
				">
					<div style="width:2rem">
						<i class="fa fa-redo-alt"> </i>
					</div>
					<div>Re-Activate ${title}</div>
				</div>
			`;
	buttons += additionalButtons !== '' ? `<div class="dropdown-divider"></div>` : '';
	buttons += additionalButtons;
    buttons += '</div>';
	return buttons;
};

function confirmationModal(type, id='') {
	var headIcon = 'fa-exclamation-triangle', headText = 'Confirmation', message, btnColor, btnText, btnIcon = 'fa-check';
	switch(type) {
		case 'create':
			message = 'Are you sure you want to submit it now?';
			btnColor = 'btn-primary ';
			btnText = "Yes, submit it!";
			break;

		case 'update':
			message = 'Are you sure you want to update your request now?';
			btnColor = 'btn-info ';
			btnText = "Yes, update it!";
			break;

		case 'delete':
			message = 'Are you sure you want to delete it now?';
			btnColor = 'btn-danger ';
			btnText = "Yes, delete it!";
			break;

		case 'cancel':
			message = 'Are you sure you want to cancel it now?';
			btnColor = 'btn-danger ';
			btnText = "Yes, cancel it!";
			break;

		case 'reactivate':
			message = 'Are you sure you want to re-activate it now?';
			btnColor = 'btn-info ';
			btnText = "Yes, re-activate it!";
			break;

		case 'logout':
			headIcon = 'fa-sign-out-alt';
			headText = 'Log out';
			message = 'Are you sure you want to log out now?';
			btnColor = 'btn-danger ';
			btnText = "Yes, log out now!";
			btnIcon = 'fa-sign-out-alt';
			break;
	}
	let modal = `
        <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="confirmModal" aria-hidden="true">
          <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
              <div class="modal-content">
                  <div class="modal-header">
				  <div class="modal-title">
					<i class="fa ${headIcon}"></i>
                      ${headText}
				  </div>
                  </div>
                  <div class="modal-body">
                      ${message}
                  </div>
      
                  <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                      <a href="#" 
					  	id="submit" 
						class="btn ${btnColor}"
						${(id !== '' && (type === 'delete' ||type === 'reactivate' || type === 'cancel')) 
							? `onClick="${type}Data('${id}', ${true})"` 
							: ""}
						${(type === 'logout') ? `onclick="location.replace('${BASE_URL}login')"` : ''}
					  >

						${btnText}
						<i class="fa ${btnIcon}"></i>
					  </a>
                  </div>
              </div>
          </div>
      </div>
	`;
	$('#confirmationModal').html(modal);
	$('#confirmModal').modal("show");
}

const logout = () => confirmationModal('logout');

$("#sidebar_picture").attr("src", user_profile.photo_url !== null ? `${BASE_URL}static/upload/${user_profile.photo_url}` : '');
$("#sidebar_full_name").html(`
	${user_profile.first_name} ${user_profile.middle_name || ''} ${user_profile.last_name} ${user_profile.suffix_name || ''}
`);
$("#sidebar_user_type").html(user_type);
$("#sidebar_user_department").html(user_profile?.department);


window.patient_fields = ["id", "type", "first_name", "middle_name", "last_name", "suffix_name", "birth_date", "gender", "contact_no", "email", "blood_type", "is_active", "btnAdd", "btnUpdate"];
    

window.arrToOptions = (arr) => {
	options = ``;
	arr.forEach(v => options+=`<option value=${v}>${v}</option>`);
	return options
}