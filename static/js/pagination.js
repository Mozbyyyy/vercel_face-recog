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

                // Reattach event listeners for edit and delete buttons
                attachEventListeners();
            },
            error: function() {
                console.log('Error fetching data');
            }
        });
    });

    // Initial attachment of event listeners
    attachEventListeners();
});

function attachEventListeners() {
    // Event delegation for edit button
    $(document).on('click', '.edit-btn', function() {
        // Your edit button logic here
        var empCode = $(this).data('emp-code');
        // ...
    });

    // Event delegation for delete button
    $(document).on('click', '.delete-btn', function() {
        // Your delete button logic here
        var empCode = $(this).data('emp-code');
        // ...
    });
}
