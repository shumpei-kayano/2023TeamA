function updateCartDisplay(cartItems) {
    // ここで cartItems を使用してカートの表示を更新する
    /*サーバーから返された新しいカートアイテムのデータを使用して
    カートの表示を更新するためのものです。
    この関数の具体的な実装は、カートの表示方法によります。
    たとえば、商品の数量や小計を表示するHTML要素を選択し、
    そのテキスト内容を新しい値に更新することができます。*/
    console.log(cartItems);  // デバッグ：カートアイテムのデータをログに出力
    var total = 0;
    var total_100 = 0;
    for (var i = 0; i < cartItems.length; i++) {
        var cartItem = cartItems[i];
        var row = $('input[data-pk="' + cartItem.pk + '"]').closest('tr');
        row.find('.cnt').val(cartItem.quantity);
        var quantity = parseInt(row.find('.cnt').val(), 10);
        var quantity = parseInt(row.find('.cnt').val(), 10);
        var salePriceText = row.find('.sale_price').text();
        console.log('salePriceText:', salePriceText);  // デバッグ出力
        var salePrice = parseFloat(salePriceText.replace(/[^0-9\.]/g, ''));
        console.log('quantity:', quantity);  // デバッグ出力
        console.log('salePrice:', salePrice);  // デバッグ出力
        var totalPrice = quantity * salePrice;
        var totalPriceElement = row.find('.total_price');
        totalPriceElement.text(totalPrice);
        // console.log(row);
        
        // console.log(totalPriceElement);  // デバッグ：小計要素をログに出力
        
        total += totalPrice;
        total_100 = total + 100;
        //row.find('.sale').text(cartItem.sale);
        //row.find('.sale_image').attr('src',cartItem.sale_image);
        row.find('.cnt').val(cartItem.quantity);
        //row.find('.total_price').text(cartItem.total_price);
        //total += cartItem.total_price;
    }
    $('.cart__total .total span').text(total + '円');
    $('.cart__total .total_100 span').text(total_100 + '円');
}
// 数量が変更されたときに小計を更新する
// $('.cnt').on('change', function() {
//     updateCartDisplay(cartItems);
// });


$(".increase-quantity, .decrease-quantity").click(function() {
    console.log('Button clicked');  // デバッグ：ボタンがクリックされたときにログを出力
    var pk = $(this).data('pk');
    var quantity = $(this).hasClass('increase-quantity') ? 1 : -1;
    var stock = $('input[data-pk="' + pk + '"]').data('stock');  // 在庫数を取得

    // // 数量を更新
    // var currentQuantity = $('input[data-pk="' + pk + '"]').val();
    // var newQuantity = currentQuantity + quantity;
    // $('input[data-pk="' + pk + '"]').val(newQuantity);

    // // 小計を更新
    // var row = $('input[data-pk="' + pk + '"]').closest('tr');
    // var salePriceText = row.find('.sale_price').text();
    // var salePrice = parseFloat(salePriceText.replace(/[^0-9\.]/g, ''));
    // var totalPrice = newQuantity * salePrice;
    // row.find('.total_price').text(totalPrice);

    if ($(this).hasClass('increase-quantity')) {
        var currentQuantity = $('input[data-pk="' + pk + '"]').val();
        if (currentQuantity >= Math.min(10, stock)) {  // 在庫数と10のうち小さい方を上限とする
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
        // updateCartDisplay(cartItems);
        // 数量が変更されたときに小計を更新する
    // $('.cnt').on('change', function() {
    //     updateCartDisplay(cartItems);
    // });
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Request failed: ' + textStatus + ', ' + errorThrown);  // デバッグ：リクエスト失敗時のログ出力
    });
});


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