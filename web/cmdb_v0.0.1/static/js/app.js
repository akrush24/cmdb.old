﻿$(document).ready(function(){

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







