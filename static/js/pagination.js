$(document).ready(function() {
    $(document).on('click', '.btn-pagination', function(event) {
        event.preventDefault();

        var page = $(this).attr('href').split('=')[1];
        $.ajax({
            url: '?page=' + page,
            type: 'GET',
            success: function(data) {
                // Update the content
                $('#defaultdatatable').html($(data).find('#defaultdatatable').html());

                // Update the pagination links
                $('.pagination').html($(data).find('.pagination').html());
            },
            error: function() {
                console.log('Error fetching data');
            }
        });
    });
});
