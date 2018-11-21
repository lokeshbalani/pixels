if (typeof (px) === "undefined") px = {};
if (typeof (px.utils) === "undefined") px.utils = {};

(function (document, window, index) {
    px.ccinit = function () {
        var ccEl = document.getElementById("connected-component");

        let init = new ConnectedComponents(ccEl)
    };

    function ConnectedComponents(comp) {
        var me = this;
        this.jqcomp = jQuery(comp)

        this.displayTable = function (mat, container_id) {
            if (typeof (container_id) != "undefined" && container_id != "") {
                let ccTbl = document.querySelector("#" + container_id + " tbody");

                let html = "",
                    i, j;

                for (i = 0; i < mat.length; i++) {
                    html += "<tr>";

                    for (j = 0; j < mat[i].length; j++) {
                        if(i != 0 && i != (mat.length - 1) && j != 0 && j != (mat[i].length - 1)){
                            if (mat[i][j] > 0) {
                                html += "<td class='white' contenteditable='true' data-pos='" + i + "," + j + "'>" + mat[i][j] + "</td>"
                            } else {
                                html += "<td class='black' contenteditable='true' data-pos='" + i + "," + j + "'>" + mat[i][j] + "</td>"
                            }
                        }
                        else{
                            if (mat[i][j] > 0) {
                                html += "<td class='white' data-pos='" + i + "," + j + "'>" + mat[i][j] + "</td>"
                            } else {
                                html += "<td class='black' data-pos='" + i + "," + j + "'>" + mat[i][j] + "</td>"
                            }
                        }
                    }

                    html += "</tr>";
                }
                ccTbl.innerHTML = html;
            }
        };

        this.associateEditableEvents = function(){
            let editableCells =  document.querySelectorAll("td[contenteditable='true']");

            for(let i = 0; i < editableCells.length; i++){
                editableCells[i].addEventListener('input', function(e){
                    if (parseInt(e.target.textContent) > 0) {
                        e.target.classList.remove('black');
                        e.target.classList.add('white');
                        coord = e.target.dataset.pos.split(",");
                        row = coord[0];
                        col = coord[1];

                        me.mat[row][col] = parseInt(e.target.textContent);
                    } else {
                        e.target.classList.remove('white');
                        e.target.classList.add('black');
                        coord = e.target.dataset.pos.split(",");
                        row = coord[0];
                        col = coord[1];

                        me.mat[row][col] = parseInt(e.target.textContent);
                    }
                })
            }
        }

        this.firstPass = function (mat, connectivity) {
            let i, j, label;
            var labels = [];

            if (typeof (connectivity) == "undefined") connectivity = 8;

            for (i = 1; i < mat.length - 1; i++) {
                for (j = 1; j < mat[i].length - 1; j++) {
                    if (mat[i][j] != 0) {
                        if (mat[i][j - 1] > 0) label = mat[i][j - 1];
                        else if (mat[i - 1][j] > 0) label = mat[i - 1][j];
                        else if (connectivity == 8) {
                            if (mat[i - 1][j - 1] > 0) label = mat[i - 1][j - 1];
                            else if (mat[i - 1][j + 1] > 0) label = mat[i - 1][j + 1];
                            else {
                                label = labels.length + 1
                                labels.push(label)
                            }
                        } else {
                            label = labels.length + 1
                            labels.push(label)
                        }
                        mat[i][j] = label
                    }
                }
            }

            return mat;
        };

        this.fpClickHandler = function () {
            var connectivityEl = document.querySelector("input[name='connectivity']:checked");
            fp_mat = me.firstPass(me.mat, connectivityEl.value);
            me.displayTable(fp_mat, "connected-component-fp");
        };

        this.init = function () {
            this.mat = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ];

            this.displayTable(this.mat, "connected-component-in");

            this.associateEditableEvents();

            var fpBtn = document.querySelector(".connected-component .cc__fp");
            fpBtn.addEventListener("click", me.fpClickHandler);

        };

        this.init();
    }

    px.ccinit();
})(document, window, 0)