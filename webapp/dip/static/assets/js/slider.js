/**
 * We can't 100% rely on browsers supporting drag and drop. We should provide a fallback solution. 
 * 
 * Drag & drop file upload relies on a number of different JavaScript API's.
 * We need to detect the support for:
 * 1. drag & drop events
 * 2. FormData interface, which is for forming a programmatic object of the selected file(s) so they can be sent to the server via Ajax
 * 3. DataTransfer object
 * 
 * There is no bullet-proof way to detect the availability of the DataTransfer object before user's 
 * first interaction with the drag & drop interface.The trick is to check the availability of FileReader API 
 * right when the document loads because browsers that support FileReader support DataTransfer too
 */

// var isAdvancedUpload = function () {
//     var div = document.createElement('div');
//     return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
// };
if (typeof (px) === "undefined") px = {};
if (typeof (px.utils) === "undefined") px.utils = {};

(function (document, window, index) {
    px.sliderinit = function () {
        var sliderElms = document.querySelectorAll(".slider-container");

        for (let i = 0; i < sliderElms.length; i++) {
            let sliderEl = new Slider(sliderElms[i])
        }
    };

    function Slider(comp) {
        var me = this;
        this.jqcomp = jQuery(comp);

        this.config = {
            slideIndex: 0
        }

        this.add = function (n) {
            this.config.slideIndex += n;
            me.render(this.config.slideIndex);
        };

        this.curr = function (n) {
            this.config.slideIndex = n;
            me.render(this.config.slideIndex);
        };

        this.render = function (n) {
            var i;
            var slides = comp.getElementsByClassName("slide");
            if (n > slides.length - 1) {
                this.config.slideIndex = 0;
            }


            if (n < 0) {
                this.config.slideIndex = slides.length - 1
            }

            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }

            slides[this.config.slideIndex].style.display = "block";
        };

        this.init = function () {
            this.render(this.config.slideIndex);

            comp.querySelector(".prev").onclick = function () {
                me.add(-1);
            }

            comp.querySelector(".next").onclick = function () {
                me.add(1);
            }
        };

        this.init();
    }

    px.sliderinit();

})(document, window, 0);