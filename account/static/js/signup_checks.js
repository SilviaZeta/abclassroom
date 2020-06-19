$(document).ready(function(){

    $("#id_username").change(function (e) {

		e.preventDefault();

		var username = $(this).val();
		var ajax_url = $(this).attr('username-url');
		$('#error_username').html("");

		$.ajax({
			url: ajax_url,
			data: {'username': username},
			dataType: 'json',
			success: function (data) {
				if (data.is_empty | data.is_taken) {
            		$('#error_username').text(data['errormsg']);
          		}
			},	
			error: function(data) {
				console.log("error");
			}
		});
    });


    $("#id_email").change(function (e) {

		e.preventDefault();
		
		var email = $(this).val();
		var ajax_url = $(this).attr('email-url');	
		$('#error_email').html("");

		$.ajax({
			url: ajax_url,
			data: {'email': email},
			dataType: 'json',
			success: function (data) {
				if (data.is_empty | data.is_taken | data.is_invalid) {
            		$('#error_email').text(data['errormsg']);
          		}; 
			},	
			error: function(data) {
				console.log("error");
			}
		});
    });


    $("#id_password1").change(function (e) {

		e.preventDefault();
			
		var password1 = $(this).val();
		var ajax_url = $(this).attr('password1-url');	
		$('#error_password1').html("");

		$.ajax({
			url: ajax_url,
			data: {'password1': password1},
			dataType: 'json',
			success: function (data) {
				if (data.is_empty | data.is_invalid) {
            		$('#error_password1').text(data['errormsg']);
          		}; 
			},	
			error: function(data) {
				console.log("error");
			}
		});
    });



    $("#id_password2").change(function (e) {

		e.preventDefault();
		
		var password1 = $("#id_password1").val();
		var password2 = $(this).val();
		var ajax_url = $(this).attr('password2-url');	
		
		$('#error_password1').html("");

		$.ajax({
			url: ajax_url,
			data: {'password1': password1, 'password2': password2},
			dataType: 'json',
			success: function (data) {
				if (data.is_invalid | data.is_unmatched) {
            		$('#error_password1').text(data['errormsg']);
          		};
			},	
			error: function(data) {
				console.log("error");
			}
		});
    });

});