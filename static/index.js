$(function () {
  //alert("Ucitana stranica!");
  //console.log('1');

  $('#btnSend').on('click', function (e) {
    //alert('kliknuto na btnSend');

    //forma se nije poslala klasicno
    e.preventDefault();

    var $country = $('#group1 :checked');
    var $category = $('#group2 :checked');

    var package = {
      country: $country.val(),
      category: $category.val()
    };

    //alert(JSON.stringify(package));

    //sada ove podatke treba poslati jednim ajax POST metodom serveru
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000',
      data: JSON.stringify(package),
      contentType: "json",
      success: function(){
        //alert('poslato');
        //location.reload();
      },
      error: function(){
        alert('greska');
      }
    });

  });

  $("p").click(function () {
    $(this).hide();
  });
});