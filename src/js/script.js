window.onload = function onWindowLoad() {
    const navbarShowBtn = document.querySelector('.navbar-show-btn');
    const navbarCollapseDiv = document.querySelector('.navbar-collapse');
    const navbarHideBtn = document.querySelector('.navbar-hide-btn');

    if (navbarShowBtn && navbarCollapseDiv && navbarHideBtn) {
        navbarShowBtn.onclick = function() {
            navbarCollapseDiv.classList.add('navbar-show');
        };

        navbarHideBtn.onclick = function() {
            navbarCollapseDiv.classList.remove('navbar-show');
        };
    } else {
        console.error('Navbar elements not found');
    }

    function changeSearchIcon() {
        const searchIconImg = document.querySelector('.search-icon img');
        if (searchIconImg) {
            let winSize = window.matchMedia("(min-width: 1200px)");
            if (winSize.matches) {
                searchIconImg.src = "images/search-icon.png";
            } else {
                searchIconImg.src = "images/search-icon-dark.png";
            }
        } else {
            console.error('Search icon image not found');
        }
    }

    window.onresize = function() {
        changeSearchIcon();
        document.body.classList.add('resize-animation-stopper');
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            document.body.classList.remove('resize-animation-stopper');
        }, 400);
    };

    changeSearchIcon();

    let resizeTimer;
};
