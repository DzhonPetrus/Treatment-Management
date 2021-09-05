	window.endpoint = 'surgery'
	window.token = "TEMPORARY"

	window.form = "#form"
	window.modal = "#modal-surgery";
	window.dataTable = "#dataTable";

	window.fields = ["id", "surgery_type_id", "room", "patient_id", "status", "is_active", "btnAdd", "btnUpdate"];
	window.fieldsHidden = ["id", "btnUpdate", "is_active"];
	window.readOnlyFields = ["id", "is_active"];

$(function () {

	formReset();
	loadTable();

	// function to save/update record
	$(form).on("submit", function (e) {
		e.preventDefault();
		trimInputFields();

		if ($(form).validate()) {
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
							formReset();
							notification("success", "Success!", data.message);
						} else {
							notification("error", "Error!", data.message);
						}
					},
					error: (data) => notification("error", data.responseJSON.detail),
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
					error: (data) => notification("error", data.responseJSON.detail),
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
				data: "patient",
				name: "patient",
				searchable: true,
			},
			{
				data: "room",
				name: "room",
				searchable: true,
			},
			{
				data: "surgery_type",
				name: "surgery_type",
				searchable: true,
			},
			{
				data: "start_date",
				name: "start_date",
				searchable: true,
			},
			{
				data: "end_date",
				name: "end_date",
				searchable: true,
			},
			{
				data: "status",
				name: "status",
				searchable: true,
			},
			{
				data: "is_active",
				render: (aData) => aData.toUpperCase() == "ACTIVE" ? `<span class="p-2 w-100 badge badge-primary">${aData}</span>` : `<span class="p-2 w-100 badge badge-danger">${aData}</span>`,
				// name: "status",
				// searchable: true,
			},
			{
				data: null,
				render: (aData) => console.log(aData)
			},
		],
		ajax: {
			url: BASE_URL + `${endpoint}/all`,
			type: "GET",
			ContentType: "application/x-www-form-urlencoded",
			success: (data) => console.log(data)
		},
		drawCallback: function (settings) {
			// POPULATE ANALYTIC CARDS
			let surgeries = settings.json;
			if(surgeries !== undefined){
				const active_surgeries = surgeries.data.filter(surgery => surgery.is_active === 'ACTIVE')
				const inactive_surgeries = surgeries.data.filter(surgery => surgery.is_active === 'INACTIVE')

				$('#totalSurgeries').html(surgeries.data.length)
				$('#totalSurgeriesActive').html(active_surgeries.length)
				$('#totalSurgeriesInactive').html(inactive_surgeries.length)
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
			error: (data) => notification("error", data.responseJSON.detail),
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
			error: (data) => notification("error", data.responseJSON.detail),
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
				if (data.error == false) {
					$('#confirmModal').modal("hide");
					notification("info", "Info!", data.message);
					loadTable();
				} else {
					notification("error", "Error!", data.message);
				}
			},
			error: (data) => notification("error", data.responseJSON.detail),
		});
	} else {
		confirmationModal('delete', id);
	}
};


// function to reactivate data
reactivateData = (id, confirmed = false) => {
	if (confirmed) {
		$.ajax({
			url: BASE_URL + endpoint + `/reactivate/${id}`,
			type: "PUT",
			data: { id },
			dataType: "json",

			success: function (data) {
				if (data.error == false) {
					$('#confirmModal').modal("hide");
					notification("info", "Info!", data.message);
					loadTable();
				} else {
					notification("error", "Error!", data.message);
				}
			},
			error: (data) => notification("error", data.responseJSON.detail),
		});
	} else {
		confirmationModal('reactivate', id);
	}
};

