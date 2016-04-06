$(document).ready(function() {
    $('.collapse').on('show.bs.collapse', function() {
        var id = $(this).attr('id');
        $('a[href="#' + id + '"]').closest('.panel-heading').addClass('active-faq');
        $('a[href="#' + id + '"] .panel-title span').html('<i class="glyphicon glyphicon-minus"></i>');
    });
    $('.collapse').on('hide.bs.collapse', function() {
        var id = $(this).attr('id');
        $('a[href="#' + id + '"]').closest('.panel-heading').removeClass('active-faq');
        $('a[href="#' + id + '"] .panel-title span').html('<i class="glyphicon glyphicon-plus"></i>');
    });

    /*
        add form validation
    */
    $( '#run-job-btn' ).on('click', function(e){
        //if (lots_of_stuff_already_done === true) {
        //    lots_of_stuff_already_done = false; // reset flag
        //    return; // let the event bubble away
        //}

        e.preventDefault();
        $( '#sim-form' ).submit();
        // do lots of stuff

        // lots_of_stuff_already_done = true; // set flag
        // $(this).trigger('click');
    });

});