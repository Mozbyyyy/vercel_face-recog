// Branch List

let BranchCards = document.querySelector(".Branch-Cards");

let rightScroll = document.getElementById("rightScroll");

let leftScroll = document.getElementById("leftScroll");

    rightScroll.style.opacity ='0.7';
    leftScroll.style.opacity = '0.7';
    BranchCards.addEventListener("wheel", (evt)=>{
        evt.preventDefault();
        BranchCards.scrollLeft += evt.deltaY;
        BranchCards.style.scrollBehavior = "auto";
    });

    rightScroll.addEventListener("click", ()=>{
        rightScroll.style.opacity = '1' ;
        BranchCards.style.scrollBehavior = "smooth";
        BranchCards.scrollLeft += 1000;
    });

    leftScroll.addEventListener("click", ()=>{
        leftScroll.style.opacity ='1';
        BranchCards.style.scrollBehavior = "smooth";
        BranchCards.scrollLeft -=1000;
    });

    leftScroll.addEventListener('transitionend', () => {
    leftScroll.style.opacity = '0.7';
    });

    rightScroll.addEventListener('transitionend', () => {
    rightScroll.style.opacity = '0.7';
    });


$(document).ready(function () {
    $('input[name="search-bar"]').on('input', function () {
        var searchTerm = $(this).val().toLowerCase();

        $('.Branch-card-style').each(function () {
            var branchName = $(this).find('.fs-small').text().toLowerCase();
            var location = $(this).find('.fs-small span').text().toLowerCase();
            var abbr = $(this).find('.fs-small-abbr').text().toLowerCase();

            if (branchName.includes(searchTerm) || location.includes(searchTerm) || abbr.includes(searchTerm)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});








