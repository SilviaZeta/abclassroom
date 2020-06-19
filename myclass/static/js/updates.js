$(document).ready(function() {

	//$('.update_button').off('click');
	$('.update_button').on('click', function(e) {

		e.preventDefault();

		/* Retrieve some variables */
		var class_id = $(this).attr('class_id');
		var class_url = $(this).attr('enroll-users-url');
		var class_slug = $(this).attr('class_slug'); 
		var class_role = $(this).attr('class_role'); 
		var username = $(this).attr('username'); 


		/* Add User Button */
		//var base_add_user_url = document.getElementById('js-add-user').getAttribute("default-href");
		document.getElementById('js-add-user').href = class_url+'add_user/'+class_id+'/'; 

		/* Retrieve user list from database */

		if (class_id == '') {

    	} else {
			$.ajax({
				type: 'POST',
				url: class_url,
				data: { class_id : class_id },
				dataType: 'json',
				success: function(response) {

					$('#js-update-section').fadeOut(100).fadeIn(100);
					
					$("#class_id").text("Class "+class_slug+": Enrolled users");

					//prepare table for new content
					$("#enrolled_users tbody").empty();

					// display the newly friend to table.
					var data = response["data"];

					//var base_del_user_url = document.getElementById('enrolled_users').getAttribute("default-href");
	                
	            	if (class_role == 'Teacher') {

	            		/* Enable Add Button */
			        	var add_button = document.getElementById('js-add-user');
			        	if ( add_button.classList.contains('disabled') ) {
			        		add_button.classList.remove('disabled');
			        	}

	            		for (var i=0; i < data["id"].length; i++) {
		                	
		                	if (data["role"][i] == "Student") {

		                		var custom_url = class_url+"remove_user/"+class_id+"/"+data["id"][i]+"/";

				                $("#enrolled_users tbody").prepend(
				                    `<tr>
				                    <td>${data["username"][i]||""}</td>
				                    <td>${data["role"][i]||""}</td>
				                    <td>${data["email"][i]||""}</td>
				                    <td><a class="link-custom" href="${custom_url}" title='Remove User'>
				                    	<i class="fas fa-user-slash fa-lg"></i></a></td>
				                    </tr>`)
				             
				            } else if (data["role"][i] == "Pending") {
				            	var custom_url = class_url+"approve_user/"+class_id+"/"+data["id"][i]+"/";

				            	$("#enrolled_users tbody").prepend(
				                    `<tr>
				                    <td>${data["username"][i]||""}</td>
				                    <td>${data["role"][i]||""}</td>
				                    <td>${data["email"][i]||""}</td>
				                    <td><a class="link-custom" href="${custom_url}" title='Approve User'>
				                    	<i class="fas fa-user-plus fa-lg"></i></a></td>
				                    </tr>`)
			                	
				        	} else {
				            	$("#enrolled_users tbody").prepend(
				                    `<tr>
				                    <td>${data["username"][i]||""}</td>
				                    <td>${data["role"][i]||""}</td>
				                    <td>${data["email"][i]||""}</td>
				                    <td></td>
				                    </tr>`)
				            };
				        }; 
			        } else if (class_role == 'Student') {
			        	
			        	/* Disable Add Button */
			        	var add_button = document.getElementById('js-add-user');
			        	if ( ! add_button.classList.contains('disabled') ) {
			        		add_button.classList.add('disabled');
			        	}


			        	for (var i=0; i < data["id"].length; i++) {

			        		if (username == data["username"][i]) {
			        			var custom_url = class_url+"remove_user/"+class_id+"/"+data["id"][i]+"/";
		                		
				            	$("#enrolled_users tbody").prepend(
				                    `<tr>
				                    <td>${data["username"][i]||""}</td>
				                    <td>${data["role"][i]||""}</td>
				                    <td>${data["email"][i]||""}</td>
				                    <td><a class="link-custom" href="${custom_url}" title='Remove User'>
				                    	<i class="fas fa-user-slash fa-lg"></i></a></td>
				                    </tr>`)
			                    
	                		} else {

				            	$("#enrolled_users tbody").prepend(
				                    `<tr>
				                    <td>${data["username"][i]||""}</td>
				                    <td>${data["role"][i]||""}</td>
				                    <td>${data["email"][i]||""}</td>
				                    <td></td>
				                    </tr>`)
		                	}
			        	};

					};
				},

				error: function(response) {
					 // alert the error if any error occured
					alert(response["error"]);
				}
			});



			$(document.body).on("click", "tr[data-href]", function() {
				if(confirm("Are you sure you want to remove this user?")){
	        		window.location.href = this.dataset.href;
			    } else {
			        return false;
			    }
			});
		}	

	});	

	

});




