	window.endpoint = 'lab_test'
	

	window.form = "#form"
	window.modal = "#modal-lab_test";
	window.dataTable = "#dataTable";

	window.fields = ["id", "name", "description", "price", "is_active", "btnAdd", "btnUpdate"];
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
		// BUTTONS FOR EXPORT
        dom: 'Blfrtip',
		buttons: [
			{
				extend: 'collection',
				text: '<i class="fa fa-file-export"></i> Export',
				buttons: [
					{
						extend: 'excelHtml5',
						text: '<i class="fa fa-file-excel"></i> Export to Excel',
						titleAttr: 'Export to Excel',
						title: 'Hospital Management System',
						exportOptions: {
							columns: ':not(:last-child)',
						}
					},
					{
						extend: 'csvHtml5',
						text: '<i class="fa fa-file-csv"></i> Export to CSV',
						titleAttr: 'CSV',
						title: 'Hospital Management System',
						exportOptions: {
							columns: ':not(:last-child)',
						}
					},
					{
						extend: 'pdfHtml5',
						text: '<i class="fa fa-file-pdf"></i> Export to PDF',
						titleAttr: 'PDF',
						title: 'Hospital Management System',
						exportOptions: {
							columns: ':not(:last-child)',
						},
					},
				]
			}
		],
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
				data: "is_active",
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
			let lab_tests = settings.json;
			if(lab_tests !== undefined){
				const active_lab_tests = lab_tests.data.filter(types => types.is_active === 'ACTIVE')
				const inactive_lab_tests = lab_tests.data.filter(types => types.is_active === 'INACTIVE')

				$('#totalTests').html(lab_tests.data.length)
				$('#totalTestsActive').html(active_lab_tests.length)
				$('#totalTestsInactive').html(inactive_lab_tests.length)
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

