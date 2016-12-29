define([
    "app",
    "models/commands",
],function(app, commands, modem_view){
    var ui = {
        view:"accordion",
        rows:[
            {
                header: "Received ALP commands",
                body: {
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
            }
        ]
    }

	return {
		$ui: ui,
		$menu: "top:menu"
	};
});