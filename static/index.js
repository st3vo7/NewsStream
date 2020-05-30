$(function () {
  //alert("Ucitana stranica!");
  //console.log('1');

  var obj;
  var initial_request;
  var errorSleepTime = 500;
  var sending_parameters;
  var tmp_list_url = [];



  function izvuci_broj(data) {

    return data.split('_')[1];
  }


  $('#btnSources').on('click', function (e) {
    //alert('kliknuto na btnSauce');
    e.preventDefault();

    var $country = $('#group1 :checked');
    //alert($country.val());
    var $category = $('#group2 :checked');
    //alert($category.val());

    var $language = $('#group3 :checked');
    //alert($language.val());

    var package = {
      country: $country.val()
    }

    if ($category.val()) {
      package.category = $category.val();
    }

    if ($category.val()) {
      package.language = $language.val();
    }

    package.initial_request = true;
    sending_parameters = package;



    /* 
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/sources',
      data: JSON.stringify(package),
      contentType: "json",
      success: data_ok_sources,
      error: function () {
        alert('greska');
      }
    }); */

    post_ajax('http://localhost:8000/sources', JSON.stringify(package), data_ok_sources, data_not_ok_sources)

  });





  $('#btnSend').on('click', function (e) {
    //alert('kliknuto na btnSend');

    //forma se nije poslala klasicno
    e.preventDefault();

    var package;



    var $country = $('#group1 :checked');
    var $category = $('#group2 :checked');
    var $keyword = $('#qsearch');
    //alert($keyword.val());


    if (!$category.val()) {

      if ($keyword.val()) {
        package = {
          country: $country.val(),
          category: 'general',
          keyword: $keyword.val()
        };

      }
      else {
        package = {
          country: $country.val(),
          category: 'general',
        };
      }
    }

    else {

      if ($keyword.val()) {
        package = {
          country: $country.val(),
          category: $category.val(),
          keyword: $keyword.val()
        };

      }

      else {
        package = {
          country: $country.val(),
          category: $category.val(),
        };
      }
    }

    package.initial_request = true;
    //da bih mogao da ga koristim ponovo u data_ok, jer package nije vidljiv van ove f-je
    sending_parameters = package;

    tmp_list_url = [];



    //alert(JSON.stringify(package));



    //sada ove podatke treba poslati jednim ajax POST metodom serveru

    /* $.ajax({
      type: 'POST',
      url: 'http://localhost:8000',
      data: JSON.stringify(package),
      contentType: "json",
      success: data_ok,
      error: function () {
        alert('greska');
      }
    }); */

    post_ajax('http://localhost:8000', JSON.stringify(package), data_ok, data_not_ok);

  });

  function check_if_not_in(word, text) {
    return !text.includes(word);
  }


  function post_ajax(url, data, success_function, failure_function) {

    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      contentType: "json",
      success: success_function,
      error: failure_function
    });

  }

  function data_ok(data) {

    var $list_for_headlines = $('#ajax_headlines_list');
    var $headline_title = $('#ajax_title');
    //var $headlines_panel = $('#panel_top_headlines');

    errorSleepTime = 500;

    //console.log(data);
    obj = JSON.parse(data);
    //console.log(obj);


    //alert(sending_parameters.initial_request);


    var articles = obj.sent.articles;

    if (sending_parameters.initial_request) {

      $list_for_headlines.hide(300, function () {
        $list_for_headlines.empty();
        $.each(articles, function (i, article) {
          $list_for_headlines.append('<li id="list-title_' + i + '" class="listica" name="' + article.publishedAt + '"><a class="naslov">' + article.title + '<br></a></li>');
          tmp_list_url.push(article.url)
        });
        $list_for_headlines.show(300);
        //alert(tmp_list_url);
      });

      $headline_title.show(300);

    }

    else {
      $.each(articles, function (i, article) {
        //alert(check_if_not_in(article.url,tmp_list_url));
        if (check_if_not_in(article.url, tmp_list_url)) {
          //dodaj na pocetak liste
          $list_for_headlines.append('<li id="list-title_' + i + '" class="listica"><a class="naslov">' + article.title + '<br></a></li>');
          tmp_list_url.push(article.url)

        }
        //inace nista 

      });

    }

    //omoguci sortiranje da bude clickable

    //alert(document.querySelectorAll('input[name="sorting"]'))
    //vrati ti listu nodova, kroz koju moras da se kreces i pobrises atribute disabled

    //zato sto na pocetku ne mozes da biras ali kasnije mozes
    $('#srtNto').removeAttr('disabled');
    $('#srtOtn').removeAttr('disabled');

    //vraca se na defaultnu vrednost
    $('#srtOtn').prop('checked', false);
    $('#srtNto').prop('checked', true);




    sending_parameters.initial_request = false;
    //alert(JSON.stringify(sending_parameters));

    //ponovo salji zahtev
    //ovaj bind ne znam kako radi, ali radi!
    window.setTimeout(post_ajax.bind(null, 'http://localhost:8000', JSON.stringify(sending_parameters), data_ok, data_not_ok), 0);
    console.log(JSON.stringify(sending_parameters))


  }


  function data_ok_sources(data) {


    var $list_for_sauces = $('#ajax_sauces_list');
    var $sauces_title = $('#sauces_title');

    errorSleepTime = 500;

    obj = JSON.parse(data);
    console.log(obj);

    var sources = obj.sent.sources;
    console.log(sources);

    $list_for_sauces.hide(300, function () {
      $list_for_sauces.empty();
      $.each(sources, function (i, source) {
        $list_for_sauces.append('<li id="list-sauce_' + i + '"><a class="naslov">' + source.name + '</a>:<p>' + source.description + '</p></li>');
      });
      $list_for_sauces.show(300);
    });

    $sauces_title.show(300);

    sending_parameters.initial_request = false;
    //alert(JSON.stringify(sending_parameters));

    //ponovo salji zahtev
    //ovaj bind ne znam kako radi, ali radi!
    window.setTimeout(post_ajax.bind(null, 'http://localhost:8000/sources', JSON.stringify(sending_parameters), data_ok_sources, data_not_ok_sources), 0);
    console.log(JSON.stringify(sending_parameters))


  }

  function data_not_ok_sources() {
    errorSleepTime *= 2;
    console.log(errorSleepTime);
    //alert(errorSleepTime);

    //ovaj bind ne znam kako radi, ali radi!
    window.setTimeout(post_ajax.bind(null, "http://localhost:8000/sources", JSON.stringify(sending_parameters), data_ok, data_not_ok_sources), errorSleepTime);

  }


  function data_not_ok() {
    errorSleepTime *= 2;
    console.log(errorSleepTime);
    //alert(errorSleepTime);

    //ovaj bind ne znam kako radi, ali radi!
    window.setTimeout(post_ajax.bind(null, "http://localhost:8000", JSON.stringify(sending_parameters), data_ok, data_not_ok), errorSleepTime);
  }




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


  $('#group1').on('click', function () {

    //alert(document.querySelector('input[name="country"]:checked').nextSibling.textContent);
    $('#btnCountry').text(document.querySelector('input[name="country"]:checked').nextSibling.textContent);
    // $('#btnCountry').parentElement.addClass('dotted_border');

    $('#btnSend').removeAttr('disabled');
    $('#btnSources').removeAttr('disabled');

  });


  $('#group2').on('click', function () {

    //alert(document.querySelector('input[name="country"]:checked').nextSibling.textContent);
    $('#btnCategory').text(document.querySelector('input[name="category"]:checked').nextSibling.textContent);
    //$('#btnCategory').addClass('dotted_border');
  });

  $('#group3').on('click', function () {

    //alert(document.querySelector('input[name="country"]:checked').nextSibling.textContent);
    $('#btnLanguage').text(document.querySelector('input[name="language"]:checked').nextSibling.textContent);
    //$('#btnCategory').addClass('dotted_border');
  });


  $('#srtNto').on('click', function () {
    $('#ajax_headlines_list').removeClass('sortOtn');
    $('#ajax_headlines_list').addClass('sortNto');

    $('#ajax_headlines_list').slideUp(400, function () {
      $('#ajax_headlines_list li').sort(sort_li_asc).appendTo('#ajax_headlines_list');
      $('#ajax_headlines_list').slideDown(400);
    });


  });


  $('#srtOtn').on('click', function () {
    $('#ajax_headlines_list').removeClass('sortNto');
    $('#ajax_headlines_list').addClass('sortOtn');

    $('#ajax_headlines_list').slideUp(400, function () {
      $('#ajax_headlines_list li').sort(sort_li_desc).appendTo('#ajax_headlines_list');
      $('#ajax_headlines_list').slideDown(400);
    });
  });


  function sort_li_asc(a, b) {
    //alert(new Date($(b).attr("name")) - new Date($(a).attr("name")));
    return new Date($(b).attr("name")) - new Date($(a).attr("name"));
  }


  function sort_li_desc(a, b) {
    //alert(new Date($(b).attr("name")) - new Date($(a).attr("name")));
    return new Date($(a).attr("name")) - new Date($(b).attr("name"));
  }










});