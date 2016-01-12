function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

$(document).ready(function() {
	$('.p-status').click(function() {
		var $status = $(this);
		var status_n = $status.data('status');
		var event_pk = $('.event').data('eventPk');
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			type: 'POST',
			url: '/events/participate/',
			data: {
				'status_n': status_n,
				'event_pk': event_pk,
				'csrfmiddlewaretoken': csrftoken
			},
			success: function() {
				console.log('done!');
				console.log($('.p-status'));
				$('.p-status').each(function() {
					$(this).removeClass('btn-primary');
				});
				console.log($(this));
				$status.addClass('btn-primary');
			},
            error: function(rs, e) {
            	alert(e);
            },
            async: false
		});
	})
});