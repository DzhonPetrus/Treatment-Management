window.PrintTreatment = () => {
  let Treatment = JSON.parse(localStorage.getItem('PrintTreatment'));
  const {
    patient_name,
    gender,
    age,
    birth_date,
    blood_type,
    contact_no,
    email,
    is_active,
    comments,
    diagnosis,
    prev_diagnosis,
    prev_surgeries,
    prev_treatments,
    treatment_no,
    treatment_service,
    treatment_type,
    treatment_description,
    physician_name,
    next_schedule,
    dose,
    drug,
    session_datetime,
    session_no,
    status,
  } = Treatment;
  let val = htmlToPdfmake(`

<div class="header" style="text-align:center;" >


    	<h6> <font color="green" style="font-size:36px;"> HoMIES </font> <br><u>
MEDICAL CENTER</u></h6>
	<p style="font-size: 14px;"> Don Fabian, Quezon City, Metro Manila <br>Tel: 6969-00000   Phone: 09696969690 <br> homiesmedical@gmail.com <br>
<u>                                                                                                                                                                                             </u></p>

</div>
<h6 style="text-align:center;"><em>TREATMENT DEPARTMENT</em></h6>


<div class="patient">
<h6 style="font-size: 18px;"> Patient Information</h6>
<table style="font-size: 16px;">
<tr>
<td style="background-color:#BFEEB7;">Name:</td>
<td>${patient_name}</td>
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
<td style="background-color:#BFEEB7;"> Diagnosis: </td>
<td>${diagnosis}</td>
<td style="background-color:#BFEEB7;">Previous Diagnosis:</td>
<td>${prev_diagnosis}</td>
</tr>



<tr>
<td style="background-color:#BFEEB7;">Previous Treatments:</td>
<td>${prev_treatments}</td>
<td style="background-color:#BFEEB7;"> Previous Surgeries: </td>
<td>${prev_surgeries}</td>
<td style="background-color:#BFEEB7;"> Status: </td>
<td>${is_active}</td>
</tr>

</table>
</div>
<br>
<p> ============================================================================== </p>
<br>
<div class="treatment">
<h6 style="font-size: 18px;"> Treatment Information</h6>
<table style="font-size: 16px;">
<tr>
<td style="background-color:#BFEEB7;">Treatment No.:</td>
<td>${treatment_no}</td>
<td style="background-color:#BFEEB7;"> Treatment Type: </td>
<td>${treatment_type}</td>
</tr>

<tr>

<td style="background-color:#BFEEB7;"> Treatment Service: </td>
<td>${treatment_service}</td>
<td style="background-color:#BFEEB7;"> Treatment Description </td>
<td>${treatment_description}</td>
</tr>


<tr>
<td style="background-color:#BFEEB7;"> Session No.: </td>
<td>${session_no}</td>
<td style="background-color:#BFEEB7;"> Session Date/Time: </td>
<td>${session_datetime == 'Invalid date' ? '<i>No data</i>' : session_datetime}</td>
</tr>



<tr>

<td style="background-color:#BFEEB7;"> Drug: </td>
<td>${drug}</td>
<td style="background-color:#BFEEB7;"> Dose: </td>
<td>${dose}</td>

</tr>

<tr>
<td style="background-color:#BFEEB7;"> Next Schedule: </td>
<td>${next_schedule == 'Invalid date' ? '<i>Not yet scheduled</i>' : next_schedule}</td>
<td style="background-color:#BFEEB7;"> Status: </td>
<td>${status}</td>
</tr>

<tr>
<td style="background-color:#BFEEB7;"> Physician: </td>
<td>${physician_name}</td>

<td style="background-color:#BFEEB7;"> Comments: </td>
<td>${comments}</td>

</tr>


</table>
</div>
<br>
<p> ============================================================================== </p>
<br>

</div>


    `);

  let dd = {
footer: 
          { text:'\n HoMIES MEDICAL CENTER \n 2022', alignment: 'center', fontSize: 9} ,
watermark: { text: 'HoMIES', color: 'gray', opacity: 0.15, bold: true},


    content: val,
  };

  pdfMake.createPdf(dd).open();
};
