
$(document).ready(function() {
    

    $('#js-search').keyup('#search-class-form', function(e) {
        e.preventDefault();

    	var class_slug = $(this).val();
    	console.log(class_slug)
    	var search_url = $(this).attr('search-url');
        console.log(search_url)


    	if (class_slug == '') {

             $("#search-result").empty();

    	} else {
    		$('#search-result').html('');
    		$.ajax({
    			url: search_url,
    			method: "post",
    			data: {class_slug:class_slug},
    			dataType:"json",
    			success:function(response) {

                    //get the data
                    var data = response["data"]

                    //empty previously filled element
                    $("#search-result").empty();

                    var base_join_class_url = document.getElementById('search-class-form').getAttribute("join-class-url");
                    console.log(base_join_class_url)

                    for (var i=0; i < data["id"].length; i++) {



                        var join_class_url = 'join_class/'+data["id"][i]+'/';
                        

                        $("#search-result").prepend(
                            `<a href="${join_class_url}" class="list-group-item list-group-item-action">
                                <div class=blue-link>Join ${data['slug'][i]}, ${data['subject'][i]}</div>
                            </a>`
                        );
                    };
                  },
                error: function(response) {
                    alert(response["error"]);
                }

    		});
    	}
    });

});




