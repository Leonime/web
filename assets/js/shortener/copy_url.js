$('span.short-url').click(function () {
    $(this).select();
});

$('button.btn-copy').click(function () {
    var $temp = $("<input>");
    var short_url = $('span.short-url');
    short_url.select();
    var $text = short_url.text();
    $("body").append($temp);
    $temp.val($text).select();
    document.execCommand("copy");
    $temp.remove();

    alert("Copied the text: " + $text);
});