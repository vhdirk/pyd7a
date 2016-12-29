define([], function(){
    var ui = {
        rows: [
            {view: "toolbar", css: "highlighted_header header3", height: 40, cols: [{template: "Command Log"}]},
            {id:"cmd_response", template:"#cmd_string#"}
        ]
    };

    return {
        $ui: ui
    };
});

