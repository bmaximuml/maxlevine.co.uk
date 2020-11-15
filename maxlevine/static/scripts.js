document.addEventListener('click', function(e) {
    let clicked = getTarget(e, 'UL', 'A', 'SPAN');
    if (clicked.tagName !== 'LI') {
        return;
    }
    let content = document.getElementById(clicked.id + '-content');
    let tabs = document.getElementById('projects-tabs');
    let projects_content = document.getElementById('projects-content');

    for (const child of tabs.children) {
        child.classList.remove('is-active');
    }
    clicked.classList.add('is-active');

    for (const child of projects_content.children) {
        child.classList.add('is-hidden');
    }
    content.classList.remove('is-hidden');
});

function getTarget(e, parent = '', child = '', grandchild = '') {
    e = e || Event;
    let target = e.target || Event.target;

    if (target.tagName === parent) {
        target = target.firstElementChild;
    }
    else if (target.tagName === child) {
        target = target.parentElement;
    }
    else if (target.tagName === grandchild) {
        target = target.parentElement.parentElement;
    }

    return target;
}

document.addEventListener('DOMContentLoaded', () => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                if ($target.classList.contains('slidein')) {
                    slideMenuOut();
                }
                else {
                    slideMenuIn();
                }
            });
        });
    }

    const navbar_items = Array.prototype.slice.call(document.querySelectorAll('.navbar-item'), 0);
    navbar_items.forEach(item => {
        item.addEventListener('click', () => {
            slideMenuOut();
        })
    })
});

function slideMenuIn() {
    const $main_navbar = document.getElementById('main_navbar');
    $main_navbar.classList.add('is-active');
    $main_navbar.classList.remove('slideout');
    $main_navbar.classList.add('slidein');
    toggleBurgers();
}

function slideMenuOut() {
    const $main_navbar = document.getElementById('main_navbar');
    $main_navbar.classList.remove('slidein');
    $main_navbar.classList.add('slideout');
    $main_navbar.addEventListener('animationend', function() {
        if ($main_navbar.classList.contains('slideout')) {
            $main_navbar.classList.remove('is-active');
        }
    });
    toggleBurgers();
}

function toggleBurgers() {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach(el => {
            // Toggle the "is-active" class on the "navbar-burger"
            el.classList.toggle('is-active');
        });
    }
}
