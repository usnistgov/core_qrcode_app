/*
* Waits for Jquery to be ready
* Load RandR terms on the search form
*/
var defer_load_qrcode = function(){
    $(document).ready(function() {
      var records_page = document.querySelectorAll('#results');
      if (records_page !== null && records_page.length > 0) {
        records_page[0].innerHTML = "<div id='qrcode-container' style='text-align: center; display: none;'><img class='' src='' id='qrcode-image'></img></br><a id='qrcode-details' href='' class='btn btn-primary' role='button'><i class='fa fa-eye'></i> Details</a> <a id='qrcode-print' class='btn btn-primary' role='button'><i class='fa fa-print'></i> Print</a></div>" + records_page[0].innerHTML;

        var records = document.querySelectorAll('.result-title');

        records.forEach(function(record)
          {
            var link = record.querySelector('a');
            link.id = link.href.split("id=")[1];
            link.removeAttribute("href");

            link.onclick = function(ev)
            {
              var qrcode_container = document.getElementById('qrcode-container');
              if (qrcode_container.style.display === "none") {
                qrcode_container.style.display = "block";
              }

              var target = $(ev.target);
              var record_id = target.attr('id');

              var url = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
              document.getElementById('qrcode-image').src='http://127.0.0.1:8000/core_qrcode_app/gen_code?record='+url+'/data?id='+record_id;
              document.getElementById('qrcode-details').href=url+'/data?id='+record_id;
              document.getElementById('qrcode-details').target="_blank";

              document.getElementById('qrcode-print').onclick = function(ev)
              {
                var popup;

                function closePrint () {
                    if ( popup ) {
                        popup.close();
                    }
                }

                popup = window.open( document.getElementById('qrcode-image').src );
                popup.onbeforeunload = closePrint;
                popup.onafterprint = closePrint;
                popup.focus(); // Required for IE
                popup.print();

              };
            };
          }
        );
      }
    });
};

// Waiting JQuery
onjQueryReady(defer_load_qrcode);
