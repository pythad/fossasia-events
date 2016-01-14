function getCookie(name) {
	var matches = document.cookie.match(new RegExp(
		"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

String.prototype.format = function() {
	var args = arguments;
	this.unkeyed_index = 0;
	return this.replace(/\{(\w*)\}/g, function(match, key) {
		if (key === '') {
			key = this.unkeyed_index;
			this.unkeyed_index++
		}
		if (key == +key) {
			return args[key] !== 'undefined' ? args[key] : match;
		} else {
			for (var i = 0; i < args.length; i++) {
				if (typeof args[i] === 'object' && typeof args[i][key] !== 'undefined') {
					return args[i][key];
				}
			}
			return match;
		}
	}.bind(this));
};

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
	});
	$('.attendees-open').click(function() {
		var event_pk = $(this).data('eventPk');
		$.ajax({
			type: 'GET',
			url: '/events/get_attendees/',
			data: {
				'event_pk': event_pk
			},
			success: function(response) {
				var p_str = "<li><a href=\"/accounts/profile/{pk}/{username}\">{username}</a></li>";
				if (response.attendees_sure) {
					var $attendees_sure_list = $(".attendees_sure{} ul".format(event_pk));
					$attendees_sure_list.html('');
					$.each(response.attendees_sure, function(key, value) {
						resp_str = p_str.format({
							'username': value.username,
							'pk': value.pk
						});
						$attendees_sure_list.append(resp_str);
					});
				};
				if (response.attendees_not_sure) {
					var $attendees_not_sure_list = $(".attendees_not_sure{} ul".format(event_pk));
					$attendees_not_sure_list.html('');
					$.each(response.attendees_not_sure, function(key, value) {
						resp_str = p_str.format({
							'username': value.username,
							'pk': value.pk
						});
						$attendees_not_sure_list.append(resp_str);
					});
				};
				if (response.attendees_declined) {
					var $attendees_declined_list = $(".attendees_declined{} ul".format(event_pk));
					$attendees_declined_list.html('');
					$.each(response.attendees_declined, function(key, value) {
						resp_str = p_str.format({
							'username': value.username,
							'pk': value.pk
						});
						$attendees_declined_list.append(resp_str);
					});
				};
			},
			error: function(rs, e) {
				alert(e);
			},
			async: false
		});
	});
});