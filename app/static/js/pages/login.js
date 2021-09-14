toastr.options = {
    'positionClass': 'toast-top-center'
};

const notification = (type, title, message)=> {
    return toastr[type](message,title);
};

formReset = () => {
	$("html", "body").animate({ scrollTop: 0 }, "slow");

	$("#form")[0].reset();
};

trimInputFields = () => 
{
    var allInputs = $("input:not(:file())");
    allInputs.each(function () 
    {
        $(this).val($.trim($(this).val()));
    });
};

$(function () {
	formReset();

	// function to save/update record
	$("#form").on("submit", function (e) {
		e.preventDefault();
		trimInputFields();


		if ($("#form").validate()) {
			var form_data = new FormData(this);
			form_data.append('username', $("#email").val());

			// add record
			$.ajax({
				url: BASE_URL + 'login',
				type: "POST",
				data: form_data,
				dataType: "JSON",
				contentType: false,
				processData: false,
				cache: false,
				success: (data) => {
					setToken(data.access_token);
					window.token = getToken();
					console.log(token)
					console.log(data.user_type)
				},
				error: (data) => notification("warning", data.responseJSON.detail),
			});
		}
	});
});
