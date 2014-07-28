$(document).ready(function(){

    // -------
    // ALL APP
    // -------

    // Ability progressbar and tooltip
    $('.ability').each(function(){
        var value = $(this).data('value');

        $(this).progressbar({
            value : value,
            max : 100
        });
    });

    $(document).tooltip({
        items: '.ability',
        content: function() {
            return $( this ).data('description');
        },
        track: true,
        show: {
            effect: 'show'
        },
        hide: {
            effect: 'hide'
        }
    });


    // ---------
    // LOGGED IN
    // ---------

    // Toggle mobile menu
    $( '.mobile-icon' ).click(function() {
        $('nav.main').slideToggle();
    });

    // Reset when window switches to desktop view
    $(window).resize(function() {
        if ($(window).width() > 620) {
            $('nav.main').show();

        }
    });


    // ---------
    // DASHBOARD
    // ---------

    // Toggle 'close to me' form on radio select

    $('input[name="locationRadios"]').on('change', function(){
        if ($(this).val()=='all') {
             $('.close-to-me').hide();
        } else  {
             $('.close-to-me').show();
        }
    });


    // Expand and Collapse Member Profiles

    $('.toggle-member-expand').click(function(e){
        e.preventDefault();

        $(this).closest('.member-card').find('.member-expand').slideToggle(150);

        var $fullProfile = $(this).closest('.member-card').find('.full-profile');

        if ($fullProfile.text() == 'View Full Profile'){
            $fullProfile.text('Collapse')
        } else {
            $fullProfile.text('View Full Profile');
        }
    });


    // --------------------------
    // MODERATION - INVITE MEMBER
    // --------------------------

    $('#reinvite-member-dialog').dialog({
        autoOpen: false,
        modal: true,
        width: 'auto'
    });

    $('#revoke-member-dialog').dialog({
        autoOpen: false,
        modal: true,
        width: 'auto'
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


    // --------------------------------
    // MODERATION - REVIEW APPLICATIONS
    // --------------------------------

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


    // ---------------------------------
    // MODERATION - REVIEW ABUSE REPORTS
    // ---------------------------------

    // Show User warning on review abuse reports page
    $('.warning-dialog').dialog({
        autoOpen: false,
        modal: true,
        width: 600
    });

    $('.show-warnings').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        $('#dialog'+ user).dialog('open');
    });


    // Enable form on review abuse reports page

    var report, decision, title;

    $('.decision-link').click(function(e){
        e.preventDefault();

        report = $(this).data('report');
        decision = $(this).data('decision');
        title = $(this).data('title');

        $('#review-abuse-dialog').dialog({
            autoOpen: false,
            modal: true,
            title: title,
            width: 400
        });

        $('#review-abuse-dialog').dialog('open');
        $('.review-abuse-form #id_report_id').val(report);
        $('.review-abuse-form #id_decision').val(decision);
        $('.review-abuse-form .button').val(title);

    });

});
