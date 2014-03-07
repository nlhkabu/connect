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

});
