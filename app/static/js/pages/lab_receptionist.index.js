// AJAX GET
async function ajaxGet(_endpoint) {
  const result = await $.ajax({
    headers: {
      Accept: "application/json",
      Authorization: "Bearer " + token,
      ContentType: "application/x-www-form-urlencoded",
    },
    url: `${BASE_URL}admin/${_endpoint}/all`,
    type: "GET",
    dataType: "json",
  });
  return result.data;
}

// HEX COLOR GENERATOR
const random_hex_color_code = () => {
  let n = (Math.random() * 0xfffff * 1000000).toString(16);
  return "#" + n.slice(0, 6);
};



//-------------
//- CARDS
//-------------
(async() => {
  let _totalLabRequests = await ajaxGet('lab_request');
  let _totalLabTestTypes = await ajaxGet('lab_test_type');

  $('#totalLabRequestsCard').html(_totalLabRequests.length);
  $('#totalLabTestTypesCard').html(_totalLabTestTypes.length);
})();




    //--------------
    //- PATIENT CHART
    //--------------
(async () => {
    let _outpatients = await ajaxGet("outpatient");
    let _inpatients = await ajaxGet("inpatient");
    let _patients = [..._outpatients, ..._inpatients];
    const _totalPatients = _patients.length;
    $('#totalPatientsCard').html(_totalPatients);
    $('#totalPatientsChart').html(_totalPatients);
    const startDate = moment().subtract(6,'day')
    const endDate = moment();
    const _filteredData = _patients.filter(_p => moment(_p?.created_at).isBetween(startDate,endDate));
    let _daysActive = [];
    let _daysInactive = [];
    let _daysLabel = [];
    let _daysGrowth = [];
    for (var m = moment(startDate); m.isBefore(endDate); m.add(1, 'days')) {
      _daysActive.push({x:m.format('YYYY-MM-DD'),y:0});
      _daysInactive.push({x:m.format('YYYY-MM-DD'),y:0});
      _daysGrowth[m.format('YYYY-MM-DD')] = 0;
      _daysLabel.push(m.format('YYYY-MM-DD'));
  } ;
    _filteredData.forEach(_f => {
      let _dt = moment(_f?.created_at).format('YYYY-MM-DD');
      _daysGrowth[_dt] += 1;
      if(_f?.is_active == 'ACTIVE'){
        const _day = _daysActive.filter(_d => _d.x == _dt)[0];
        _day.y += 1;
        _daysActive[_daysActive.findIndex(_d => _d.x === _day.x)] = _day
      }else{
        const _day = _daysInactive.filter(_d => _d.x == _dt)[0];
        _day.y += 1;
        _daysInactive[_daysInactive.findIndex(_d => _d.x === _day.x)] = _day
      }
    });

    _percentage_growth = (((_totalPatients+_daysGrowth[endDate.format('YYYY-MM-DD')])-(_totalPatients+_daysGrowth[startDate.format('YYYY-MM-DD')]))/(_totalPatients+_daysGrowth[startDate.format('YYYY-MM-DD')]))*100;
    const growth_content = `
    <span class="${_percentage_growth > 0 ? 'text-success' : 'text-danger'}">
    <i class="fas ${_percentage_growth > 0 ? 'fa-arrow-up' : 'fa-arrow-down'}"></i> ${_percentage_growth.toFixed(2)}%
  </span>
  <span class="text-muted">Since last week</span>
    `;
    $('#patientGrowth').html(growth_content);


    var patientChartData = {
      labels  : _daysLabel,
      datasets: [
        {
          label               : 'Active',
          backgroundColor     : 'rgba(60,141,188,0.9)',
          borderColor         : 'rgba(60,141,188,0.8)',
          pointRadius          : false,
          pointColor          : '#3b8bba',
          pointStrokeColor    : 'rgba(60,141,188,1)',
          pointHighlightFill  : '#fff',
          pointHighlightStroke: 'rgba(60,141,188,1)',
          // data                : [28, 48, 40, 19, 86, 27, 90]
          data                : _daysActive
        },
        {
          label               : 'Inactive',
          backgroundColor     : 'rgba(210, 214, 222, 1)',
          borderColor         : 'rgba(210, 214, 222, 1)',
          pointRadius         : false,
          pointColor          : 'rgba(210, 214, 222, 1)',
          pointStrokeColor    : '#c1c7d1',
          pointHighlightFill  : '#fff',
          pointHighlightStroke: 'rgba(220,220,220,1)',
          // data                : [65, 59, 80, 81, 56, 55, 40]
          data                : _daysInactive
        },
      ]
    }

    var patientChartOptions = {
      maintainAspectRatio : false,
      responsive : true,
      legend: {
        display: false
      },
      scales:{
        x: {
          type: 'time',
          time: {
            unit: 'day'
          }
        },
        y: {
          beginAtZero: true
        }
      }
      // scales: {
      //   xAxes: [{
      //     gridLines : {
      //       display : false,
      //     }
      //   }],
      //   yAxes: [{
      //     gridLines : {
      //       display : false,
      //     }
      //   }]
      // }
    }

    var _patientChartCanvas = $('#chartPatients').get(0).getContext('2d')
    var _patientChartOptions = $.extend(true, {}, patientChartOptions)
    var _patientChartData = $.extend(true, {}, patientChartData)
    _patientChartData.datasets[0].fill = false;
    _patientChartData.datasets[1].fill = false;
    _patientChartOptions.datasetFill = false

    new Chart(_patientChartCanvas, {
      type: 'line',
      data: _patientChartData,
      options: _patientChartOptions
    })


}
)();




  //- LabRequest Types Table

(async () => {
    let template = ``;
    let _lab_test_types = await ajaxGet("lab_test_type");

    top_20_lab_test_types = _lab_test_types.slice(0, 26);

    top_20_lab_test_types.forEach((_lab_test_type) => {
if(_lab_test_type?.lab_test_type_name != 'CT-Scan'){


      template += `
		<tr>
			<td>${_lab_test_type?.lab_test_type_name}</td>
			<td>${_lab_test_type?.lab_service_name[0]?.lab_service_name}</td>
			<td>${_lab_test_type?.lab_service_name[0]?.status}</td>
		</tr>
		`;
}
    });

    $("#tableLabTestTypes").html(template);
  }
)();





  //- Latest Transaction Table
(async () => {
    let template = ``;
    let _lab_requests = await ajaxGet("lab_request");

    sorted_transactions = _lab_requests.sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );
    top_20_latest_transactions = sorted_transactions.slice(0, 20);

    top_20_latest_transactions.forEach((_transaction) => {

      const patient =
        _transaction?.inpatient == null
          ? _transaction.outpatient
          : _transaction.inpatient;
      const patient_name = `${patient.last_name}, ${patient.first_name} ${
        patient.middle_name || ""
      } ${patient.suffix_name ? ", " + patient.suffix_name : ""}`;

      template += `
		<tr>
			<td>${_transaction?.lab_request_no}</td>
			<td>${_transaction?.lab_service_name?.lab_service_name}</td>
			<td>${patient_name}</td>
			<td>${_transaction?.status}</td>
			<td>${moment(_transaction?.created_at).format("DD-MM-YYYY hh:mm:ss")}</td>
		</tr>
		`;
    });

    $("#tableLabRequestTypes").html(template);
    $("#tableLabRequestTransactions").html(template);
  }
)();
