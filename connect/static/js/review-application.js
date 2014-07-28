$(document).ready(function(){

    $('#review-application-dialog').dialog({
        autoOpen: false,
        modal: true
    });

    var user, decision;

    $('.decision-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        decision = $(this).data('decision');

        $('#review-application-dialog').dialog('open');
        $('.review-application-form #id_user_id').val(user);
        $('.review-application-form #id_decision').val(decision);
    });

});
