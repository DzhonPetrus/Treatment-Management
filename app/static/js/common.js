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

	$(form)[0].reset();
	showAllFields();
	setHiddenFields();
};

const showModal = () => $(modal).modal("show");
const hideModal = () => $(modal).modal("hide");
const setInputValue = (data) =>{
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
	$("#detailed_result_placeholder").hide();
};

const setState = (state, data) => {


	$("#photo_url_placeholder").attr("src", `${BASE_URL}static/upload/${data.photo_url}`);
	$("#detailed_result_placeholder").hide();
	if(data.detailed_result !== undefined){
		$("#detailed_result_placeholder").attr("href", `${BASE_URL}static/upload/${data.detailed_result}`);
		$("#detailed_result_placeholder").show();
	}

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