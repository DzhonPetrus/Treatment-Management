	window.endpoint = (window.user_type).toLowerCase() + '/' + 'lab_result'
	

	window.form = "#form"
	window.modal = "#modal-lab_result";
	window.dataTable = "#dataTable";

	window.fields = ["id", "lab_request_id", "specimen", "result", "reference", "unit", "detailed_result", "status", "is_active", "btnAdd", "btnUpdate", "file", "detailed_result_placeholder", "ordered", "dt_requested", "dt_received", "dt_reported", "comments"];
	window.fieldsHidden = ["id", "btnUpdate", "is_active", "detailed_result_placeholder"];
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
			form_data.append('is_active', $('#is_active').val());
			form_data.append('status', $('#status').val());

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
        dom: "<'row'<'col-sm-12 col-md-6'Bl><'col-sm-12 col-md-6'f>>" +
"<'row'<'col-sm-12'tr>>" +
"<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
		buttons: [
			{
				extend: 'collection',
className: 'btn-sm',
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
			{ sClass: "text-left" },
			{ sClass: "text-left" },
			{ sClass: "text-left" },
			{ sClass: "text-center" },
		],
		columns: [
			{
				data: "lab_request",
				name: "lab_request",
				searchable: true,
				render: data => data.lab_request_no
			},
			{
				data: "specimen",
				name: "specimen",
				searchable: true,
			},
			{
				data: "result",
				name: "result",
				searchable: true,
			},
			{
				data: "reference",
				name: "reference",
				searchable: true,
			},
			{
				data: "unit",
				name: "unit",
				searchable: true,
			},
			{
				data: "detailed_result",
				name: "detailed_result",
				searchable: true,
				render: (aData) => `<a target="_blank" href="${BASE_URL}static/upload/${aData}">${aData}</a>` || `<span class='font-italic text-secondary'>No data</span>`
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
				render: (aData) => renderButtons(aData, "Lab Result"),
			},
		],
		ajax: {
			url: BASE_URL + `${endpoint}/all`,
			type: "GET",
			ContentType: "application/x-www-form-urlencoded",
		},
		drawCallback: function (settings) {
			// POPULATE ANALYTIC CARDS
			let lab_results = settings.json;
			if(lab_results !== undefined){
				const active_lab_results = lab_results.data.filter(types => types.is_active === 'ACTIVE')
				const inactive_lab_results = lab_results.data.filter(types => types.is_active === 'INACTIVE')

				$('#totalLabResults').html(lab_results.data.length)
				$('#totalLabResultsActive').html(active_lab_results.length)
				$('#totalLabResultsInactive').html(inactive_lab_results.length)
			}
		},
	});
};

// VIEW DATA
viewData = (id) => {
	window.modal = "#modal-lab_result-view";
	{
		$.ajax({
			url: BASE_URL + `${endpoint}/${id}`,
			type: "GET",
			dataType: "json",

			success: data => {
				if (data.error == false) { 
					setState("view", data.data);
					lab_test_name = data.data?.lab_request?.lab_test?.name;
					$('#lab_testView').html(lab_test_name);
				} else {
					notification("error", "Error!", data.message)
				}
			},
			error: (data) => notification("error", data.responseJSON.detail),
		});
	}
};

// Edit DATA
editData = (id) => {
	window.modal = "#modal-lab_result";
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

