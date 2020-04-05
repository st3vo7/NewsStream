$(function () {
  //alert("Ucitana stranica!");
  //console.log('1');

  var obj;

  function izvuci_broj(data) {

    return data.split('_')[1];
  }

  $('#btnSources').on('click', function (e) {
    //alert('kliknuto na btnSauce');
    e.preventDefault();

    var $country = $('#group1 :checked');
    //alert($country.val());

    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/sources',
      data: JSON.stringify($country.val()),
      contentType: "json",
      success: data_ok_sources,
      error: function () {
        alert('greska');
      }
    });


  });




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

    /* $('#ajax_headlines_list').slideUp(300, function(){
      $(this).empty();
    }); */


    //sada ove podatke treba poslati jednim ajax POST metodom serveru
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000',
      data: JSON.stringify(package),
      contentType: "json",
      success: data_ok,
      error: function () {
        alert('greska');
      }
    });


    //ode ga umetni...................
  });

  function data_ok_sources(data) {


    var $list_for_sauces = $('#ajax_sauces_list');
    var $sauces_title = $('#sauces_title');

    obj = JSON.parse(data);
    console.log(obj);
    var sources = obj.sent.sources;
    console.log(sources);

    $list_for_sauces.hide(300, function(){
      $list_for_sauces.empty();
      $.each(sources, function(i,source){
        $list_for_sauces.append('<li id="list-sauce_'+i+'"><a class="naslov">'+source.name+'</a>:<p>'+source.description+'</p></li>');
      });
      $list_for_sauces.show(300);
    });

    $sauces_title.show(300);

  }


  function data_ok(data) {


    var $list_for_headlines = $('#ajax_headlines_list');
    var $headline_title = $('#ajax_title');
    //var $headlines_panel = $('#panel_top_headlines');

    //console.log(data);
    obj = JSON.parse(data);
    //console.log(obj);


    var articles = obj.sent.articles;

    $list_for_headlines.hide(300, function () {
      $list_for_headlines.empty();
      $.each(articles, function (i, article) {
        $list_for_headlines.append('<li id="list-title_' + i + '" class="listica"><a class="naslov">' + article.title + '<br></a></li>');
      });
      $list_for_headlines.show(300);
    });

    $headline_title.show(300);

  }
  //ode ga umetni......................

  $('#ajax_headlines_list').on('click', '.listica', function () {
    //alert($(this).closest('li')[0].id);

    var articles = obj.sent.articles;
    //alert(articles[0].title);
    console.log(articles);
    //console.log(articles[0].title);

    //var $id_kliknute = $(this).closest('li')[0].id
    //alert($id_kliknute);
    //$(this).fadeOut(500);
    $kliknuta_lista = $(this);

    //vest se vraca samo na naslov kada se klikne na drugu
    $kliknuta_lista.closest('li').siblings(".prosiren").slideUp(300, function () {
      var id_vesti = izvuci_broj($(this)[0].id);
      var tekst_koji_ostaje = articles[id_vesti].title;

      $(this).html('<a class="naslov">' + tekst_koji_ostaje + '<br></a>').slideDown(300);
      $(this).removeClass('prosiren');
    });

    if ($kliknuta_lista.attr("class").includes('prosiren')) {
      //to znaci da je vest otvorena i treba je zatvoriti
      //alert('kliknuo na otvorenu vest');
      $kliknuta_lista.closest('li').slideUp(300, function () {
        var id_vesti = izvuci_broj($(this)[0].id);
        var tekst_koji_ostaje = articles[id_vesti].title;

        $(this).html('<a class="naslov">' + tekst_koji_ostaje + '<br></a>').slideDown(300);
        $(this).removeClass('prosiren');
      });


    }

    else {

      //vest nije prosirena i treba je prosiriti
      $(this).slideUp(300, function () {
        //$kliknuta_lista.empty();
        $kliknuta_lista.addClass('prosiren');
        var id_vesti = izvuci_broj($kliknuta_lista[0].id);
        //alert(id_vesti);

        $(this).append('<div class="container"><img src="' + articles[id_vesti].urlToImage + '" class="img"</div>')
          .append('<p>' + articles[id_vesti].description + '</p>')
          .append('<a href="' + articles[id_vesti].url + '"target="_blank" class="zatamni"> Read more... </a>')
          .slideDown(300);
      });
    }

  });


});