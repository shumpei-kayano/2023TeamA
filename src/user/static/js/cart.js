function updateCartDisplay(cartItems) {
    // ここで cartItems を使用してカートの表示を更新する
    /*サーバーから返された新しいカートアイテムのデータを使用して
    カートの表示を更新するためのものです。
    この関数の具体的な実装は、カートの表示方法によります。
    たとえば、商品の数量や小計を表示するHTML要素を選択し、
    そのテキスト内容を新しい値に更新することができます。*/
    var total = 0;
    var total_100 = 0;
    for (var i = 0; i < cartItems.length; i++) {
        var cartItem = cartItems[i];
        var row = $('input[data-pk="' + cartItem.pk + '"]').closest('tr');
        console.log(row);
        var totalPriceElement = row.find('.total_price');
        console.log(totalPriceElement);  // デバッグ：小計要素をログに出力
        totalPriceElement.text(cartItem.total_price);
        total += cartItem.total_price;
        total_100 += cartItem.total_price + 100;
        //row.find('.sale').text(cartItem.sale);
        //row.find('.sale_image').attr('src',cartItem.sale_image);
        row.find('.cnt').val(cartItem.quantity);
        //row.find('.total_price').text(cartItem.total_price);
        //total += cartItem.total_price;
    }
    $('.cart__total .total span').text(total + '円');
    $('.cart__total .total_100 span').text(total_100 + '円');
}

// $(".increase-quantity, .decrease-quantity").click(function() {
//     var pk = $(this).data('pk');
//     var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
//     $.post('/update_cart/', {pk: pk, quantity: quantity}, function(data) {
//         updateCartDisplay(data.cart_items);
//     });
// });
// $(".increase-quantity, .decrease-quantity").click(function() {
//     var pk = $(this).data('pk');
//     var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
//     var updateCartPromise = $.post('/update_cart/', {pk: pk, quantity: quantity});
//     updateCartPromise.then(function(data) {
//         updateCartDisplay(data.cart_items);
//     });
// });

// $(".increase-quantity, .decrease-quantity").click(function() {
//     var pk = $(this).data('pk');
//     var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
//     var updateCartPromise = $.post('/update_cart/', {pk: pk, quantity: quantity});
//     updateCartPromise.then(function(data) {
//         console.log(data);  // デバッグ：レスポンスデータをログに出力
//         updateCartDisplay(data.cart_items);
//     });
// });

// $(".increase-quantity, .decrease-quantity").click(function() {
//     var pk = $(this).data('pk');
//     var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
//     console.log('Sending request');  // デバッグ：リクエスト送信前にログ出力
//     var updateCartPromise = $.post('/update_cart/', {pk: pk, quantity: quantity});
//     updateCartPromise.then(function(data) {
//         console.log(data);  // デバッグ：レスポンスデータをログに出力
//         updateCartDisplay(data.cart_items);
//     });
// });

// $(".increase-quantity, .decrease-quantity").click(function() {
//     console.log('Button clicked');  // デバッグ：ボタンがクリックされたときにログを出力
//     var pk = $(this).data('pk');
//     var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
//     var updateCartPromise = $.post('/update_cart/', {pk: pk, quantity: quantity});
//     updateCartPromise.then(function(data) {
//         console.log(data);  // デバッグ：レスポンスデータをログに出力
//         updateCartDisplay(data.cart_items);
//     }).fail(function(jqXHR, textStatus, errorThrown) {
//         console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
//     });
// });

// $(".increase-quantity, .decrease-quantity").click(function() {
//     console.log('Button clicked');  // デバッグ：ボタンがクリックされたときにログを出力
//     var pk = $(this).data('pk');
//     var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
//     var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
//     $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     });
//     var updateCartPromise = $.post('/update_cart/', {pk: pk, quantity: quantity});
//     updateCartPromise.then(function(data) {
//         console.log(data);  // デバッグ：レスポンスデータをログに出力
//         updateCartDisplay(data.cart_items);
//     }).fail(function(jqXHR, textStatus, errorThrown) {
//         console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
//     });
// });

$(".increase-quantity, .decrease-quantity").click(function() {
    console.log('Button clicked');  // デバッグ：ボタンがクリックされたときにログを出力
    var pk = $(this).data('pk');
    var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;

    if ($(this).hasClass('increase-quantity')) {
        var currentQuantity = $('input[data-pk="' + pk + '"]').val();
        if (currentQuantity >= 10) {
            console.log('Cannot increase quantity above 10');  // デバッグ：数量を10以上にする操作を防ぐ
            return;  // 数量が10以上になる場合は、操作を中止
        }
    }
    // 数量を減らす操作を行う前に、現在の数量が1以上であることを確認
    if ($(this).hasClass('decrease-quantity')) {
        var currentQuantity = $('input[data-pk="' + pk + '"]').val();
        if (currentQuantity <= 1) {
            console.log('Cannot decrease quantity below 1');  // デバッグ：数量を1以下にする操作を防ぐ
            return;  // 数量が1以下になる場合は、操作を中止
        }
    }

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    var updateCartPromise = $.post('/update_cart/', {pk: pk, quantity: quantity});
    updateCartPromise.then(function(data) {
        console.log(data);  // デバッグ：レスポンスデータをログに出力
        updateCartDisplay(data.cart_items);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
    });
});
// $(".delete-quantity").click(function() {
//     console.log('Delete button clicked');  // デバッグ：削除ボタンがクリックされたときにログを出力
//     var pk = $(this).data('pk');

//     var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
//     $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     });
//     var deleteItemPromise = $.post('/delete_item/', {pk: pk});
//     deleteItemPromise.then(function(data) {
//         console.log(data);  // デバッグ：レスポンスデータをログに出力
//         updateCartDisplay(data.cart_items);
//     }).fail(function(jqXHR, textStatus, errorThrown) {
//         console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
//     });
// });

// $(".delete-quantity").click(function() {
//     var pk = $(this).data('pk');  // data-pk属性からpkを取得

//     $.ajax({
//         url: '/delete_item/',  // 適切なエンドポイントに変更してください
//         type: 'POST',
//         data: {
//             'pk': pk,  // pkをPOSTデータとして送信
//             'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
//         },
//         dataType: 'json',
//         success: function (data) {
//             // 成功時の処理
//         }
//     });
// });

// $(".delete-quantity").click(function() {
//     console.log('Delete button clicked');  // デバッグ：削除ボタンがクリックされたときにログを出力
//     var pk = $(this).data('pk');
//     console.log('pk: ' + pk);  // デバッグ：pkの値をログに出力

//     var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
//     $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     });
//     var deleteItemPromise = $.post('/delete_item/', {pk: pk});
//     deleteItemPromise.then(function(data) {
//         console.log(data);  // デバッグ：レスポンスデータをログに出力
//         updateCartDisplay(data.cart_items);
//     }).fail(function(jqXHR, textStatus, errorThrown) {
//         console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
//     });
// });

$(".delete-quantity").click(function(e) {
    //e.preventDefault();  // フォームのデフォルトの送信動作をキャンセル
    console.log('Delete button clicked');  // デバッグ：削除ボタンがクリックされたときにログを出力
    var pk = $(this).attr('data-pk');  // attrメソッドを使用してdata-pk属性の値を取得
    console.log('pk: ' + pk);  // デバッグ：pkの値をログに出力

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    var deleteItemPromise = $.post('/delete_item/', {pk: pk});
    deleteItemPromise.then(function(data) {
        console.log(data);  // デバッグ：レスポンスデータをログに出力
        updateCartDisplay(data.cart_items);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
    });
});