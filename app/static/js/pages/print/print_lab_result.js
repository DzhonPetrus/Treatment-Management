window.PrintLabResult = () => {
  let LabResult = JSON.parse(localStorage.getItem('PrintLabResult'));
  const {
    name,
    gender,
    age,
    birth_date,
    blood_type,
    contact_no,
    email,
    is_active,
    lab_request_no,
    lab_result_no,
    lab_test,
    lab_type,
    ordered,
    reference,
    result,
    specimen,
    comments,
    lab_technician,
    initial_diagnosis,
    status,
    dt_requested,
    dt_received,
    dt_reported,
  } = LabResult;
  console.log(LabResult)
  let val = htmlToPdfmake(`
<div class="header" style="text-align:center;" >


    	<h6> <font color="green" style="font-size:36px;"> HoMIES </font> <br><u>
MEDICAL CENTER</u></h6>
	<p style="font-size: 14px;"> Don Fabian, Quezon City, Metro Manila <br>Tel: 6969-00000   Phone: 09696969690 <br> homiesmedical@gmail.com <br>
<u>                                                                                                                                                                                             </u></p>

</div>
<h6 style="text-align:center;"><em>LABORATORY DEPARTMENT</em></h6>


<div class="patient">
<h6 style="font-size: 18px;"> Patient Information</h6>
<table style="font-size: 16px;">
<tr>
<td style="background-color:#BFEEB7;">Name:</td>
<td>${name}</td>
<td style="background-color:#BFEEB7;"> Sex: </td>
<td>${gender}</td>
<td style="background-color:#BFEEB7;"> Age: </td>
<td>${age}</td>
</tr>

<tr>
<td style="background-color:#BFEEB7;"> Birthdate: </td>
<td>${birth_date}</td>
<td style="background-color:#BFEEB7;"> Blood Type: </td>
<td>${blood_type}</td>
<td style="background-color:#BFEEB7;">Contact No: </td>
<td>${contact_no}</td>
</tr>


<tr>
<td style="background-color:#BFEEB7;"> E-mail: </td>
<td>${email}</td>
<td style="background-color:#BFEEB7;"> Initial Diagnosis: </td>
<td>${initial_diagnosis}</td>
<td style="background-color:#BFEEB7;"> Status: </td>
<td>${is_active}</td>
</tr>

</table>
</div>
<br>
<p> ============================================================================== </p>
<br>
<div class="lab-results">
<h6 style="font-size: 18px;"> Laboratory Results</h6>
<table style="font-size: 16px;">
<tr>
<td style="background-color:#BFEEB7;">Lab Request No.:</td>
<td>${lab_request_no}</td>
<td style="background-color:#BFEEB7;"> Lab Result No.: </td>
<td>${lab_result_no}</td>
</tr>

<tr>

<td style="background-color:#BFEEB7;"> Specimen: </td>
<td>${specimen}</td>
<td style="background-color:#BFEEB7;"> Ordered: </td>
<td>${ordered}</td>
</tr>


<tr>
<td style="background-color:#BFEEB7;"> Date/Time Requested: </td>
<td>${dt_requested}</td>
<td style="background-color:#BFEEB7;"> Date/Time Received: </td>
<td>${dt_received == 'Invalid date' ? '<i>Not yet received</i>' : dt_received}</td>
</tr>



<tr>

<td style="background-color:#BFEEB7;"> Date/Time Reported: </td>
<td>${dt_reported == 'Invalid date' ? '<i>Not yet reported</i>' : dt_reported}</td>
<td style="background-color:#BFEEB7;"> Laboratory Technician: </td>
<td>${lab_technician}</td>

</tr>

<tr>
<td style="background-color:#BFEEB7;"> Comments: </td>
<td>${comments}</td>
<td style="background-color:#BFEEB7;"> Status: </td>
<td>${status}</td>
</tr>

</table>
<br>
<table style="font-size: 16px;">
<tr>
<td style="background-color:#BFEEB7;">Laboratory Types.:</td>
<td style="background-color:#BFEEB7;">Laboratory Tests.:</td>
<td style="background-color:#BFEEB7;"> Results: </td>
<td style="background-color:#BFEEB7;"> Reference Range: </td>
</tr>

<tr>
<td>${lab_type}</td>
<td>${lab_test}</td>
<td>${result}</td>
<td>${reference}</td>
</tr>
</table>
</div>
<br>
<p> ============================================================================== </p>
<br>

</div>


    `);

  let dd = {
    pageSize: "A6",
    pageOrientation: "landscape",

    watermark: { text: "HoMIES", color: "gray", opacity: 0.15, bold: true },

    content: val,
  };

  pdfMake.createPdf(dd).open();
};
