$(function () {
	$.ajaxSetup({
		headers: {
			Accept: "application/json",
			Authorization: "Bearer " + token,
			ContentType: "application/x-www-form-urlencoded",
		},
	});

	// USERS
	$.ajax({
		url: BASE_URL + `admin/user/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const users = data.data;
			const active_users = users.filter(user => user.is_active === 'ACTIVE')
			const inactive_users = users.filter(user => user.is_active === 'INACTIVE')
			const totalUsers = users.length;
			const totalUsersActive = active_users.length;
			const totalUsersInactive = inactive_users.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});


	// PATIENTS
	$.ajax({
		url: BASE_URL + `admin/patient/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const patients = data.data;
			const active_patients = patients.filter(patient => patient.is_active === 'ACTIVE')
			const inactive_patients = patients.filter(patient => patient.is_active === 'INACTIVE')

			const total_patients = patients.length;
			const total_active_patients = active_patients.length;
			const total_inactive_patients = inactive_patients.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});



	// TREATMENT TYPES
	$.ajax({
		url: BASE_URL + `admin/treatment_type/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const treatment_types = data.data;
			const active_treatment_types = treatment_types.filter(treatment_type => treatment_type.is_active === 'ACTIVE')
			const inactive_treatments = treatments.filter(treatment_type => treatment_type.is_active === 'INACTIVE')

			const total_treatment_types = treatment_types.length;
			const total_active_treatment_types = active_treatment_types.length;
			const total_inactive_treatment_types = inactive_treatment_types.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});



	// LAB REQUESTS
	$.ajax({
		url: BASE_URL + `admin/lab_request/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const lab_requests = data.data;
			const active_lab_requests = lab_requests.filter(lab_request => lab_request.is_active === 'ACTIVE')
			const inactive_lab_requests = lab_requests.filter(lab_request => lab_request.is_active === 'INACTIVE')

			const total_lab_requests = lab_requests.length;
			const total_active_lab_requests = active_lab_requests.length;
			const total_inactive_lab_requests = inactive_lab_requests.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});



	// LAB TESTS
	$.ajax({
		url: BASE_URL + `admin/lab_test/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const lab_tests = data.data;
			const active_lab_tests = lab_tests.filter(lab_test => lab_test.is_active === 'ACTIVE')
			const inactive_lab_tests = lab_tests.filter(lab_test => lab_test.is_active === 'INACTIVE')

			const total_lab_tests = lab_tests.length;
			const total_active_lab_tests = active_lab_tests.length;
			const total_inactive_lab_tests = inactive_lab_tests.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});



	// SURGERIES
	$.ajax({
		url: BASE_URL + `admin/surgery/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const surgeries = data.data;
			const active_surgeries = surgery.filter(surgery => surgery.is_active === 'ACTIVE')
			const inactive_surgeries = surgery.filter(surgery => surgery.is_active === 'INACTIVE')

			const total_surgeries = surgeries.length;
			const total_active_surgeries = active_surgeries.length;
			const total_inactive_surgeries = inactive_surgeries.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});



	// SURGERY TYPES
	$.ajax({
		url: BASE_URL + `admin/surgery_type/all`,
		type: "GET",
		dataType: "json",

		success: data => {
			const surgery_types = data.data;
			const active_surgery_types = surgery_types.filter(surgery_type => surgery_type.is_active === 'ACTIVE')
			const inactive_surgery_types = surgery_types.filter(surgery_type => surgery_type.is_active === 'INACTIVE')

			const total_surgery_types = surgery_types.length;
			const total_active_surgery_types = active_surgery_types.length;
			const total_inactive_surgery_types = inactive_surgery_types.length;

		},
		error: (data) => notification("error", data.responseJSON.detail),
	});





});