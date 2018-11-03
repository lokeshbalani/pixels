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

(function (e, t, n) {
    var r = e.querySelectorAll("html")[0];
    r.className = r.className.replace(/(^|\s)no-js(\s|$)/, "$1js$2")
})(document, window, 0);