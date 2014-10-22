$(document).ready(function () {    

$( "#name" ).autocomplete({
      source: function(request, response){
        // ������ 
        $.ajax({
          url: "http://cmdb.at-consulting.ru:5000/get_list_user/",
          dataType: "json",
          // ��������� �������, ������������ �� ������ (��������� - ��������� ��� ������):
          data:{
            email_list: request.term
          },
          // ��������� ��������� ���������� �������
          success: function(data){
            // �������� ���������� ������ � ������������ ������� � ��������� � ��������������� ������� response.
            response($.map(data, function(item){
              return{
                label: item.full_name , // label ��� ������� � ������, �� ����������� �������� �� name.
                value: item.email  // value �������� ������� ���������� ���� ����� �� ����� EMAIL � json.
              }
			  
            }));
          }
        });
      },
      minLength: 1 // ����������� ����� ������� ��� ���������� ������.
    }); 
	
	}); 