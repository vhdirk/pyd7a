define([
    "models/commands"
],function(commands){
    var ui = {
        view:"accordion",
        rows:[
            {
                header: "Received ALP commands",
                body: {
                    view:"list",
                    id:"received_alp_commands_list",
                    template: "#id# - #command# - #response#",
                    data:commands.data
                }
            }
        ]
    }

	return {
		$ui: ui,
		$menu: "top:menu"
	};
});