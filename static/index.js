var x = {}

function add_customer() {
    console.log('==========================')
    //$.ajax({url:"/customers"})
    customer = {
        first_name: $('#txt_fname').val(),
        last_name: $('#txt_lname').val(),
        address: $('#txt_address').val(),
        phone_number: $('#txt_phone').val(),
        credit_card_number: $('#txt_ccn').val(),
        user_id: $('#txt_user_id').val(),
        username: $('#txt_username').val(),
        password: $('#txt_password').val(),
        email: $('#txt_email').val()
    }
    console.log(customer)
    $.ajax({
            type: "POST",
            url: "/customers",
            data: JSON.stringify(customer),
            dataType: "JSON",
            contentType: 'application/json',
            success: function(data, status){
                console.log('status', status)
                console.log('data', data)
                get_all_customers(true)
            },
            error: function (xhr, desc, err) {
            }
            });

}
function get_customer_by_id() {
     $.ajax({url:"/customers/" + $('#txt_id_u').val()}).then(
      function(one_customer) // after-promise succeed
                {
                    console.log(one_customer)
                    $('#txt_fname_u').val(one_customer.first_name)
                    $('#txt_lname_u').val(one_customer.last_name)
                    $('#txt_address_u').val(one_customer.address)
                    $('#txt_phone_u').val(one_customer.phone_number)
                    $('#txt_ccn_u').val(one_customer.credit_card_number)
                });
}

function update_customer(id) {
    customer = {
        id: $('#txt_id_u').val(),
        first_name: $('#txt_fname_u').val(),
        last_name: $('#txt_lname_u').val(),
        address: $('#txt_address_u').val(),
        phone_number: $('#txt_phone_u').val(),
        credit_card_number: $('#txt_ccn_u').val()
    }
    $.ajax({
        type: "PATCH",
        url: "/customers/" + customer.id,
        data: JSON.stringify(customer),
        dataType: "JSON",
        contentType: 'application/json',
        success: function(data, status){
            console.log('status', status)
            console.log('data', data)
            get_all_customers(true)
        },
        error: function (xhr, desc, err) {
        }
        });
}

function delete_customer(id) {
    console.log(`send ajax to delete where customer id = ${id}`)

    $.ajax({
            type: "DELETE",
            url: "/customers/" + id,
            success: function(data, status){
                console.log('status', status)
                console.log('data', data)
                get_all_customers(false)
            },
            error: function (xhr, desc, err) {
            }
            });
}

function get_all_customers(draw_last_only) {
        var customers_table =  $("#customers"); //cache

        if (!draw_last_only)
            customers_table.find("tr:gt(0)").remove();

        $.ajax({url:"/customers"}).then(
                function(_customers) // after-promise succeed
                {
                x.result = _customers
                    console.log(_customers);
                    console.log(_customers[0])

                   $.each(_customers,  (i, customer) => {
                            if (!draw_last_only || i == _customers.length - 1) {
                                customers_table.append(
                                    `<tr><td>${customer.id}</td>
                                         <td>${customer.first_name}</td>
                                         <td>${customer.last_name}</td>
                                         <td>${customer.address}</td>
                                         <td>${customer.phone_number}</td>
                                         <td>${customer.credit_card_number}</td>
                                         <td>${customer.user_id}</td>
                                         <td><button style="color:red" onclick="delete_customer(${customer.id})">X</button></td></tr>`)
                                         };
                    })
                }
                ,function(err)   // after-promise failed
                {
                    console.log(err);}
                );
}

$(document).ready(function()
{
    $('#btn1').on('click', () => {

        get_all_customers(false);

    });
});