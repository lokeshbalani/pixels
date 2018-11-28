if (typeof (px) === "undefined") px = {};
if (typeof (px.utils) === "undefined") px.utils = {};

(function (document, window, index) {
    px.ccinit = function () {
        var ccEl = document.getElementById("connected-component");

        let init = new ConnectedComponents(ccEl)
    };

    class Group {
        constructor(head) {
            this.members = new Set();
            this.head = head;
            this.add(head);
        }
        add(member) {
            this.members.add(member);
        }
        union(other) {
            this.members = new Set([...other.members, ...this.members]);
        }
    }

    function ConnectedComponents(comp) {
        var me = this;
        this.jqcomp = jQuery(comp);

        this.colors = ["aqua", "beige", "blue", "violetblue", "brown", "chocolate", "crimson", "darkblue", "darkgrey", "darkgreen", "lightgreen", "yellow", "magenta", "pink", "indigo", "lavender", "lightgrey", "teal", "wheat"];

        this.assignColors = function (table_id) {
            var tdEls = document.querySelectorAll("#" + table_id + " td");

            for (let i = 0; i < tdEls.length; i++) {
                if (tdEls[i].textContent <= me.colors.length && tdEls[i].textContent > 0) {
                    tdEls[i].style.backgroundColor = me.colors[tdEls[i].textContent - 1];
                }
            }
        };

        this.displayTable = function (mat, container_id) {
            if (typeof (container_id) != "undefined" && container_id != "") {
                let ccTbl = document.querySelector("#" + container_id + " tbody");

                if(ccTbl.closest(".connected-component").classList.contains("hide")){
                    ccTbl.closest(".connected-component").classList.remove("hide");
                    ccTbl.closest(".connected-component").classList.add("show");
                }
                

                let html = "",
                    i, j;

                for (i = 0; i < mat.length; i++) {
                    html += "<tr>";

                    for (j = 0; j < mat[i].length; j++) {
                        if (i != 0 && i != (mat.length - 1) && j != 0 && j != (mat[i].length - 1)) {
                            if (mat[i][j] > 0) {
                                html += "<td class='white' contenteditable='true' data-pos='" + i + "," + j + "'>" + mat[i][j] + "</td>"
                            } else {
                                html += "<td class='black' contenteditable='true' data-pos='" + i + "," + j + "'>" + mat[i][j] + "</td>"
                            }
                        } else {
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

        this.associateEditableEvents = function () {
            let editableCells = document.querySelectorAll("td[contenteditable='true']");

            for (let i = 0; i < editableCells.length; i++) {
                editableCells[i].addEventListener('input', function (e) {
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
            me.connectivity = connectivityEl.value;
            me.fp_mat = me.firstPass(me.mat, me.connectivity);
            me.displayTable(me.fp_mat, "connected-component-fp");
            me.assignColors("connected-component-fp");
        };

        this.getnodeLabelPairs = function (mat, connectivity) {
            let all_labels = [];
            let pairs_collected = [];

            for (i = 1; i < mat.length - 1; i++) {
                for (j = 1; j < mat[i].length - 1; j++) {
                    let current_label = mat[i][j];

                    if (current_label != 0) {
                        all_labels.push([current_label, current_label]);

                        if (mat[i - 1][j] > 0 && mat[i - 1][j] != current_label) {
                            let top_label = mat[i - 1][j];

                            if (!pairs_collected.includes([current_label, top_label]) && !pairs_collected.includes([top_label, current_label])) {
                                pairs_collected.push([current_label, top_label]);
                            }
                        }

                        if (connectivity == 8) {
                            if (mat[i - 1][j + 1] > 0 && mat[i - 1][j + 1] != current_label) {
                                let label_45 = mat[i - 1][j + 1];

                                if (!pairs_collected.includes([current_label, label_45]) && !pairs_collected.includes([label_45, current_label])) {
                                    pairs_collected.push([current_label, label_45]);
                                }
                            }
                        }
                    }
                }
            }

            pairs_collected.concat(all_labels);

            return pairs_collected;
        };

        this.unionFind = function (mat, connectivity) {
            let pairs_collected = me.getnodeLabelPairs(mat, connectivity);

            let groups = {};

            for (let i = 0; i < pairs_collected.length; i++) {
                let head = pairs_collected[i][0];

                if (!(head in groups)) {
                    var group = new Group(head);
                    groups[head] = group;
                } else {
                    group = groups[head];
                }

                let node = pairs_collected[i][1];

                if (!(node in groups)) {
                    group.add(node);
                    groups[node] = group;
                } else if (!(head in groups[node].members)) {
                    //merge two groups
                    let new_members = groups[node];
                    group.union(new_members);

                    for (let migrate of new_members.members) {
                        groups[migrate] = group;
                    }
                }
            }

            return groups;
        };

        this.secondPass = function () {
            let groups = me.unionFind(me.fp_mat, me.connectivity);

            let tree = [];
            var sp_mat = me.fp_mat;

            for (let [key, value] of Object.entries(groups)) {
                if (key == value.head) {
                    tree.push([...value.members]);
                }
            }

            for (let m = 0; m < tree.length; m++) {
                    for (let i = 1; i < sp_mat.length - 1; i++) {
                        for (let j = 1; j < sp_mat[i].length - 1; j++) {
                            if(tree[m].includes(sp_mat[i][j])) sp_mat[i][j] = tree[m][0];
                        }
                    }
               
            }

            me.sp_mat = sp_mat;
        };

        this.spClickHandler = function () {
            me.secondPass();
            me.displayTable(me.sp_mat, "connected-component-sp");
            me.assignColors("connected-component-sp");
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

            var spBtn = document.querySelector(".connected-component .cc__sp");
            spBtn.addEventListener("click", me.spClickHandler);

        };

        this.init();
    }

    px.ccinit();
})(document, window, 0)