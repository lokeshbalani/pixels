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

        var originalCanvas = document.createElement('canvas');
        originalCanvas.setAttribute("class", "originalCanvas");
        var originalContext = originalCanvas.getContext("2d");
        pximg.append(originalCanvas);

        var img = new Image();
        img.src = el.src;
        img.onload = function () {
            px.utils.canvas_fit2container(originalCanvas, img.width, img.height);
            originalContext.drawImage(img, 0, 0);
            px.utils.init_canvas_selectnzoom(originalCanvas);
        };

        el.style.display = 'none';
    };

    px.utils.canvas_fit2container = function (canvas, w, h, isPositonAbsolute) {
        // Make it visually fill the positioned parent
        canvas.style.width = '100%';

        if (isPositonAbsolute) {
            canvas.style.position = 'absolute';
            canvas.style.top = '0';
            canvas.style.left = '0';
        }

        // ...then set the internal size to match
        canvas.width = w;
        canvas.height = h;
    };

    px.utils.init_canvas_selectnzoom = function (originalCanvas) {
        var xyCoord = originalCanvas.getBoundingClientRect();
        var shiftX = xyCoord.left;
        var shiftY = xyCoord.top;
        var container = originalCanvas.parentElement;

        var selCanvas = document.createElement('canvas');
        var selContext = selCanvas.getContext("2d");
        selCanvas.setAttribute("class", "selectedCanvas");
        container.append(selCanvas);
        px.utils.canvas_fit2container(selCanvas, originalCanvas.width, originalCanvas.height, true);

        var targetImage = document.createElement('img'),
            downloadContainer = document.createElement('div');

        downloadContainer.setAttribute("class", "downloadContainer");
        targetImage.setAttribute("class", "targetImage");

        downloadContainer.append(targetImage);
        container.append(downloadContainer);

        var width = originalCanvas.width,
            height = originalCanvas.height;

        selContext.fillStyle = '#000';

        var clipCanvas = document.createElement('canvas'),
            clipContext = clipCanvas.getContext('2d');

        clipCanvas.width = 0;
        clipCanvas.height = 0;

        downloadContainer.append(clipCanvas);

        selCanvas.onmousedown = function (event) {
            var x0 = Math.max(0, Math.min(Math.abs(event.clientX - shiftX), width)),
                y0 = Math.max(0, Math.min(Math.abs(event.clientY - shiftY), height));

            targetImage.style.display = 'none';

            function update(event) {
                var x = Math.max(0, Math.min(Math.abs(event.clientX - shiftX), width)),
                    y = Math.max(0, Math.min(Math.abs(event.clientY - shiftY), height)),
                    dx = x - x0,
                    w = Math.abs(dx),
                    dy = y - y0,
                    h = Math.abs(dy);

                selContext.clearRect(0, 0, width, height);
                selContext.fillRect(x0, y0, dx, dy);
                clipCanvas.width = w;
                clipCanvas.height = h;
                if (w * h == 0) {
                    downloadContainer.style.visibility = 'hidden';
                } else {
                    downloadContainer.style.visibility = 'visible';
                    clipContext.drawImage(originalCanvas,
                        x0 + Math.min(0, dx), y0 + Math.min(0, dy), w, h,
                        0, 0, w, h);
                    downloadContainer.style.visibility = (w * h == 0 ? 'hidden' : 'visible');
                }

            };
            update(event);
            selCanvas.onmousemove = update;
            document.onmouseup = function (event) {
                selCanvas.onmousemove = undefined;
                document.onmouseup = undefined;
                targetImage.src = clipCanvas.toDataURL();
                targetImage.style.display = 'block';
            };
        };

        clipCanvas.style.display = 'none';
    };

})(document, window, 0);