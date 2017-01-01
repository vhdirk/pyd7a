define([
    "app",
    "models/commands",
],function(app, commands){
    var ui = {
        rows:[
            {view: "toolbar", css: "highlighted_header header1", height: 40, cols: [{template: "Command Log"}]},
            {
                view:"datatable",
                id:"received_alp_commands_list",
                columns:[
                    {id:"id", header:"Tag", sort:"int"},
                    {id:"interface", header:"Interface"},
                    {id:"command_description", header:"Request", fillspace:true},
                    {id:"response_command_description", header:"Response", fillspace:true},
                ],
                data:commands.data,
                on:{
                    'onItemClick':function(id){
                        app.callEvent("commandSelected", [this.getItem(id)]);
                    }
                }
            }
        ]
    }

	return {
		$ui: ui,
		$menu: "top:menu"
	};
});