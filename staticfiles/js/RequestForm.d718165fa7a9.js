

document.getElementById('request').addEventListener('change', function () {
    var selectedValue = this.value;
    var outTimeDate = document.querySelector('.out-time-date');
    var inTimeDate = document.querySelector('.in-time-date');
    var deductRange = document.querySelector('.deductrange');
    var requestdate = document.querySelector('.requestdate');

    // Hide all div elements
    outTimeDate.style.display = 'none';
    inTimeDate.style.display = 'none';
    deductRange.style.display = 'none';
    requestdate.style.display = 'none';
    document.getElementById('out-time-date').removeAttribute('required')
    document.getElementById('in-time-date').removeAttribute('required')
    document.getElementById('deductrange').removeAttribute('required')
    document.getElementById('requestdate').removeAttribute('required')


    // Show specific div elements based on the selected option
    if (selectedValue === 'Sick' || selectedValue === 'Vacation'|| selectedValue === 'Paternity') {
        deductRange.style.display = 'block';
        requestdate.style.display = 'block';
        document.getElementById('deductrange').setAttribute('required','required')
        document.getElementById('requestdate').setAttribute('required','required')
    } else {
        
        outTimeDate.style.display = 'block';
        inTimeDate.style.display = 'block';
        document.getElementById('out-time-date').setAttribute('required','required')
        document.getElementById('in-time-date').setAttribute('required','required')
    }
});




$(document).ready(function() {


var empcodeInput = $('#empcode');
var searchList = $('#search-list');


var outTimeDateInput = $('#out-time-date');
empcodeInput.keyup(function() {

    var query = $(this).val();


    if (query.trim() === '') {

        searchList.hide();
        return;
    }

$.ajax({
    url: '/search_view/',
    data: { 'query': query, csrfmiddlewaretoken: '{{ csrf_token }}' },
    dataType: 'json',
    success: function(response) {
   
        searchList.empty();

        if (response.data && response.data.length > 0) {
            response.data.forEach(function(item) {
                searchList.append('<li>' + item.empcode + '</li>');
            });
            searchList.show();
        } else {
            searchList.hide();
        }
    },
    error: function(xhr, textStatus, errorThrown) {
        console.error('Error in AJAX request:', errorThrown);
    }
});
});


searchList.hide();



empcodeInput.focus(function() {

searchList.show();

searchList.css('z-index', 2);
});

empcodeInput.blur(function() {

searchList.hide();

searchList.css('z-index', 1);
});

outTimeDateInput.focus(function() {
searchList.css('z-index', 2);
});

outTimeDateInput.blur(function() {
searchList.css('z-index', 1);
});
});


document.getElementById('invalidCheck').addEventListener('change', function() {
  var remarksContainer = document.getElementById('remarksContainer');
  remarksContainer.style.display = this.checked ? 'block' : 'none';
});
