define([
    "app",
    "models/commands",
],function(app, commands){
    var ui = {
        rows:[
            {view: "toolbar", css: "highlighted_header header1", height: 40, cols: [{template: "Response"}]},
            {
                view:"list",
                id:"received_alp_commands_list",
                template: "#tag_id# - #command# - #response#",
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