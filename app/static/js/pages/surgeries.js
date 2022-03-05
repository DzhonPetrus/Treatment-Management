window.endpoint = window.user_type.toLowerCase() + "/" + "surgery";

window.form = "#form";
window.modal = "#modal-surgery";
window.dataTable = "#dataTable";

window.fields = [
  "id",
  "surgery_service_id",
  "room",
  "inpatient_id",
  "start_time",
  "end_time",
  "status",
  "is_active",
  "btnAdd",
  "btnUpdate",
  "surgery_no",
  "head_surgeon_id",
  "description",
  "surgeon_in_charge",
  "nurse_in_charge",
];
window.fieldsHidden = [
  "id",
  "btnUpdate",
  "is_active",
  "end_time",
  "surgery_no",
];
window.readOnlyFields = ["id", "is_active", "end_time", "surgery_no"];

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
					<div>Cancel Surgery</div>
				</div>
			`;
  }

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
      // var form_data = new FormData(this);

      // form_data.append("id", $("#id").val());
      // form_data.append("start_time", $("#start_time").val());
      // form_data.append("end_time", $("#end_time").val());
      // form_data.append("status", $("#status").val());
      // form_data.append("is_active", $("#is_active").val());

      var form_data = new FormData();

      fieldsAppendToFormData(form_data);

      in_charge = $("#surgeon_in_charge").val();
      in_charge = [...in_charge, ...$("#nurse_in_charge").val()];
      form_data.append("in_charge", in_charge);

      // console.log(form_data.get('in_charge'))
      // console.log(in_charge)

      // console.table([...form_data]);
      // console.log(form_data);
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
          {
            extend: "pdfHtml5",
            text: '<i class="fa fa-file-pdf"></i> Export to PDF',
            titleAttr: "PDF",
            title: "Hospital Management System",
            exportOptions: {
              columns: ":not(:last-child)",
            },
          },
          "colvis",
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
        data: "surgery_no",
        name: "surgery_no",
        searchable: true,
      },
      {
        data: "inpatient",
        name: "inpatient",
        searchable: true,
        render: (aData) =>
          `${aData.last_name}, ${aData.first_name} ${aData.middle_name || ""} ${
            aData.suffix_name ? ", " + aData.suffix_name : ""
          }`,
      },
      {
        data: "room",
        name: "room",
        searchable: true,
      },
      {
        data: "surgery_service.surgery_type_info.surgery_type_name",
        name: "surgery_service.surgery_type_info.surgery_type_name",
        searchable: true,
      },
      {
        data: "surgery_service.surgery_service_name",
        name: "surgery_service.surgery_service_name",
        searchable: true,
      },
      {
        data: "start_time",
        searchable: true,
        render: (data) => moment(data).format("YYYY-MM-DD"),
      },
      {
        data: "start_time",
        name: "start_time",
        searchable: true,
        render: (data) =>
          formatDateTime(data) +
          `<div class="text-secondary fomt-italic">${moment(
            data
          ).fromNow()}</div><div class="d-none text-secondary fomt-italic">${moment(
            data
          ).format("YYYY-MM-DD hh:mm:ss")}</div>`,
      },
      {
        data: "end_time",
        name: "end_time",
        searchable: true,
        render: (data) =>
          data == null
            ? `<div class='text-secondary font-italic'>No data</div>`
            : formatDateTime(data) +
              `<div class='font-italic text-secondary'>${moment(
                data
              ).fromNow()}</div>`,
      },
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
          renderButtons(aData, "Surgery", renderAdditionalButtons(aData)),
        // render:(data) => console.log(data.surgery_type)
      },
    ],
    ajax: {
      url: BASE_URL + `${endpoint}/all`,
      type: "GET",
      ContentType: "application/x-www-form-urlencoded",
    },
    drawCallback: function (settings) {
      // POPULATE ANALYTIC CARDS
      let surgeries = settings.json;
      if (surgeries !== undefined) {
        const active_surgeries = surgeries.data.filter(
          (surgery) => surgery.is_active === "ACTIVE"
        );
        const inactive_surgeries = surgeries.data.filter(
          (surgery) => surgery.is_active === "INACTIVE"
        );

        $("#totalSurgeries").html(surgeries.data.length);
        $("#totalSurgeriesActive").html(active_surgeries.length);
        $("#totalSurgeriesInactive").html(inactive_surgeries.length);
          
        // TODO: READY FOR POPULATING WITH "MY SURGERIES"
        //   window.mySurgeries = [];

        // surgeries?.data?.forEach(_data =>{
        //   _isMySurgery = _data?.in_charge.filter(_d => _d?.in_charge_id == window.user_id);
        //   if(_isMySurgery?.length > 0)
        //     window.mySurgeries.push(_data)

        // });

      }
    },
  });
  $.ajax({
    url: BASE_URL + `admin/user/all/surgical_nurse`,
    type: "GET",
    dataType: "json",
    success: function (data) {
      options = "";
      data.data.forEach((data) => {
        options += `
					<option value="${data.id}">${data.user_profile?.last_name}, ${data.user_profile?.first_name}</option>
				`;
      });
      $("#nurse_in_charge").html(options);
    },
    error: (data) => notification("error", data.responseJSON.detail),
  });
  $.ajax({
    url: BASE_URL + `admin/user/all/surgeon`,
    type: "GET",
    dataType: "json",
    success: function (data) {
      options = "";
      data.data.forEach((data) => {
        options += `
					<option value="${data.id}">${data.user_profile?.last_name}, ${data.user_profile?.first_name}</option>
				`;
      });
      $("#surgeon_in_charge").html(options);
    },
    error: (data) => notification("error", data.responseJSON.detail),
  });

  let tbl = $(dataTable).DataTable();
  // $('#filter_date').hide();
  $("#filter_date").on("change", () => tbl.draw());
  $("#filter_select").select2();
  $("#filter_select").on("select2:select", function () {
    // $('#filter_date').hide();
    let selected = this.value;
    switch (selected) {
      case "ALL":
        filter_all();
        break;
      case "TODAY":
        filter_today();
        break;
      case "THIS WEEK":
        filter_week();
        break;
      case "THIS MONTH":
        filter_month();
        break;
      case "THIS YEAR":
        filter_year();
        break;
      case "CUSTOM":
        filter_custom();
        this.value = null;
        break;
    }
    tbl.draw();
  });

  filter_all = () =>
    $("#filter_date").val(
      `${moment()
        .subtract(30, "year")
        .startOf("month")
        .format("YYYY-MM-DD")} - ${moment()
        .endOf("month")
        .format("YYYY-MM-DD")}`
    );

  filter_today = () =>
    $("#filter_date").val(
      `${moment().format("YYYY-MM-DD")} - ${moment().format("YYYY-MM-DD")}`
    );

  filter_week = () =>
    $("#filter_date").val(
      `${moment().subtract(6, "days").format("YYYY-MM-DD")} - ${moment().format(
        "YYYY-MM-DD"
      )}`
    );

  filter_month = () =>
    $("#filter_date").val(
      `${moment().startOf("month").format("YYYY-MM-DD")} - ${moment()
        .endOf("month")
        .format("YYYY-MM-DD")}`
    );

  filter_year = () =>
    $("#filter_date").val(
      `${moment().startOf("year").format("YYYY-MM-DD")} - ${moment()
        .endOf("year")
        .format("YYYY-MM-DD")}`
    );

  filter_custom = () => {
    // $('#filter_date').show();
    $("#filter_date").focus();
  };

  tbl.column(5).visible(false);
};

// VIEW DATA
viewData = (id) => {
  window.modal = "#modal-surgery-view";
  {
    $.ajax({
      url: BASE_URL + `${endpoint}/${id}`,
      type: "GET",
      dataType: "json",

      success: (data) => {
        if (data.error == false) {
          const currentSurgery = data.data;

          // setPrintData(currentSurgery);
          setState("view", currentSurgery);


          $("#surgery_type_nameView").html(
            currentSurgery?.surgery_service?.surgery_type_info?.surgery_type_name
          );
          $("#surgery_service_nameView").html(
            currentSurgery?.surgery_service?.surgery_service_name
          );

			const head_surgeon = currentSurgery?.head_surgeon?.user_profile;
          const head_surgeon_name = `${head_surgeon.last_name}, ${
            head_surgeon.first_name
          } ${head_surgeon.middle_name || ""} ${
            head_surgeon.suffix_name ? ", " + head_surgeon.suffix_name : ""
          }`;
          $("#head_surgeon_nameView").html(
            head_surgeon_name
          );

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
	window.modal = "#modal-surgery";
  {
    $.ajax({
      url: BASE_URL + `${endpoint}/${id}`,
      type: "GET",
      data: { id },
      dataType: "json",

      success: (data) =>{
        if(data.error == false){
					const currentSurgery = data.data;
          setState("edit", currentSurgery);
          console.log(currentSurgery)

          // TODO: CLARIFY/FINALIZE
          // IN_CHARGES
          const in_charge = currentSurgery?.in_charge;
          let _surgeons = [];
          let _surgical_nurses = [];
          in_charge.forEach(v => {
            let position = v?.in_charge?.user_type.toLowerCase();

            if(position == 'surgeon')
              _surgeons.push(v?.in_charge_id);

            if(position == 'surgical_nurse')
              _surgical_nurses.push(v?.in_charge_id);

            window.temp_end_time = $('#end_time').val();

            if(currentSurgery?.status != 'PENDING'){
              setFieldsReadOnly(fields,true);
              $("#status").prop('disabled', false);
            }
          });

          $('#surgeon_in_charge').val(_surgeons).trigger('change');
          $('#nurse_in_charge').val(_surgical_nurses).trigger('change');

          $('#head_surgeon_id').val(currentSurgery?.head_surgeon_id).trigger('change');


					$(`#inpatient_id`).val(currentSurgery?.inpatient_id).trigger('change');

					$("#surgery_types_id").val(currentSurgery?.surgery_service?.surgery_type_info?.surgery_type_name).trigger('change');

					$("#surgery_service_id").val(currentSurgery?.surgery_service_id).trigger('change');
        }else{
          notification("error", "Error!", data.message);
        }
      },
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

// function to cancel surgery
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
