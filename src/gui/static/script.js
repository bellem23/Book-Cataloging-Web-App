$( document ).ready(function() {
    var imgSource = $("#bookPic").val();
    $("#bookIMG").attr("src", imgSource);

    $( "#bookPic").on( "change", function() {
        var imgSource = $("#bookPic").val();
        $("#bookIMG").attr("src", imgSource);
      } );
});

