var $DOM = $(document);

$DOM.on('click', '#login_submit', function() {

	console.log("login clicked");
    data = {}
    data["email"] = $(".email").val();
    data["password"] = $(".password").val();

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/login/validate',
        contentType: 'application/json', // Add this line to specify the content type
		success: function(result) {
            if (result.success) {
                window.location.href = "/";
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});
