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

(function (e, t, n) {
    var r = e.querySelectorAll("html")[0];
    r.className = r.className.replace(/(^|\s)no-js(\s|$)/, "$1js$2")

    //function to add zoom and pan functionality to images
    px.utils.generate_zoom_pan_img = function (el) {
        pximg = el.parentElement;
        // zoom-pan mouse actions
        $(pximg).on('mouseover', function () {
            $(this).children('.photo').css({
                'transform': 'scale(' + $(this).attr('data-scale') + ')'
            });
        })
        $(pximg).on('mouseout', function () {
            $(this).children('.photo').css({
                'transform': 'scale(1)'
            });
        })
        $(pximg).on('mousemove', function (e) {
            $(this).children('.photo').css({
                'transform-origin': ((e.pageX - $(this).offset().left) / $(this).width()) * 100 + '% ' + ((e.pageY - $(this).offset().top) / $(this).height()) * 100 + '%'
            });
        })
        // px-img set up
        $(pximg).each(function () {
            var html = '<div class="txt">';

            // some text just to show zoom level on current item in this example
            if($(this).attr('data-ksize')){
                html += 'KERNEL SIZE: <strong class="pri-3 bold">' + $(this).attr('data-ksize') + '</strong><br>';
            }
            if($(this).attr('data-scale')){
                html += '<strong class="pri-3 bold">' + $(this).attr('data-scale') + 'x </strong>ZOOM ON HOVER';
            }

            html += '</div>'
            $(this).append(html);
        })
    }
})(document, window, 0);