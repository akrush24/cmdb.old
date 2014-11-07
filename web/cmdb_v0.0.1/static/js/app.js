$(document).ready(function(){

$.extend({ //обработчик перехода по ссылке на итем
  getUrlVars: function(){
    var vars = [], id;
    var ides = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < ides.length; i++)
    {
      id = ides[i].split('=');
      vars.push(id[0]);
      vars[id[0]] = id[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});

var byuuid = $.getUrlVar('id'); //считать id итема из ссылки и открыть окно редактирвоания
if (byuuid !== undefined ) {edit_item(byuuid);}

}); //onreadypage_end


// Перехват клика по редактированию итема
        var val_param_id;
        function edit_item(param_id){
                val_param_id = param_id;
                $('#editItem').modal("show"); //Показать модальное окно для редактирвоания итема
            };
            
            var c_id;
            function edit_option_view(clicked_opt_id)
            { c_id = clicked_opt_id;
             $('#editoptionss').modal("show");
            };
			
			










