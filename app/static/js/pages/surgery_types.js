	window.endpoint = 'surgery_type'
	window.token = "TEMPORARY"

	window.form = "#form"
	window.modal = "#modal-surgery_type";
	window.dataTable = "#dataTable";

	window.fields = ["id", "name", "description", "price", "status", "btnAdd", "btnUpdate"];
	window.fieldsHidden = ["id", "btnUpdate", "status"];
	window.readOnlyFields = ["id"];

$(function () {

	formReset();
	loadTable();

	// function to save/update record
	$(form).on("submit", function (e) {
		e.preventDefault();
		trimInputFields();

		if ($(form).parsley().validate()) {
			var form_data = new FormData(this);

			var id = $("#id").val();
			if (id == "") {

				// add record
				$.ajax({
					url: BASE_URL + endpoint,
					type: "POST",
					data: form_data,
					dataType: "JSON",
					contentType: false,
					processData: false,
					cache: false,
					success: function (data) {
						if (data.error == false) {
							loadTable();
							notification("success", "Success!", data.message);
							$(form).reset();
						} else {
							notification("error", "Error!", data.message);
						}
					},
					error: function (data) {
						notification("error", data.responseJSON.message);
							console.log('error in add')
				},
				});
			} else {
				$.ajax({
					url: BASE_URL + `${endpoint}/${id}`,
					type: "PUT",
					data: form_data,
					dataType: "JSON",
					contentType: false,
					processData: false,
					cache: false,
					success: function (data) {
						if (data.error == false) {
							loadTable();
							notification("success", "Success!", data.message);
						} else {
							notification("error", "Error!", data.message);
						}
					},
					error: function (data) {
						notification("error", data.responseJSON.message);
				},
				});
			}
		}
	});
});

loadTable = () => {
	$.ajaxSetup({
		headers: {
			Accept: "application/json",
			Authorization: "Bearer " + token,
			ContentType: "application/x-www-form-urlencoded",
		},
	});
	$(dataTable).dataTable().fnClearTable();
	$(dataTable).dataTable().fnDestroy();
	$(dataTable).dataTable({
		responsive: true,
		serverSide: false,
		stateSave:true,
		order: [[0, "desc"]],
		aLengthMenu: [5, 10, 20, 30, 50, 100],
		aoColumns: [
			{ sClass: "text-left" },
			{ sClass: "text-left" },
			{ sClass: "text-left" },
			{ sClass: "text-left" },
			{ sClass: "text-center" },
		],
		columns: [
			{
				data: "name",
				name: "name",
				searchable: true,
			},
			{
				data: "description",
				name: "description",
				searchable: true,
			},
			{
				data: "price",
				name: "price",
				searchable: true,
			},
			{
				data: "status",
				render: (aData) => aData.toUpperCase() == "ACTIVE" ? `<span class="p-2 w-100 badge badge-primary">${aData}</span>` : `<span class="p-2 w-100 badge badge-danger">${aData}</span>`,
				// name: "status",
				// searchable: true,
			},
			{
				data: null,
				render: (aData) => renderButtons(aData, "Surgery Type"),
			},
		],
		ajax: {
			url: BASE_URL + `${endpoint}/all`,
			type: "GET",
			ContentType: "application/x-www-form-urlencoded",
		},
		drawCallback: function (settings) {
			// POPULATE ANALYTIC CARDS
			let surgery_types = settings.json;
			if(surgery_types !== undefined){
				console.log(surgery_types)
				const active_surgery_types = surgery_types.data.filter(types => types.status === 'ACTIVE')
				const inactive_surgery_types = surgery_types.data.filter(types => types.status === 'INACTIVE')

				$('#totalTypes').html(surgery_types.data.length)
				$('#totalTypesActive').html(active_surgery_types.length)
				$('#totalTypesInactive').html(inactive_surgery_types.length)
			}
		},
	});
};

// VIEW DATA
viewData = (id) => {
	{
		$.ajax({
			url: BASE_URL + `${endpoint}/${id}`,
			type: "GET",
			dataType: "json",

			success: data => (data.error == false) ? setState("view", data.data) : notification("error", "Error!", data.message),
			error: ({ responseJSON }) => console.error(responseJSON),
		});
	}
};

// Edit DATA
editData = (id) => {
	{
		$.ajax({
			url: BASE_URL + `${endpoint}/${id}`,
			type: "GET",
			data: { id },
			dataType: "json",

			success: data => (data.error == false) ? setState("edit", data.data) : notification("error", "Error!", data.message),
			error: function ({ responseJSON }) {},
		});
	}
};

// function to delete data
deleteData = (id, confirmed = false) => {
	if (confirmed) {
		$.ajax({
			url: BASE_URL + endpoint + `/${id}`,
			type: "DELETE",
			data: { id },
			dataType: "json",

			success: function (data) {
				console.log(data)
				if (data.error == false) {
					notification("info", "Info!", data.message);
					loadTable();
				} else {
					notification("error", "Error!", data.message);
				}
			},
			error: function ({ responseJSON }) {console.log(data)},
		});
	} else {
		confirmationModal('delete', id);
	}
};

