
$(function() {
	var window_height = $(window).height(),
   	content_height = window_height - 200;
   	$('#list').innerHeight(content_height);
   	$('#employeeInfo').innerHeight(content_height);

	if($('#list').prop('scrollHeight') <= $('#list').height()){
    	$('#list').height('auto');
    	var window_height = $('#list').height(),
	   	content_height = window_height;
	   	$('#employeeInfo').height(content_height);
    }
});

$( window ).resize(function() {
	var window_height = $(window).height(),
   	content_height = window_height - 200;

   	$('#list').innerHeight(content_height);
   	$('#employeeInfo').innerHeight(content_height);

	if($('#list').prop('scrollHeight') <= $('#list').height()){
    	$('#list').height('auto');
    	var window_height = $('#list').height(),
	   	content_height = window_height;
	   	$('#employeeInfo').height(content_height);
    }
});

$(function() {
	var window_height = $(window).height(),
   	content_height = window_height - 250;
   	$('#listWithPadding').innerHeight(content_height);
   	$('#employeeInfo').innerHeight(content_height);

	if($('#listWithPadding').prop('scrollHeight') <= $('#listWithPadding').height()){
    	$('#listWithPadding').height('auto');
    	var window_height = $('#listWithPadding').height(),
	   	content_height = window_height;
	   	$('#employeeInfo').height(content_height);
    }
});

$( window ).resize(function() {
	var window_height = $(window).height(),
   	content_height = window_height - 250;

   	$('#listWithPadding').innerHeight(content_height);
   	$('#employeeInfo').innerHeight(content_height);

	if($('#listWithPadding').prop('scrollHeight') <= $('#listWithPadding').height()){
    	$('#listWithPadding').height('auto');
    	var window_height = $('#listWithPadding').height(),
	   	content_height = window_height;
	   	$('#employeeInfo').height(content_height);
    }
});