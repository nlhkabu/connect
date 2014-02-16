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


    // ----------------
    // PROFILE SETTINGS
    // ----------------

    // Enable fancy hover/focus CSS
    $('.bio, .name').on('blur', function(){
        $(this).addClass('inactive');
    }).on('focus', function(){
        $(this).removeClass('inactive');
    });

    // Set bio textarea width based on container

    var bioContainerWidth = $('td.profile-bio').width();

    $('.bio').css({
        width: bioContainerWidth - 20 // accounts for padding
    })

    // Fancy vertical resizing
    $('.bio').autosize();

});
