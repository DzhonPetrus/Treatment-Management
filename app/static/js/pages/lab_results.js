	window.endpoint = (window.user_type).toLowerCase() + '/' + 'lab_result'
	

	window.form = "#form"
	window.modal = "#modal-lab_result";
	window.dataTable = "#dataTable";

	window.fields = ["id", "lab_request_id", "specimen", "result", "reference", "unit", "detailed_result", "status", "is_active", "btnAdd", "btnUpdate", "file", "detailed_result_placeholder", "ordered", "dt_requested", "dt_received", "dt_reported", "comments", 'lab_result_no'];
	window.fieldsHidden = ["id", "btnUpdate", "is_active", "detailed_result_placeholder"];
	window.readOnlyFields = ["id", "is_active"];

const renderAdditionalButtons = (aData) => {
  let buttons = `
				<div 
					class="dropdown-item d-flex" 
					role="button" 
					onClick="return printData('${aData.id}')
				">
					<div style="width:2rem">
						<i class="fa fa-print"> </i>
					</div>
					<div>Print Lab Result</div>
				</div>
			`;

  return buttons;
};


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
						text: '<i class="fa fa-file-pdf"></i> Export to PDF',
						action: function(e, dt, button, config) {
							let data = dt.buttons.exportData();
							window.PrintLabResultTable(data);
						},
						titleAttr: "PDF",
						title: "Hospital Management System",
						exportOptions: {
						columns: ":not(:last-child)",
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
				render: (aData) => renderButtons(aData, "Lab Result", renderAdditionalButtons(aData)),
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

setPrintData = (LAB_RESULT) => {
localStorage.removeItem("PrintLabResult");

  const patient =
    LAB_RESULT?.lab_request?.inpatient == null
      ? LAB_RESULT.lab_request?.outpatient
      : LAB_RESULT.lab_request?.inpatient;

  let {birth_date, blood_type, gender, contact_no, email, is_active} = patient;
  const age = Math.floor(moment().diff(birth_date, 'years', true));

//   TODO:  INITIAL DIAGNOSIS
  const creator = LAB_RESULT?.creator?.user_profile;
  const lab_technician = `${creator.last_name}, ${creator.first_name} ${
    creator.middle_name || ""
  } ${creator.suffix_name ? ", " + creator.suffix_name : ""}`;


  const initial_diagnosis = "None";

  const { lab_result_no, result, reference, specimen, ordered, dt_requested, dt_received, dt_reported, comments, status } = LAB_RESULT;

  const lab_type = LAB_RESULT?.lab_request?.laboratory_service?.laboratory_type?.name;
  const lab_service = LAB_RESULT?.lab_request?.laboratory_service?.name;

  const name = `${patient.last_name}, ${patient.first_name} ${
    patient.middle_name || ""
  } ${patient.suffix_name ? ", " + patient.suffix_name : ""}`;

  let LabResult = {
    name,
	birth_date,
	age,
	blood_type,
	gender,
	contact_no,
	email,
	is_active,

	lab_technician,
	initial_diagnosis,

	lab_result_no,
	specimen,
	ordered,
	result,
	reference,
	dt_requested: moment(dt_requested).format("llll"),
	dt_received: moment(dt_received).format("llll"),
	dt_reported: moment(dt_reported).format("llll"),
	comments,
	status,

	lab_type,
	lab_service,

	lab_request_no: LAB_RESULT?.lab_request?.lab_request_no,
  };
  localStorage.setItem("PrintLabResult", JSON.stringify(LabResult));
};

// PRINT DATA
printData = (id) => {
  {
    $.ajax({
      url: BASE_URL + `${endpoint}/${id}`,
      type: "GET",
      dataType: "json",

      // success: data => (data.error == false) ? setState("view", data.data) : notification("error", "Error!", data.message),
      success: (data) => {
        if (data.error == false) {
          // DATA FOR PRINTING
          setPrintData(data.data);
          window.PrintLabResult();
        } else {
          notification("error", "Error!", data.message);
        }
      },
      error: (data) => notification("error", data.responseJSON.detail),
    });
  }
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
					setPrintData(data.data);
					setState("view", data.data);

					currentLabRequest = data.data?.lab_request;

					$('#lab_type_nameView').html(currentLabRequest?.laboratory_service?.laboratory_type?.name);
					$('#lab_service_nameView').html(currentLabRequest?.laboratory_service?.name);
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

