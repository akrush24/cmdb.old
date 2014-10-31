$(document).ready(function(){

$.extend({ //обработчик перехода по ссылке на итем
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});

var byuuid = $.getUrlVar('hash'); //считать хэш итема из ссылки и открыть окно редактирвоания
if (byuuid !== undefined ) {edit_item(byuuid);}

}); //onreadypage_end


// Перехват клика по редактированию итема
        var uuid;
        function edit_item(clicked_id)
            {   
                uuid = clicked_id;
                $('#editItem').modal("show"); //Показать модальное окно для редактирвоания итема
            };
            
            var c_id;
            function edit_option_view(idid)
            { c_id = idid;
             $('#editoptionss').modal("show");
            };










