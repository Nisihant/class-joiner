ml = false;
tool = false;

function all_ml_projects() {
    if(ml)return;
    const ele = $('#ml_box');
    
    var url = "/apis/AllMlProjects";

    $.get(url, {},
        function (data, status) {
            if(data.length == 0 || !data)return;
            data = JSON.parse(data)
            for (const opt in data) {
                const page = data[opt];
                var li = document.createElement("LI");
                var a = document.createElement("A");
                a.innerText = opt;
                a.href = page;
                li.append(a);
                ele.append(li);
            }
            ml = true;
        })
}


function all_tool_projects() {
    if(tool)return;
    const ele = $('#tool_box');

    var url = "/apis/AllToolBox";

    $.get(url, {},
        function (data, status) {
            if(data.length == 0 || !data)return;
            data = JSON.parse(data)
            for (const opt in data) {
                const page = data[opt];
                var li = document.createElement("LI");
                var a = document.createElement("A");
                a.innerText = opt;
                a.href = page;
                li.append(a);
                ele.append(li);
            }
            tool = true;
        })
}