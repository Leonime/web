$(document).on("click", ".OpenModal", function () {
    const ImageDisplay = $(this).data('image');
    $("#ModalImageLink").attr("href", ImageDisplay);
    $("#ImageDisplay").attr("src", ImageDisplay);
});