$('#addtocartbtn').click(function (e) {
    e.preventDefault();

    let product_id = $(this).closest('.product_detail').find('.product_id').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        method: "POST",
        url: '/add-to-cart/',  // Make sure this URL is correct
        data: {
            'product_id': product_id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            console.log(response);
            if (response.status === "success") {
                location.reload();  // Reload the page after successful add to cart
            }
        },
        error: function (xhr, status, error) {
            console.log("AJAX Error: ", status, error);
        }
    });
});

$('.cart-increase-quantity').click(function (e) {
    e.preventDefault();

    let product_id = $(this).closest('tr').find('.cart_product_id').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();
    let current_product_quantity = $(this).closest('tr').find('.current-product-quantity').val();

    $.ajax({
        method: "POST",
        url: '/product-quantity-update/',
        data: {
            'product_id': product_id,
            'action': 'increase',
            'current_product_quantity': current_product_quantity,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            console.log(response);
            if (response.status === "success") {
                location.reload();  // Reload the page after successfully increasing quantity
            }
        },
        error: function (xhr, status, error) {
            console.log("AJAX Error: ", status, error);
        }
    });
});

$('.cart-decrease-quantity').click(function (e) {
    e.preventDefault();

    let product_id = $(this).closest('tr').find('.cart_product_id').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();
    let current_product_quantity = $(this).closest('tr').find('.current-product-quantity').val();

    $.ajax({
        method: "POST",
        url: '/product-quantity-update/',
        data: {
            'product_id': product_id,
            'action': 'decrease',
            'current_product_quantity': current_product_quantity,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            console.log(response);
            if (response.status === "success") {
                location.reload();  // Reload the page after successfully decreasing quantity
            }
        },
        error: function (xhr, status, error) {
            console.log("AJAX Error: ", status, error);
        }
    });
});
