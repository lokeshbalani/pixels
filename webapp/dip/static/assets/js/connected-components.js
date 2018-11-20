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

        this.displayTable = function(mat){
            let ccTbl = document.querySelector("#connected-component-grid tbody");

            let html = "",
                i,j;

            for(i = 0; i < mat.length; i++){
                html += "<tr>";

                for(j = 0; j < mat[i].length; j++){
                    if(mat[i][j] == 1){
                        html += "<td class='white' data-pos='"+i+","+j+"'>"+mat[i][j]+"</td>"
                    } else{
                        html += "<td class='black' data-pos='"+i+","+j+"'>"+mat[i][j]+"</td>"
                    }
                }

                html += "</tr>";
            }
            ccTbl.innerHTML = html;
        };

        this.init = function(){
            var mat = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0],
            [0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0],
            [0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0],
            [0,0,1,1,1,1,0,0,0,1,1,1,0,0,1,1,0],
            [0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0],
            [0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0],
            [0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ];

            this.displayTable(mat);
        };

        this.init();
    }

    px.ccinit();
})(document, window, 0)