window.PrintLabRequest = () => {
  let LabRequest = JSON.parse(localStorage.getItem('PrintLabRequest'));
  let val = htmlToPdfmake(`

    <div class="header" style="text-align:center;" >


            <h6 style="font-size:20px";> <font color="green"> HoMIES </font> <br><u>
    MEDICAL CENTER</u></h6>
        <p style="font-size: 9px;"> Don Fabian, Quezon City, Metro Manila <br>Tel: 6969-00000   Phone: 09696969690 <br> homiesmedical@gmail.com <br>
    <u>                                                                                                </u></p>

    </div>
    <h6 style="text-align:center;"><em>LABORATORY REQUEST</em></h6>


    <div class="lab-req">
    <table style="font-size: 12px;">
    <tr>
    <td style="background-color:#BFEEB7;">Name:</td>
    <td>${LabRequest.name}</td>
    <td style="background-color:#BFEEB7;"> Lab Request No. </td>
    <td>${LabRequest.request_number}</td>
    </tr>

    <tr>
    <td style="background-color:#BFEEB7;"> Lab Request Type: </td>
    <td>${LabRequest.request_type}</td>
    <td style="background-color:#BFEEB7;"> Lab Request Service: </td>
    <td>${LabRequest.request_service}</td>
    </tr>


    <tr>
    <td style="background-color:#BFEEB7;">Fee:</td>
    <td>${LabRequest.fee}</td>
    <td style="background-color:#BFEEB7;">Quantity:</td>
    <td>${LabRequest.quantity}</td>
    </tr>

    <tr>
    <td style="background-color:#BFEEB7;"> Date/Time: Requested </td>
    <td>${LabRequest.dt_requested}</td>
    <td style="background-color:#BFEEB7;"> Status: </td>
    <td>${LabRequest.status}</td>
    </tr>
    </table>
    </div>
    <br>
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
