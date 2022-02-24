window.endpoint = window.user_type.toLowerCase() + "/" + "lab_request";

window.form = "#form";
window.modal = "#modal-lab_request";
window.dataTable = "#dataTable";

window.fields = [
  "id",
  "lab_test_id",
  "lab_result_id",
  "status",
  "is_active",
  "btnAdd",
  "btnUpdate",
  "lab_request_no",
  "inpatient_id",
  "outpatient_id",
  "quantity",
];
window.fieldsHidden = [
  "id",
  "btnUpdate",
  "is_active",
  "lab_request_no",
  "inpatient_id",
];
window.readOnlyFields = ["id", "is_active", "lab_request_no"];

const renderAdditionalButtons = (aData) => {
  let buttons = "";
  if (aData.status === "PENDING") {
    buttons += `
				<div 
					class="dropdown-item d-flex" 
					role="button" 
					onClick="return cancelData('${aData.id}')
				">
					<div style="width:2rem">
						<i class="fa fa-trash-alt"> </i>
					</div>
					<div>Cancel Lab Request</div>
				</div>
				
			`;
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
					<div>Print Lab Request</div>
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

      form_data.append("id", $("#id").val());
      form_data.append("status", $("#status").val());
      form_data.append("is_active", $("#is_active").val());

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
    dom:
      "<'row'<'col-sm-12 col-md-6'Bl><'col-sm-12 col-md-6'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    buttons: [
      {
        extend: "collection",
        className: "btn-sm",
        text: '<i class="fa fa-file-export"></i> Export',
        buttons: [
          {
            extend: "excelHtml5",
            text: '<i class="fa fa-file-excel"></i> Export to Excel',
            titleAttr: "Export to Excel",
            title: "Hospital Management System",
            exportOptions: {
              columns: ":not(:last-child)",
            },
          },
          {
            extend: "csvHtml5",
            text: '<i class="fa fa-file-csv"></i> Export to CSV',
            titleAttr: "CSV",
            title: "Hospital Management System",
            exportOptions: {
              columns: ":not(:last-child)",
            },
          },
		//   CLASSIC DIRECT
        //   {
        //     extend: "pdfHtml5",
        //     text: '<i class="fa fa-file-pdf"></i> Export to PDF',
        //     titleAttr: "PDF",
        //     title: "Hospital Management System",
        //     exportOptions: {
        //       columns: ":not(:last-child)",
        //     },
        //   },
          {
            text: '<i class="fa fa-file-pdf"></i> Export to PDF',
			action: function(e, dt, button, config) {
				let data = dt.buttons.exportData();
				window.PrintLabRequestTable(data);
			},
            titleAttr: "PDF",
            title: "Hospital Management System",
            exportOptions: {
              columns: ":not(:last-child)",
            },
          },
        ],
      },
    ],
    responsive: true,
    serverSide: false,
    stateSave: true,
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
        data: "lab_request_no",
        name: "lab_request_no",
        searchable: true,
      },
      {
        data: null,
        render: (data) => {
          let patient =
            data.inpatient == null ? data.outpatient : data.inpatient;
          return `${patient.last_name}, ${patient.first_name} ${
            patient.middle_name || ""
          } ${patient.suffix_name ? ", " + patient.suffix_name : ""}`;
        },
      },
      {
        data: "lab_test.name",
        name: "lab_test.name",
        searchable: true,
      },
      // {
      // 	data: "lab_result.result",
      // 	name: "lab_result.result",
      // 	searchable: true,
      // },
      {
        data: "status",
        name: "status",
        searchable: true,
      },
      {
        data: "is_active",
        render: (aData) =>
          aData.toUpperCase() == "ACTIVE"
            ? `<span class="p-2 w-100 badge badge-primary">${aData}</span>`
            : `<span class="p-2 w-100 badge badge-danger">${aData}</span>`,
        // name: "status",
        // searchable: true,
      },
      {
        data: null,
        render: (aData) =>
          renderButtons(aData, "Lab Request", renderAdditionalButtons(aData)),
        // render:(data) => console.log(data.lab_request_type)
      },
    ],
    ajax: {
      url: BASE_URL + `${endpoint}/all`,
      type: "GET",
      ContentType: "application/x-www-form-urlencoded",
    },
    drawCallback: function (settings) {
      // POPULATE ANALYTIC CARDS
      let lab_requests = settings.json;
      if (lab_requests !== undefined) {
        const active_lab_requests = lab_requests.data.filter(
          (lab_request) => lab_request.is_active === "ACTIVE"
        );
        const inactive_lab_requests = lab_requests.data.filter(
          (lab_request) => lab_request.is_active === "INACTIVE"
        );

        $("#totalLabRequests").html(lab_requests.data.length);
        $("#totalLabRequestsActive").html(active_lab_requests.length);
        $("#totalLabRequestsInactive").html(inactive_lab_requests.length);
      }
    },
  });
};

setPrintData = (LAB_REQUEST) => {
localStorage.removeItem("PrintLabRequest");
console.log(LAB_REQUEST)
  const patient =
    LAB_REQUEST?.inpatient == null
      ? LAB_REQUEST.outpatient
      : LAB_REQUEST.inpatient;
  const name = `${patient.last_name}, ${patient.first_name} ${
    patient.middle_name || ""
  } ${patient.suffix_name ? ", " + patient.suffix_name : ""}`;
  let LabRequest = {
    name,
    request_number: LAB_REQUEST?.lab_request_no,
    request_type: LAB_REQUEST?.lab_test?.name,
    request_service: LAB_REQUEST?.lab_test?.name,
    fee: LAB_REQUEST?.lab_test?.fee,
    quantity: LAB_REQUEST?.quantity,
    dt_requested: moment(LAB_REQUEST?.created_at).format("llll"),
    status: LAB_REQUEST?.status,
  };
  localStorage.setItem("PrintLabRequest", JSON.stringify(LabRequest));
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
          window.PrintLabRequest();
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
  window.modal = "#modal-lab_request-view";
  {
    $.ajax({
      url: BASE_URL + `${endpoint}/${id}`,
      type: "GET",
      dataType: "json",

      // success: data => (data.error == false) ? setState("view", data.data) : notification("error", "Error!", data.message),
      success: (data) => {
        if (data.error == false) {
          setPrintData(data.data);
          setState("view", data.data);
        } else {
          notification("error", "Error!", data.message);
        }
      },
      error: (data) => notification("error", data.responseJSON.detail),
    });
  }
};

// Edit DATA
editData = (id) => {
  window.modal = "#modal-lab_request";
  {
    $.ajax({
      url: BASE_URL + `${endpoint}/${id}`,
      type: "GET",
      data: { id },
      dataType: "json",

      success: (data) =>
        data.error == false
          ? setState("edit", data.data)
          : notification("error", "Error!", data.message),
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
          $("#confirmModal").modal("hide");
          notification("info", "Info!", data.message);
          loadTable();
        } else {
          notification("error", "Error!", data.message);
        }
      },
      error: (data) => notification("error", data.responseJSON.detail),
    });
  } else {
    confirmationModal("delete", id);
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
          $("#confirmModal").modal("hide");
          notification("info", "Info!", data.message);
          loadTable();
        } else {
          notification("error", "Error!", data.message);
        }
      },
      error: (data) => notification("error", data.responseJSON.detail),
    });
  } else {
    confirmationModal("reactivate", id);
  }
};

// function to cancel lab_request
cancelData = (id, confirmed = false) => {
  if (confirmed) {
    $.ajax({
      url: BASE_URL + endpoint + `/cancel/${id}`,
      type: "PUT",
      data: { id },
      dataType: "json",

      success: function (data) {
        if (data.error == false) {
          $("#confirmModal").modal("hide");
          notification("info", "Info!", data.message);
          loadTable();
        } else {
          notification("error", "Error!", data.message);
        }
      },
      error: (data) => notification("error", data.responseJSON.detail),
    });
  } else {
    confirmationModal("cancel", id);
  }
};
