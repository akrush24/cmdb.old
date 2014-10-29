$(document).ready(function () {    

$( "#name" ).autocomplete({
      source: function(request, response){
        // Запрос 
        $.ajax({
          url: "http://cmdb.at-consulting.ru:5000/get_list_user/",
          dataType: "json",
          // параметры запроса, передаваемые на сервер (последний - подстрока для поиска):
          data:{
            email_list: request.term
          },
          // обработка успешного выполнения запроса
          success: function(data){
            // приведем полученные данные к необходимому формату и передадим в предоставленную функцию response.
            response($.map(data, function(item){
              return{
                label: item.full_name , // label это надпись в списке, ей присваиваем параметр из name.
                value: item.email  // value значение которое присвоится полю ввода из ключа EMAIL в json.
              }
			  
            }));
          }
        });
      },
      minLength: 1 // минимальная длина запроса для выполнения поиска.
    }); 
	
	}); 