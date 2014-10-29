$(document).ready(function(){

// Добавление справочника 
$(function() { 
var iditer=1; // Итератор для нового newid
$('#adddictline').click(function() {
$('#dictline').append('<div><input type="text" class="form-control" name="newid'+iditer+'" placeholder="Введите новое значение" required="" autocomplete="off" /></div>')
iditer=iditer+1;
});
});
// Добавление справочника конец 


$("#addticketsubmit").click(function()
        {
        $("form[name='Ticketform']").submit();
        });

$("#editItemForm").click(function()
        {
        $("form[name='editItemForm']").submit();
        });
}); //onreadypage_end


// Перехват клика по редактированию итема
        var uuid;
        function edit_item(clicked_id)
            {   
                uuid = clicked_id;
                $('#editItem').modal("show"); //Показать модальное окно для редактирвоания итема
            };
// Перехват клика по редактированию итема


 $(function(){
								$(function(){ 
                                $.getJSON('{{ url_for('get_user_menu') }}', function(menulist) {
								  var i = -1;
									$.each(menulist, function(keylist, vallist) { 
									   i=i+1;
										$('#dropMenu').prepend('<li><a href="http://cmdb.at-consulting.ru:5000/list/'+menulist[i].name+'"><b>'+menulist[i].name + '</b>&nbsp;<span class="badge pull-right">'+menulist[i].value + '</span></a></li></option>');
										});  
                                            });
                                        });
                                        });





