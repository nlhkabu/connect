$(document).ready(function(){
    //~var RevokeInvitationForm = $('.');

    var user, email;

    $('.resend-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        email = $(this).data('email');
        $('.reinvite-member-form').show(); // TODO: change this to toggle a modal
        $('.reinvite-member-form #id_user_id').val(user);
        $('.reinvite-member-form #id_email').val(email);
    });

    $('.revoke-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        $('.revoke-invitation-form').show(); // TODO: change this to toggle a modal
        $('.revoke-invitation-form #id_user_id').val(user);
    });
});
