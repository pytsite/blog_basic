require(['jquery', 'twitter-bootstrap', 'pytsite-responsive'], function ($) {
    var topNavbar = $('#navbar-top-collapse');
    topNavbar.find('a').click(function () {
        topNavbar.collapse('hide');
    });
});
