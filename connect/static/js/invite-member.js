$(document).ready(function(){

    $('#reinvite-member-dialog').dialog({
        autoOpen: false,
        modal: true
    });
    $('#revoke-member-dialog').dialog({
        autoOpen: false,
        modal: true
    });

    var user, email;

    $('.resend-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        email = $(this).data('email');
        $('#reinvite-member-dialog').dialog('open');
        $('.reinvite-member-form #id_user_id').val(user);
        $('.reinvite-member-form #id_email').val(email);
    });

    $('.revoke-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        $('#revoke-member-dialog').dialog('open');
        $('.revoke-invitation-form #id_user_id').val(user);
    });
});
