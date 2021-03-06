if (typeof (px) === "undefined") px = {};
if (typeof (px.utils) === "undefined") px.utils = {};

(function (document, window, index) {
    px.stickyinit = function () {
        var stickyElms = document.querySelectorAll(".is-sticky");

        for(let i = 0; i < stickyElms.length; i++){
            let stickyEl = new StickyNav(stickyElms[i])
        }
    };

    function StickyNav(comp) {
        var me = this;
        this.jqcomp = jQuery(comp)

        this.doSticky = function(elTop){
            if (window.pageYOffset >= elTop) {
                comp.parentElement.classList.add("sticky");
                comp.closest('.px').firstElementChild.classList.add("sticky");
            } else {
                comp.parentElement.classList.remove("sticky");
                comp.closest('.px').firstElementChild.classList.remove("sticky");
            }
        };

        this.init = function(){
            let elTop = comp.offsetTop;

            window.onscroll = function () {
                me.doSticky(elTop);
            };
        };

        this.init();
    }

    px.stickyinit();
})(document, window, 0)