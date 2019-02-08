$('.short-url').click(function () {
    $(this).select();
});

$('button.btn-copy').click(function () {
    var $temp = $("<input>");
    var $text = $('.short-url').text();
    $("body").append($temp);
    $temp.val($text).select();
    document.execCommand("copy");
    $temp.remove();

    alert("Copied the text: " + $text);
});