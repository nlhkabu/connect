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

    $('.toggle-user-expand').click(function(e){
        e.preventDefault();

        $(this).closest('.user-card').find('.user-expand').slideToggle(150);

        var $fullProfile = $(this).closest('.user-card').find('.full-profile');

        if ($fullProfile.html() == 'View Full Profile'){
            $fullProfile.html('Collapse')
        } else {
            $fullProfile.html('View Full Profile');
        }
    });


    // Display a Welcome dialog for new users

    $('#welcome-dialog').dialog({
        modal: true,
        width: 600,
        open: function( event, ui ) {
            $(this).closest('.ui-dialog').addClass('active');
        },
        close: function( event, ui ) {
            $(this).closest('.ui-dialog').removeClass('active');
        }
    });


    // ----------------------
    // MODERATION - UNIVERSAL
    // ----------------------


    // Show full application comments if they have been truncated
    $('.comments-dialog').dialog({
        autoOpen: false,
        modal: true,
        width: 600,
        maxHeight: 600,
        open: function( event, ui ) {
            $(this).closest('.ui-dialog').addClass('active');
        },
        close: function( event, ui ) {
            $(this).closest('.ui-dialog').removeClass('active');
        }
    });

    $('.read-more').click(function(e){
        e.preventDefault();

        id = $(this).data('id');
        $('#dialog'+ id).dialog('open');
    });


    // --------------------------
    // MODERATION - INVITE MEMBER
    // --------------------------

    $('#reinvite-member-dialog').dialog({
        autoOpen: false,
        modal: true,
        width: 300,
        open: function( event, ui ) {
            $(this).closest('.ui-dialog').addClass('active');
        },
        close: function( event, ui ) {
            $(this).find('form').parsley().reset();
            $(this).closest('.ui-dialog').removeClass('active');
        }
    });

    $('#revoke-member-dialog').dialog({
        autoOpen: false,
        modal: true,
        width: 450,
        open: function( event, ui ) {
            $(this).closest('.ui-dialog').addClass('active');
        },
        close: function( event, ui ) {
            $(this).find('form').parsley().reset();
            $(this).closest('.ui-dialog').removeClass('active');
        }
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

    var name;

    $('.revoke-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        name = $(this).data('name');
        email = $(this).data('email');

        $('#revoke-member-dialog').dialog('open');
        $('.revoke-invitation-form #id_user_id').val(user);
        $('.revoke-invitation-form .name').html(name);
        $('.revoke-invitation-form .email').html(email);
    });


    // --------------------------------
    // MODERATION - REVIEW APPLICATIONS
    // --------------------------------

    function applicationDialog(title){
        $('#review-application-dialog').dialog({
            autoOpen: false,
            modal: true,
            width: 400,
            title: title || 'Review Application',
            open: function( event, ui ) {
                $(this).closest('.ui-dialog').addClass('active');
            },
            close: function( event, ui ) {
                $(this).find('form').parsley().reset();
                $(this).closest('.ui-dialog').removeClass('active');
            }
        });
    };

    applicationDialog();

    $('.decision-link').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        decision = $(this).data('decision');
        title = $(this).html();

        applicationDialog(title);
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
        width: 600,
        maxHeight: 600,
        open: function( event, ui ) {
            $(this).closest('.ui-dialog').addClass('active');
        },
        close: function( event, ui ) {
            $(this).find('form').parsley().reset();
            $(this).closest('.ui-dialog').removeClass('active');
        }
    });

    $('.show-warnings').click(function(e){
        e.preventDefault();

        user = $(this).data('user');
        $('#dialog'+ user).dialog('open');
    });


    // Enable form on review abuse reports page
    function reportDialog(title){
        $('#review-abuse-dialog').dialog({
            autoOpen: false,
            modal: true,
            width: 400,
            title: title || 'Moderate Abuse Report',
            open: function( event, ui ) {
                $(this).closest('.ui-dialog').addClass('active');
            },
            close: function( event, ui ) {
                $(this).find('form').parsley().reset();
                $(this).closest('.ui-dialog').removeClass('active');
            }
        });
    };

    reportDialog();

    var report, decision, title;

    $('.decision-link').click(function(e){
        e.preventDefault();

        report = $(this).data('report');
        decision = $(this).data('decision');
        title = $(this).data('title');

        reportDialog(title);
        $('#review-abuse-dialog').dialog('open');
        $('.review-abuse-form #id_report_id').val(report);
        $('.review-abuse-form #id_decision').val(decision);
        $('.review-abuse-form .button').val(title);

    });

    // ---------------------------------
    // MODERATION - VIEW LOGS
    // ---------------------------------


    var period = $('#id_period').val();

    function toggleDateRange(period){
        var custom = $('.custom-date');
        var customInputs = $('.custom-date input');
        var error = $('.filter-logs .form-error');

        if (period == 'CUSTOM'){
            custom.show();
            customInputs.attr('disabled', false);
        } else {
            error.hide();
            custom.hide();
            customInputs.attr('disabled', true);
        }
    }

    toggleDateRange(period);

    $('#id_period').change(function(){
        period = $(this).val();
        toggleDateRange(period);
    });


    // Add Datepicker to date fields
    var minDate = $('#id_start_date').val();
    var maxDate = $('#id_end_date').val();

    $('#id_start_date').datepicker({
        dateFormat: "d/m/yy",
        maxDate: maxDate,
        onClose: function( selectedDate ) {
            $( "#id_end_date" ).datepicker( "option", "minDate", selectedDate );
        }
    });

    $('#id_end_date').datepicker({
        minDate: minDate,
        dateFormat: "d/m/yy",
        onClose: function( selectedDate ) {
            $( "#id_start_date" ).datepicker( "option", "maxDate", selectedDate );
        }
    });

});
