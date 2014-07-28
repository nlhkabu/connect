$(document).ready(function(){

    var user, decision, title;

    $('.decision-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        decision = $(this).data('decision');
        title = $(this).html();

        $('#review-application-dialog').dialog({
            autoOpen: false,
            modal: true,
            title: title,
            width: 400
        });

        $('#review-application-dialog').dialog('open');
        $('.review-application-form #id_user_id').val(user);
        $('.review-application-form #id_decision').val(decision);
        $('.review-application-form .button').val(title);
    });

});
