define([],function(){

	var commands = new webix.DataCollection({ data:[
	]});

	return {
		data: commands,
		$oninit:function(){
		},

		add_request:function(tag_id, command){
			// TODO assert tag_id does not exist yet
			commands.add({'id': tag_id, 'command': command, 'response': null});
		},

		add_response:function(tag_id, command_response){
			if(commands.exists(tag_id)){
				commands.getItem(tag_id).response = command_response;
				commands.updateItem(tag_id);
			} else {
				commands.add({'id': tag_id, 'command': null, 'response': null});
			}
		}
	};
});