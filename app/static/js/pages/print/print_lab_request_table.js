window.PrintLabRequestTable = (data) => {
let content = `


<div class="header" style="text-align:center;" >


    	<h6> <font color="green" style="font-size:36px;"> HoMIES </font> <br><u>
MEDICAL CENTER</u></h6>
	<p style="font-size: 14px;"> Don Fabian, Quezon City, Metro Manila <br>Tel: 6969-00000   Phone: 09696969690 <br> homiesmedical@gmail.com <br>
<u>                                                                                                                                                                                             </u></p>

</div>
<h6 style="text-align:center;"><em>LABORATORY REQUEST TRANSACTIONS</em></h6>


<table class="table table-bordered table-hover" style="width:100%;margin:0 auto;">
  <thead>
    <tr>
      <th>${data.header[0]}</th>
      <th>${data.header[1]}</th>
      <th>${data.header[2]}</th>
      <th>${data.header[3]}</th>
    </tr>
  </thead>
  <tbody>
`;

data.body.forEach(_data => {
  content += `
  <tr>
    <td>${_data[0]}</td>
    <td>${_data[1]}</td>
    <td>${_data[2]}</td>
    <td>${_data[3]}</td>
  </tr>
  `;
});

content+=`
  </tbody>
</table>

`;
  

  let val = htmlToPdfmake(content);

  let dd = {
    /*footer: 

	function(currentPage, pageCount) {return currentPage.toString() + ' of ' + pageCount; 
   
    // you can apply any logic and return any valid pdfmake element

    return [
      { canvas: [ { type: 'rect', x: 170, y: 32, w: pageSize.width - 170, ': 40 } ]  }
    ]
  },
*/

    footer: {
      text: "\n HoMIES MEDICAL CENTER \n 2022",
      alignment: "center",
      fontSize: 9,
    },

    watermark: { text: "HoMIES", color: "gray", opacity: 0.15, bold: true },

    content: val,
  };

  pdfMake.createPdf(dd).open();
};
