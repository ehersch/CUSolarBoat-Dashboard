//menu-icon click toggles class 'open' for navbar and toggles bear visibility
let navbar_open = false;

function toggleNavbar() {
    /*Toggles the state of the navbar, used on mobile when
    menu-icon is clicked to open and close menu*/

    //navbar_open is a bool that provides the state of the navbar
    navbar_open = !navbar_open;

    //Toggle class 'open' for navbar and bear
    var navbar = document.getElementById('navbar');
    var bear = document.getElementById('bear');
    navbar.classList.toggle('open');
    bear.classList.toggle('open');

    //Switches between menu and cross icon
    var icon = document.getElementById('menu-icon');
    if (navbar_open) {
        icon.classList.remove('fa-bars')
        icon.classList.add('fa-xmark')
    }
    else {
        icon.classList.remove('fa-xmark')
        icon.classList.add('fa-bars')
    }
}

//If the menu is open and user clicks outside menu, it gets hidden
$(document).mouseup(function(e){
    var menu = $('.navbar');
    if (!menu.is(e.target) && menu.has(e.target).length === 0 && navbar_open){
       toggleNavbar();
    }
 });
  