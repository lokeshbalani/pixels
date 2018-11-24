'use strict';

(function (document, window, index) {
    // feature detection for drag&drop upload
    var isAdvancedUpload = function () {
        var div = document.createElement('div');
        return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
    }();


    // applying the effect for every form
    var forms = document.querySelectorAll('form');
    Array.prototype.forEach.call(forms, function (form) {
        var box = form.querySelector('.box'),
            input = form.querySelector('input[type="file"]'),
            label = form.querySelector('label'),
            errorMsg = form.querySelector('.box__error span'),
            restart = form.querySelectorAll('.box__restart'),
            config_range = document.querySelectorAll('.box__range'),
            droppedFiles = false,
            showFiles = function (files, target) {
                // label.textContent = files.length > 1 ? (input.getAttribute('data-multiple-caption') || '').replace('{count}', files.length) : files[0].name;
                // label.style.display = 'none';
                var placeholder = target.parentElement;
                placeholder.querySelector('.box__icon').style.display = 'none';
                if (target.classList.contains("box__padding")) {
                    target.classList.remove('box__padding');
                } else {
                    placeholder.parentElement.classList.remove('box__padding');
                }

                var uploadedDisplayEl = placeholder.querySelector('.box__im__uploaded');
                uploadedDisplayEl.innerHTML = "";

                var originalCanvas = document.createElement('canvas');
                originalCanvas.setAttribute("id", "upl_originalCanvas");
                var originalContext = originalCanvas.getContext("2d");
                uploadedDisplayEl.append(originalCanvas);

                Array.prototype.forEach.call(files, function (file, index) {
                    var img = new Image();
                    img.src = window.URL.createObjectURL(file);
                    img.onload = function () {
                        px.utils.canvas_fit2container(originalCanvas, img.width, img.height);
                        originalContext.drawImage(img, 0, 0);
                        window.URL.revokeObjectURL(this.src);
                        px.utils.init_canvas_selectnzoom(originalCanvas);
                    };
                });

                // Array.prototype.forEach.call(files, function (file, index) {
                //     var img = document.createElement('img');
                //     img.setAttribute("class", "photo")
                //     img.onload = function () {
                //         window.URL.revokeObjectURL(this.src);
                //     };
                //     img.style.width = '100%';
                //     img.src = window.URL.createObjectURL(file);
                //     uploadedDisplayEl.append(img);
                //     px.utils.generate_zoom_pan_img(img)
                // });



            },
            triggerFormSubmit = function () {
                var event = document.createEvent('HTMLEvents');
                event.initEvent('submit', true, false);
                form.dispatchEvent(event);
            };

        // letting the server side to know we are going to make an Ajax request
        var ajaxFlag = document.createElement('input');
        ajaxFlag.setAttribute('type', 'hidden');
        ajaxFlag.setAttribute('name', 'ajax');
        ajaxFlag.setAttribute('value', 1);
        form.appendChild(ajaxFlag);

        // automatically submit the form on file select
        input.addEventListener('change', function (e) {
            showFiles(e.target.files, e.target);
        });

        // drag&drop files if the feature is available
        if (isAdvancedUpload) {
            box.classList.add('has-advanced-upload'); // letting the CSS part to know drag&drop is supported by the browser

            ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(function (event) {
                form.addEventListener(event, function (e) {
                    // preventing the unwanted behaviours
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
            ['dragover', 'dragenter'].forEach(function (event) {
                form.addEventListener(event, function () {
                    box.classList.add('is-dragover');
                });
            });
            ['dragleave', 'dragend', 'drop'].forEach(function (event) {
                form.addEventListener(event, function () {
                    box.classList.remove('is-dragover');
                });
            });
            box.addEventListener('drop', function (e) {
                droppedFiles = e.dataTransfer.files; // the files that were dropped
                input.files = droppedFiles;
                showFiles(droppedFiles, e.target.parentElement);
            });
        }

        // restart the form if has a state of error/success
        Array.prototype.forEach.call(restart, function (entry) {
            entry.addEventListener('click', function (e) {
                e.preventDefault();
                box.classList.remove('is-error', 'is-success');
                input.click();
            });
        });

        // read and display the value of the range selected
        Array.prototype.forEach.call(config_range, function (config) {
            let rangeValEl = config.parentElement.parentElement.getElementsByClassName('box__rangeval')[0];

            rangeValEl.innerHTML = ": " + config.value;

            config.oninput = function () {
                rangeValEl.innerHTML = ": " + this.value;
            }
        });

        // Firefox focus bug fix for file input
        input.addEventListener('focus', function () {
            input.classList.add('has-focus');
        });
        input.addEventListener('blur', function () {
            input.classList.remove('has-focus');
        });

    });
}(document, window, 0));