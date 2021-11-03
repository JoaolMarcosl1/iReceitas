function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(arquivo) {
            $('#previa_perfil').css('background-image', 'url('+arquivo.target.result +')');
            $('#previa_perfil').hide();
            $('#previa_perfil').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#envioFoto").change(function() {
    readURL(this);
});