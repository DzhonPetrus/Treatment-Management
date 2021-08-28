	window.endpoint = 'surgery_type'
	window.token = "TEMPORARY"

	window.form = "#form"
	window.modal = "#modal-surgery_type";
	window.dataTable = "#dataTable";

	window.fields = ["id", "description", "price", "status", "btnAdd", "btnUpdate"];
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
							console.log('successfully added')
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

const loadTable = () => {
    $(dataTable).DataTable({
	  stateSave:true,
      data: surgery_types,
	  aLengthMenu: [5, 10, 20, 30, 50, 100],
	  responsive: true,
	  serverSide: false,
      columns: [
        { data : "name"},
        { data : "description"},
        { data : "price"},
        { data : "status"},
		{
			data: null,
			render: (aData) => renderButtons(aData),
		},
      ],
    });


}

// VIEW DATA
viewData = (id) => {
	{
		$.ajax({
			url: BASE_URL + `${endpoint}/${id}`,
			type: "GET",
			dataType: "json",

			success: data => (data.error == false) ? setState("view", data) : notification("error", "Error!", data.message),
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

			success: data => (data.error == false) ? setState("edit", data) : notification("error", "Error!", data.message),
			error: function ({ responseJSON }) {},
		});
	}
};

// function to delete data
deleteData = (id) => {
	Swal.fire({
		title: "Are you sure you want to delete this record?",
		text: "You won't be able to revert this!",
		icon: "warning",
		showCancelButton: !0,
		confirmButtonColor: "#34c38f",
		cancelButtonColor: "#f46a6a",
		confirmButtonText: "Yes, delete it!",
	}).then(function (t) {
		// if surgery_type clickes yes, it will change the active status to "Not Active".
		if (t.value) {
			$.ajax({
				url: BASE_URL + endpoint,
				type: "DELETE",
				data: { id },
				dataType: "json",

				success: function (data) {
					if (data.error == false) {
						notification("success", "Success!", data.message);
						loadTable();
					} else {
						notification("error", "Error!", data.message);
					}
				},
				error: function ({ responseJSON }) {},
			});
		}
	});
};

