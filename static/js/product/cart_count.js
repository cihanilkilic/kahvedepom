function updateCartCount() {
    $.ajax({
        url: "{% url 'basket:get_cart_count' %}",
        method: "GET",
        success: function(data) {
            $('#cart-count').text(data.cart_count); // Sepet sayısını güncelle
        },
        error: function(error) {
            console.log("Error:", error);
        }
    });
}

$(document).ready(function() {
    // Sayfa yüklendiğinde sepet sayısını al
    updateCartCount();

    // Sepete ürün eklendiğinde bu fonksiyonu çağırın
    $('.add-to-cart').on('click', function() {
        // Sepete ürün ekleme işlemleri burada yapılmalı.
        // Ürün sepete eklendiğinde sepet sayısını güncelle
        updateCartCount();
    });
});