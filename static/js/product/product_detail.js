$(document).ready(function () {
    
    // Butona tıklama olayı
    $('.product-btn').click(function (e) {
        e.preventDefault(); // Formun otomatik olarak gönderilmesini engelle

        var productId = $(this).data('product-id'); // Ürün ID'sini al
        var productName = $(this).closest('.product-card').find('.breadcrumb-item[data-product-name]').data('product-name'); // Ürün adını al

        // AJAX isteği gönder
        $.ajax({
            type: 'POST',
            url: '{% url "basket:add_to_basket" 0 %}'.replace('0', productId), // URL'yi güncelle
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}' // CSRF token ekle
            },
            success: function (response) {
                // Başarılı yanıt geldiğinde popup göster
                displayAlertPopup('Ürün sepete eklendi'  +"<br>"+ productName); // Popup mesajı
            },
            error: function (xhr, status, error) {
                $('#message').text('Bir hata oluştu: ' + error); // Hata mesajı göster
            }
        });
    });

    function displayAlertPopup(message) {
        // Özel bir uyarı popup'ı oluştur
        var popup = $('<div class="custom-popup bg-danger text-coffee text-uppercase">' + message + '<i class="bi bi-check2-circle"></i></div>');
        
        // Popup'ı body'e ekle
        $('body').append(popup);
        
        // Popup'ı göster
        popup.fadeIn();
        
        // 2 saniye sonra popup'ı gizle
        setTimeout(function() {
            popup.fadeOut(function() {
                // Fade out'dan sonra popup'ı DOM'dan kaldır
                $(this).remove();
            });
        }, 2000);
    }
});

