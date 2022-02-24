	window.endpoint = (window.user_type).toLowerCase() + '/' + 'treatment'
	

	window.form = "#form"
	window.modal = "#modal-treatment";
	window.dataTable = "#dataTable";

	window.fields = ["id", "treatment_no", "treatment_type_id", "physician_id", "inpatient_id", "outpatient_id", "start_time", "description", "status", "is_active", "btnAdd", "btnUpdate", "session_no", "session_datetime", "drug", "dose", "next_schedule", "comments", "professional_fee", "room", "quantity"];
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
				data: "treatment_type",
				name: "treatment_type",
				searchable: true,
				render: aData => aData.name
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
console.log(TREATMENT)

// comments: "comment"
// created_at: "2022-02-19T11:07:45"
// description: "desc"
// dose: null
// drug: null
// id: "1c8a376c-9131-11ec-a80e-1c1b0ddb5781"
// inpatient:
// birth_date: "1994-01-05"
// blood_type: "O-"
// contact_no: "09123456789"
// email: "in@patient.com"
// first_name: "In"
// full_name: "Patient, In  "
// gender: "Male"
// is_active: "ACTIVE"
// last_name: "Patient"
// middle_name: null
// picture: null
// suffix_name: null
// [[Prototype]]: Object
// inpatient_id: "8a09d9aa-90aa-11ec-a5f2-1c1b0ddb5781"
// is_active: "ACTIVE"
// next_schedule: null
// outpatient: null
// outpatient_id: null
// physician:
// created_at: "2022-02-06T23:25:32"
// email: "surgeon2@surgeon.com"
// handled_surgeries: {room: null, patient_id: null, surgery_type_id: null, in_charge: null, start_time: null, …}
// id: "064f2fb8-8761-11ec-93ec-1c1b0ddb5781"
// is_active: "ACTIVE"
// password: "$2b$12$CmjBQe8ZKH9hZ/eeCIBWUePTesKYhoZsy5di0YURYhyDlyDJjwxOe"
// updated_at: null
// user_profile: {department: 'Emergency Room', position: 'Surgeon', first_name: 'surgeon', middle_name: null, last_name: 'last', …}
// user_profile_id: "b4c98c92-8760-11ec-93ec-1c1b0ddb5781"
// user_type: "Surgeon"
// [[Prototype]]: Object
// physician_id: "064f2fb8-8761-11ec-93ec-1c1b0ddb5781"
// physician_name: "last, surgeon  "
// professional_fee: 550
// quantity: 1
// room: "111"
// session_datetime: "2022-02-19T11:07:00"
// session_no: 1
// status: "PENDING"
// treatment_no: "TN-FA2205C1"
// treatment_type:
// description: "treatment3"
// fee: 333
// is_active: "ACTIVE"
// name: "treatment3"
// room: "333"
// [[Prototype]]: Object
// treatment_type_id: "1780df60-60a7-11ec-88bf-f0761c112d4e"
// treatment_type_name: "treatment3"
// updated_at: null


//   const patient =
//     TREATMENT?.lab_request?.inpatient == null
//       ? TREATMENT.lab_request?.outpatient
//       : TREATMENT.lab_request?.inpatient;

//   const {birth_date, blood_type, gender, contact_no, email, is_active} = patient;
//   const age = Math.floor(moment().diff(birth_date, 'years', true));

// //   TODO: ADD LAB TECHNICIAN & INITIAL DIAGNOSIS
//   const lab_technician = "Temporary Technician";
//   const initial_diagnosis = "None";

//   const { lab_result_no, result, reference, specimen, ordered, dt_requested, dt_received, dt_reported, comments, status } = TREATMENT;

//   // TODO: CHANGE LAB_TYPE
//   const lab_type = TREATMENT?.lab_request?.lab_test?.name;
//   const lab_test = TREATMENT?.lab_request?.lab_test?.name;

//   const name = `${patient.last_name}, ${patient.first_name} ${
//     patient.middle_name || ""
//   } ${patient.suffix_name ? ", " + patient.suffix_name : ""}`;

//   let Treatment = {
//     name,
// 	birth_date,
// 	age,
// 	blood_type,
// 	gender,
// 	contact_no,
// 	email,
// 	is_active,

// 	lab_technician,
// 	initial_diagnosis,

// 	lab_result_no,
// 	specimen,
// 	ordered,
// 	result,
// 	reference,
// 	dt_requested: moment(dt_requested).format("llll"),
// 	dt_received: moment(dt_received).format("llll"),
// 	dt_reported: moment(dt_reported).format("llll"),
// 	comments,
// 	status,

// 	lab_type,
// 	lab_test,

// 	lab_request_no: TREATMENT?.lab_request?.lab_request_no,
//   };
//   localStorage.setItem("PrintTreatment", JSON.stringify(Treatment));
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

