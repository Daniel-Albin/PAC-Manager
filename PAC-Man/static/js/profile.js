function generateQRCode() {
    var image = document.querySelector('.qr-code-image');
    if (image.style.display === 'none') {
        image.style.display = 'block';
    } else {
        image.style.display = 'none';
    }
}
