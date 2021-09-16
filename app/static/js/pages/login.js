	
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

$(async function () {
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
					setUserType(data.user_type.toLowerCase());
					window.user_type = getUserType();
					fetch(`${BASE_URL}admin/user/${data.id}`, {
						method: 'GET',
						headers: {
							Authorization: `bearer ${token}`
						}
					})
						.then(res => res.json())
						.then(data => setUserProfile(JSON.stringify(data.data.user_profile)))
					window.user_profile = getUserProfile();
					location.replace(`${BASE_URL}${window.user_type}/`);
				},
				error: (data) => notification("warning", data.responseJSON.detail),
			});
		}
	});
});
