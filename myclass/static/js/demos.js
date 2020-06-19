
$(document).ready(function() {

   $('.dragme').each(function() {
      $(this).draggable();
    });


  $('.group-countdown').each(function() {
    var expiry = $(this).attr('expiry');
    console.log(expiry)
    $(this).countdown({until: new Date(expiry), compact:true});
  });


});




