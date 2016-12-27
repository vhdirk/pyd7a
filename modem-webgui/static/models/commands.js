define([],function(){

	var commands = new webix.DataCollection({ data:[
	]});

	return {
		data: commands,
		$oninit:function(){
		},

		add_request:function(tag_id, command){
			// TODO assert tag_id does not exist yet
			commands.add({'id': tag_id, 'tag_id': tag_id, 'command': command, 'response': null});
			// use tag_id for id field so we can use tag_id directly in for example exists() and getItem(),
			// however use tag_id field for displaying, since a id cannot be null and this would result in bogus id in GUI
		},

		add_response:function(tag_id, command_response){
			if(commands.exists(tag_id)){
				commands.getItem(tag_id).response = command_response;
				commands.updateItem(tag_id);
			} else {
				commands.add({'tag_id': tag_id, 'command': null, 'response': null}); // id will be generated
			}
		}
	};
});