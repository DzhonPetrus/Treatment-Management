	window.endpoint = (window.user_type).toLowerCase() + '/' + 'treatment'
	

	window.form = "#form"
	window.modal = "#modal-treatment";
	window.dataTable = "#dataTable";

	window.fields = ["id", "treatment_no", "treatment_service_id", "physician_id", "inpatient_id", "outpatient_id", "start_time", "description", "status", "is_active", "btnAdd", "btnUpdate", "session_no", "session_datetime", "drug", "dose", "next_schedule", "comments", "professional_fee", "room", "quantity"];
	window.fieldsHidden = ["btnUpdate", "is_active", "end_time", "treatment_no", "id", "inpatient_id"];
	window.readOnlyFields = ["is_active", "end_time", "treatment_no", "id"];

	const renderAdditionalButtons = (aData) => {
		let buttons = '';
		if(aData.status === 'PENDING'){
			buttons += `
				<div 
					class="dropdown-item d-flex" 
					role="button" 
					onClick="return cancelData('${aData.id}')
				">
					<div style="width:2rem">
						<i class="fa fa-trash-alt"> </i>
					</div>
					<div>Cancel Treatment</div>
				</div>
			`
		}
    buttons += `
				<div 
					class="dropdown-item d-flex" 
					role="button" 
					onClick="return printData('${aData.id}')
				">
					<div style="width:2rem">
						<i class="fa fa-print"> </i>
					</div>
					<div>Print Treatment</div>
				</div>
			`;

		return buttons;
	}

$(function () {

	formReset();
	loadTable();

	// function to save/update record
	$(form).on("submit", function (e) {
		e.preventDefault();
		trimInputFields();


		if ($(form).validate()) {
			var form_data = new FormData(this);

			form_data.append('treatment_no', $("#treatment_no").val())
			form_data.append('id', $("#id").val())
			form_data.append('status', $("#status").val())
			form_data.append('is_active', $("#is_active").val())

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
							window.PrintTreatmentTable(data);
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
			{ sClass: "text-center" },
		],
		columns: [
			{
				data: "treatment_no",
				name: "treatment_no",
				searchable: true,
			},
			{
				data: null,
				render: (data) => {
					let patient = (data.inpatient == null) ? data.outpatient : data.inpatient;
					return  `${patient.last_name}, ${patient.first_name} ${patient.middle_name || ''} ${patient.suffix_name ? ', ' + patient.suffix_name : ''}`
				}
			},
      {
        data: "treatment_service.treatment_type.name",
        name: "treatment_service.treatment_type.name",
        searchable: true,
      },
      {
        data: "treatment_service.name",
        name: "treatment_service.name",
        searchable: true,
      },
			{
				data: "physician",
				name: "physician",
				searchable: true,
				render: (aData) => `${aData.user_profile.last_name}, ${aData.user_profile.first_name} ${aData.user_profile.middle_name || ''} ${aData.user_profile.suffix_name ? ', ' + aData.user_profile.suffix_name : ''}`
			},
			{
				data: "description",
				name: "description",
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
				render: (aData) => renderButtons(aData, "Treatment", renderAdditionalButtons(aData)),
				// render:(data) => console.log(data.treatment_type)
			},
		],
		ajax: {
			url: BASE_URL + `${endpoint}/all`,
			type: "GET",
			ContentType: "application/x-www-form-urlencoded",
		},
		drawCallback: function (settings) {
			// POPULATE ANALYTIC CARDS
			let treatments = settings.json;
			if(treatments !== undefined){
				const active_treatments = treatments.data.filter(treatment => treatment.is_active === 'ACTIVE')
				const inactive_treatments = treatments.data.filter(treatment => treatment.is_active === 'INACTIVE')

				$('#totalTreatments').html(treatments.data.length)
				$('#totalTreatmentsActive').html(active_treatments.length)
				$('#totalTreatmentsInactive').html(inactive_treatments.length)
			}
		},
	});
};

setPrintData = (TREATMENT) => {
localStorage.removeItem("PrintTreatment");


  const patient =
    TREATMENT?.inpatient == null
      ? TREATMENT.outpatient
      : TREATMENT.inpatient;

  const {birth_date, blood_type, gender, contact_no, email, is_active} = patient;
  const age = Math.floor(moment().diff(birth_date, 'years', true));

//   TODO: ADD  INITIAL DIAGNOSIS, DIAGNOSIS, PAST TREATMENTS, PREVIOUS THERAPY
  const initial_diagnosis = "None";
  const diagnosis = "None";
  const past_treatments = "None";
  const previous_therapy = "None";

  const { treatment_no, session_no, session_datetime, drug, dose, next_schedule, status, comments } = TREATMENT;
  const treatment_type = TREATMENT?.treatment_service?.treatment_type?.name;
  const treatment_service = TREATMENT?.treatment_service?.name;
  const treatment_description = TREATMENT?.treatment_service?.description;

  const patient_name = `${patient.last_name}, ${patient.first_name} ${
    patient.middle_name || ""
  } ${patient.suffix_name ? ", " + patient.suffix_name : ""}`;

  const physician = TREATMENT?.physician?.user_profile;

  const physician_name = `${physician.last_name}, ${physician.first_name} ${
    physician.middle_name || ""
  } ${physician.suffix_name ? ", " + physician.suffix_name : ""}`;

  let Treatment = {
 treatment_no, session_no, drug, dose, status, comments ,

    physician_name,
    patient_name,
	birth_date,
	age,
	blood_type,
	gender,
	contact_no,
	email,
	is_active,

	initial_diagnosis,
	diagnosis,
	past_treatments,
	previous_therapy,

	treatment_type,
	treatment_service,
	treatment_description,

	next_schedule : moment(next_schedule).format("llll"),
	session_datetime: moment(session_datetime).format("llll"),


  };
  localStorage.setItem("PrintTreatment", JSON.stringify(Treatment));
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
          window.PrintTreatment();
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
	window.modal = "#modal-treatment-view";
	{
		$.ajax({
			url: BASE_URL + `${endpoint}/${id}`,
			type: "GET",
			dataType: "json",

			success: data => {
				if(data.error == false) {
					 setPrintData(data.data);
					 setState("view", data.data);
					const currentTreatment = data.data;
					setPrintData(currentTreatment);
					setState("view", currentTreatment);

					$('#treatment_type_nameView').html(currentTreatment?.treatment_service?.treatment_type?.name);
					$('#treatment_service_nameView').html(currentTreatment?.treatment_service?.name);
				 }else{
					notification("error", "Error!", data.message);
				 }
			},
			error: (data) => notification("error", data.responseJSON.detail),
		});
	}
};

// Edit DATA
editData = (id) => {
	window.modal = "#modal-treatment";
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



// function to cancel treatment
cancelData = (id, confirmed = false) => {
	if (confirmed) {
		$.ajax({
			url: BASE_URL + endpoint + `/cancel/${id}`,
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
		confirmationModal('cancel', id);
	}
};

