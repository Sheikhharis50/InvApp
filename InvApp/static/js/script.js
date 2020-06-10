setTimeout(function () {
    $('#message').fadeOut('slow');
}, 2000)
$(function () {
    var state = $('#state').val();
    var city = $('#city').val();
    if (typeof state !== 'undefined' && typeof city !== 'undefined'){
        if (state.length == 0 || state=='None'){
            $(".state").append("<option value='' selected disabled>Select a State</option>")
        }
        if (city.length == 0 || city=='None') {
            $(".city").append("<option value='' selected disabled>Select a City</option>")
        }
    }
    var password_check = $(".password_check").val()
    if (typeof password_check !== 'undefined'){
        if (password_check.search('Add')!=-1){
            $(".password").prop('required', true);
            $(".c_password").prop('required', true);
        }
        if (password_check.search('Update') != -1) {
            $(".password").attr('placeholder', 'Leave empty if do not want to update');
            $(".c_password").attr('placeholder', 'Leave empty if do not want to update');
        }
    }
    $("#example1").DataTable({
        "responsive": true,
        "autoWidth": false,
    });
    $('#example2').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
    });
});
$(".myaccordion1").click(function () {
    if($("#collps_icon1").attr('class').search('fa-plus')>0){
        $("#collps_icon1").removeClass('fa-plus').addClass("fa-minus");
    }
    else if ($("#collps_icon1").attr('class').search('fa-minus') > 0){
        $("#collps_icon1").removeClass('fa-minus').addClass("fa-plus");
    }
});
$(".myaccordion2").click(function () {
    if ($("#collps_icon2").attr('class').search('fa-plus') > 0) {
        $("#collps_icon2").removeClass('fa-plus').addClass("fa-minus");
    }
    else if ($("#collps_icon2").attr('class').search('fa-minus') > 0) {
        $("#collps_icon2").removeClass('fa-minus').addClass("fa-plus");
    }
});
$(document).ready(function () {
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');
});
$(function () {
    //Initialize Select2 Elements
    $('.select2').select2()

    //Initialize Select2 Elements
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })

    //Datemask dd/mm/yyyy
    $('#datemask').inputmask('dd/mm/yyyy', { 'placeholder': 'dd/mm/yyyy' })
    //Datemask2 mm/dd/yyyy
    $('#datemask2').inputmask('mm/dd/yyyy', { 'placeholder': 'mm/dd/yyyy' })
    //Money Euro
    $('[data-mask]').inputmask()

    //Date range picker
    $('#reservation').daterangepicker()
    //Date range picker with time picker
    $('#reservationtime').daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        locale: {
            format: 'MM/DD/YYYY hh:mm A'
        }
    })
    //Date range as a button
    $('#daterange-btn').daterangepicker(
        {
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            startDate: moment().subtract(29, 'days'),
            endDate: moment()
        },
        function (start, end) {
            $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))
        }
    )

    //Timepicker
    $('#timepicker').datetimepicker({
        format: 'LT'
    })

    //Bootstrap Duallistbox
    $('.duallistbox').bootstrapDualListbox()

    //Colorpicker
    // $('.my-colorpicker1').colorpicker()
    //color picker with addon
    // $('.my-colorpicker2').colorpicker()

    $('.my-colorpicker2').on('colorpickerChange', function (event) {
        $('.my-colorpicker2 .fa-square').css('color', event.color.toString());
    });

    $("input[data-bootstrap-switch]").each(function () {
        $(this).bootstrapSwitch('state', $(this).prop('checked'));
    });

})
$(document).ready(function () {
    var date_input = $('input[name="date"]'); //our date input has the name "date"
    var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
    var options = {
        format: 'mm/dd/yyyy',
        container: container,
        todayHighlight: true,
        autoclose: true,
    };
    date_input.datepicker(options);
    $("#clear").hide()
})
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#temp_img').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#temp_img").click(function () {
    $("input[id='up_item_img']").click();
});
$("#up_item_img").change(function () {
    readURL(this);
});
// ++++++++++ Popup Functionaility ++++++++++++++
function openWindow(url, nme) {
    'use strict';
    var w = (window.innerWidth / 2) + (window.innerWidth / 4);
    var h = (window.innerHeight / 2) + (window.innerHeight / 4);
    // let params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
    // width=50,height=50,left=100,top=100`;
    let params = `status=no,location=no,toolbar=no,menubar=no,
            width=`+ w + `,height=` + (h) + `,left=100,top=100`;

    open(url, nme, params);
}
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ++++++++++++ populate new data in dropdowns  ++++++++++++++
$(".form-ajax").submit(function (e) {
    e.preventDefault();
    var data = $(this).serialize();
    var url = $(this).attr("action");

    //  check wether the imp-fields are empty or not
    var nonempty = $('.imp-field').filter(function () {
        return this.value != ''
    });
    if (nonempty.length == 0) {
        $(".imp-field").prop('required', true);
        return false;
    }

    // +++++++++++++ Toast setup +++++++++++++++
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
    });

    $.ajax({
        //url: 'http://' + window.location.hostname + ':' + window.location.port + "/inventory/getcategories/",
        method: "POST",
        data: data,
        url: url,
        dataType: 'json',
        /*type: 'POST',
        contentType: false,
        headers: { "X-CSRFToken": data[0].value },*/
        success: function (response) {
            // console.log(response);
            if ('results' in response) {
                if (response['status'] == 'categories' || response['status'] == 'warehouses' || 
                    response['status'] == 'departments' || response['status'] == 'brands' || 
                    response['status'] == 'manufacturers' || response['status'] == 'units' || 
                    response['status'] == 'subcategories'){
                    populatesimilar(response);
                }
                else if (response['status'] == 'taxes') {
                    populateTaxes(response);
                }

                $('.modal').modal('hide')

                Toast.fire({
                    icon: 'success',
                    title: '&nbsp&nbsp'+response['message']
                })
            }
            else {
                Toast.fire({
                    icon: 'error',
                    title: '&nbsp&nbsp' + response['message']
                })
            }
        },
        error: function (e) {
            Toast.fire({
                icon: 'error',
                title: '&nbsp&nbsp' +"Server is not responding"
            })
            console.log("error");
            console.log(e);
        }
    });
});
function populatesimilar(response){
    var len = response['results'].length;
    $("." + response['status']).empty();
    $("." + response['status']).append("<option value='' selected='selected' disabled>" + response['selected'] + "</option>");
    for (var i = 0; i < len; i++) {
        var id = response['results'][i]['id'];
        var name = response['results'][i]['name']

        $("." + response['status']).append("<option value='" + id + "'>" + name + "</option>");
    }
}
function populateTaxes(response) {
    var len = response['results'].length;
    $("#" + response['status']).empty();
    $("#" + response['status']).append("<option value='' selected='selected' disabled>" + response['selected'] + "</option>");
    for (var i = 0; i < len; i++) {
        var id = response['results'][i]['id'];
        var name = response['results'][i]['name'];
        var percentage = response['results'][i]['percentage'];


        $("#" + response['status']).append("<option value='" + id + "'>" + name + ", " + percentage + "%</option>");
    }
}
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ++++++++++++ CRUD operations for item in forms ++++++++++++
// add item functionaility
$("#add_item").click(function(){
    // get selected item
    var selected_text;
    var selected_value;
    var index = parseInt($("input[name='items_count']").val());
    $(".items option:selected").each(function () {
        selected_text = $(this).text();
        selected_value = $(this).val();
    });
    // +++++++++++++ Toast setup +++++++++++++++
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
    });
    
    if (!selected_value){
        Toast.fire({
            icon: 'error',
            title: '&nbsp&nbsp' + "Select Item from Dropdown!"
        })
        return
    }
    var stock = $('.stock').val();
    if (typeof stock !== 'undefined' && stock.length <= 0){
        Toast.fire({
            icon: 'error',
            title: '&nbsp&nbsp' + "Provide stock value!"
        })
        return
    }
    var found = false;
    $(".items_container tr").each(function () {
        var $tds = $(this).find('td');
        if ($tds.eq(1).text().toString() == selected_text.toString()) {
            Toast.fire({
                icon: 'error',
                title: '&nbsp&nbsp' + 'Item ' + selected_text + ' is already selected!'
            });
            found = true;
            return false;
        }
    });

    if(!found){
        var row = 
            '<tr>'+
                '<td>' + (index+1) + '</td>'+
                '<td>' + selected_text +'</td>';
                
        if (typeof stock !== 'undefined' && stock.length > 0) {
            row += 
            '<td>'+
                '<span>' + stock + '</span>'+
                '<input id="stock" type="hidden" value="' + stock + '" name="stock' + index + '"/>'+
            '</td>';
        }
        else{
            row += '<td><input type="checkbox" checked name="is_available' + index + '"></td>';
        }
        row += 
                '<td style="text-align: center;">'+
                    '<a type="button" onclick=view_item(' + selected_value + ')>'+
                        '<i class="fa fa-eye"></i>'+
                    '</a>'+
                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                    '<a type="button" onclick=delete_item(' + (index+1) + ')>'+
                        '<i class="fa fa-trash"></i>'+
                    '</a>'+
                '</td>'+
                '<input type="hidden" name="item' + index + '" value="' + selected_value + '"/>'+
            '</tr>';
        
        
        index += 1;
        $("input[name='items_count']").val(index);
        $(".items_container").append(row);
    }

});
// delete item functionailty
function delete_item(index){
    $(".items_container tr").each(function () {
        var $tds = $(this).find('td');
        if ($tds.eq(0).text() == index){
            $(this).remove();
        }
    });
}
// view item from dropdown functionaility 
$("#view_item").click(function(){
    var selected_value;
    $(".items option:selected").each(function () {
        selected_value = $(this).val();
    });
    // +++++++++++++ Toast setup +++++++++++++++
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
    });

    if (!selected_value) {
        Toast.fire({
            icon: 'error',
            title: '&nbsp&nbsp' + "Select Item from Dropdown First!"
        })
        return
    }

    url = 'http://' + window.location.hostname + ':' + window.location.port + "/inventory/item/item_partial_detail/" + selected_value + "/";
    openWindow(url, 'Item Detail');

});
// view item from table functionaility 
function view_item(id) {
    url = 'http://' + window.location.hostname + ':' + window.location.port + "/inventory/item/item_partial_detail/" + id + "/";
    openWindow(url, 'Item Detail');
}
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
