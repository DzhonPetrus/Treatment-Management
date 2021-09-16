	window.endpoint = (window.user_type).toLowerCase() + '/' + 'user'

	window.modal = "#modal-user";
	window.dataTable = "#dataTable";

	window.account_fields = ["account_id", "email", "password", "user_profile_id", "user_type", "account_is_active", "btnAdd", "btnUpdate"];
	window.account_fieldsHidden = ["account_id", "btnUpdate", "account_is_active", "user_profile_id"];
	window.account_readOnlyFields = ["account_id", "account_is_active", "user_profile_id"];

	window.info_fields = ["info_id", "position", "first_name", "middle_name", "last_name", "suffix_name", "birth_date", "department", "info_is_active", "btnAdd", "btnUpdate", "file"];
	window.info_fieldsHidden = ["info_id", "btnUpdate", "info_is_active"];
	window.info_readOnlyFields = ["info_id", "info_is_active"];

$(function () {

	loadForms()

	$('#accountForm').on("submit", function (e) {
		e.preventDefault();
		trimInputFields();

		if ($('#accountForm').validate()) {
			var form_data = new FormData(this);

			form_data.append('account_id', $("#account_id").val())
			form_data.append('user_profile_id', $("#user_profile_id").val())
			form_data.append('account_is_active', $("#account_is_active").val())

			var id = $("#id").val();
			$.ajax({
				url: BASE_URL + `admin/user/${id}`,
				type: "PUT",
				data: form_data,
				dataType: "JSON",
				contentType: false,
				processData: false,
				cache: false,
				success: function (data) {
					if (data.error == false) {
						loadForms();
						notification("success", "Success!", data.message);
					} else {
						notification("error", "Error!", data.message);
					}
				},
				error: (data) => notification("error", data.responseJSON.detail),
			});
		}
	});

	$('#infoForm').on("submit", function (e) {
		e.preventDefault();
		trimInputFields();

		if ($('#infoForm').validate()) {
			var form_data = new FormData(this);

			form_data.append('info_id', $("#info_id").val())
			form_data.append('user_profile_id', $("#user_profile_id").val())
			form_data.append('info_is_active', $("#info_is_active").val())

			var id = $("#id").val();
			$.ajax({
				url: BASE_URL + `admin/profile/${id}`,
				type: "PUT",
				data: form_data,
				dataType: "JSON",
				contentType: false,
				processData: false,
				cache: false,
				success: function (data) {
					if (data.error == false) {
						loadForms();
						notification("success", "Success!", data.message);
					} else {
						notification("error", "Error!", data.message);
					}
				},
				error: (data) => notification("error", data.responseJSON.detail),
			});
		}
	});
});

loadForms = () => {
	$.ajaxSetup({
		headers: {
			Accept: "application/json",
			Authorization: "Bearer " + token,
			ContentType: "application/x-www-form-urlencoded",
		},
	});
	$.ajax({
		url: BASE_URL + `admin/user/${user_id}`,
		type: "GET",
		dataType: "json",

		success: data => {
			(data.error == false) ? setAccountState(data.data) : notification("error", "Error!", data.message)
		},
		error: (data) => notification("error", data.responseJSON.detail),
	});
	$.ajax({
		url: BASE_URL + `admin/profile/${user_profile.id}`,
		type: "GET",
		dataType: "json",
		success: data => {
			(data.error == false) ? setInfoState(data.data) : notification("error", "Error!", data.message)
		},
		error: (data) => notification("error", data.responseJSON.detail),
	});
};

const setInfoState = data => {
	// setUserProfile(data);
	console.log(data)
	data.info_id = data.id;
	data.info_is_active = data.is_active;

	$("#photo_url_placeholder").attr("src", `${BASE_URL}static/upload/${data.photo_url}`);

	info_fields.forEach((field) => $(`#${field}`).val(data[field]));
	info_fields.forEach((field) => $(`#group-${field}`).show());
	info_fields.forEach((field) => $(`#${field}`).prop("disabled", true));
	// info_readOnlyFields.forEach((field) => $(`#${field}`).prop("disabled", true));

}

const setAccountState = data => {
	console.log(data)
	data.account_id = data.id;
	data.account_is_active = data.is_active;

	account_fields.forEach((field) => $(`#${field}`).val(data[field]));
	account_fields.forEach((field) => $(`#group-${field}`).show());
	account_fields.forEach((field) => $(`#${field}`).prop("disabled", true));
	// account_readOnlyFields.forEach((field) => $(`#${field}`).prop("disabled", true));
}