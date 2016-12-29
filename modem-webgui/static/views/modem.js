define([
	"models/commands",
	"models/modem",
    "views/command_request",
    "views/command_response",
    "views/command_log"
],function(commands_model, modem, command_request, command_response, command_log){
	var ui = {
		rows:[
			{ height: 49, id: "title", css: "title", template: "Command #tag_id#", data: {tag_id: ""}},
			{   type: "space",
                cols:[
				    command_request,
				    command_response
			    ]
            },
			command_log
		]
	};

	function loadCommand(command){
		console.log("load: " + command.tag_id);
		$$("title").parse({'tag_id': command.tag_id});
		$$("cmd_response").parse({'cmd_string': command.response});
	}

	return {
		$ui: ui,
		$oninit:function(){
			//view.parse(records.data);
		},

		$onevent:{
			commandSelected: function(command){
				loadCommand(command);
			}
		}
	};
	
});
