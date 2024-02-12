
document.addEventListener("DOMContentLoaded", function () {
    // Get the current date
    var currentDate = new Date();

    // Check if it's December
    if (currentDate.getMonth() === 11) {
        // Apply Christmas styles to specific elements

        var christmasNav = document.querySelector('.christmas-nav');
        christmasNav.classList.add("christmas-style-nav");
        document.body.classList.add("bg-christmas-design");
       

        // For Header Style contianer
        addClass('.HeaderStyle .HeaderContext-christmas', 'HeaderContext-christmas-style');
        removeClass('.HeaderStyle .HeaderContext-christmas','.HeaderContext-christmas');

        // Add the specified class this isfor the header context
        addClass('.HeaderContext .fs-secondary', 'NewHeaderColor1');
        addClass('.HeaderContext .fs-medium', 'NewHeaderColor1');
        addClass('.HeaderContext .fs-medium.text-clr-primary-accent', 'NewHeaderColor2');
        addClass('.HeaderContext .fs-primary.text-clr-primary-accent', 'NewHeaderColor2');
        // Remove the specified class
        removeClass('.HeaderContext .fs-secondary', '.fs-secondary');
        removeClass('.HeaderContext .fs-medium', '.fs-medium');
        removeClass('.HeaderContext .fs-medium.text-clr-primary-accent', '.fs-medium.text-clr-primary-accent');
        removeClass('.HeaderContext .fs-primary.text-clr-primary-accent', '.fs-primary.text-clr-primary-accent');

        // For Psuedo element icon
        addClass('.employeeCount', 'employeeCount-cm');
        addClass('.earlyEmployeeCount', 'earlyEmployeeCount-cm');
        addClass('.lateEmployeeCount', 'lateEmployeeCount-cm');
        addClass('.notEmployeeLogin', 'notEmployeeLogin-cm');

    
        removeClass('.employeeCount', 'employeeCount');
        removeClass('.earlyEmployeeCount', 'earlyEmployeeCount');
        removeClass('.lateEmployeeCount', 'lateEmployeeCount');
        removeClass('.notEmployeeLogin', 'notEmployeeLogin');

        // for insight border
        addClass('.InsightBorder', 'InsightBorder-cm')
        removeClass('.InsightBorder', 'InsightBorder');


        //for insight Text Color

        addClass('.InsightTextColor','InsightTextColor-cm')
        removeClass('.InsightTextColor', 'InsightTextColor');


        // for videoframe border 
        addClass('.videoElement', 'videoElement-cm' );
        removeClass('.videoElement','videoElement');


        //for table header and border
        addClass('.defaultdatatable', 'defaultdatatable-cm' );
        removeClass('.defaultdatatable','defaultdatatable');

        addClass('.InsightsEventIcon', 'InsightsEventIcon-cm');


        addClass('.video-container', 'video-container-cm');

        addClass('.TableContainer', 'TableContainer-cm');

        //for attendance row even adn odd column styling
        document.getElementById('defaultdatatable').classList.add('event-day');

        var christmasElements = document.querySelectorAll('.christmas-design');
        christmasElements.forEach(function(element) {
            element.classList.add("christmas-style");
        });
    }

    // // Check if it's February
    // if (currentDate.getMonth() === 1) {
    //     // Apply Valentine's design
    //     document.body.classList.add("valentines-design");
    // }

    // Add more conditions for other months or events

});

function addClass(selector, className) {
    var elements = document.querySelectorAll(selector);
    elements.forEach(function (element) {
        element.classList.add(className);
    });
}

function removeClass(selector, className) {
    var elements = document.querySelectorAll(selector);
    elements.forEach(function (element) {
        element.classList.remove(className);
    });
}

