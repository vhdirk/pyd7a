define([
	"models/commands",
	"models/modem",
	"views/command_log"
],function(commands_model, modem, command_log){

	var ui = {
		rows:[
			{ cols:[
				{ view:"tabview", cells:
					[{
						header: "Execute Command",
						body: {
							view:"form", id:"execute_command_form", elements:[
								{ template:"Read file", type:"section" }, // TODO other operations
								{ view:"text", label:'file ID', validate:webix.rules.isNumber, name:"file_id", value: "0" },
								{ view:"text", label:'offset', validate:webix.rules.isNumber, name:"offset", value: "0" },
								{ view:"text", label:'length', validate:webix.rules.isNumber, name:"length", value: "8" },
								{
									view:"select", label:"Interface", value: 0, name:"interface", options:[
										{id:0, value:"HOST"},
										{id:0xD7, value:"D7ASP"}
									],
									on:{
										onChange: function(value){
											if(value == 0xD7) {
												$$("d7asp_interface").show();
											} else {
												$$("d7asp_interface").hide();
											}
										}
									}
								},
								{ view:"fieldset", id:"d7asp_interface", label:"D7ASP Interface Configuration", hidden: true, body:{
									rows:[
										{ template:"QoS", type:"section" },
										{view:"select", label:"Response mode", value: 1, name:"qos_response_mode", options:"/responsemodes"},
										{ template:"Addressee", type:"section" },
										{ view:"text", label:"Access Class", value: "0", validate:webix.rules.isNumber, name:"access_class"},
										{ view:"select", label:"IdType", value: 1, name:"id_type", options:"/idtypes" },
										{ view:"text", label:"ID", validate:webix.rules.isNumber, name:"id", value:"0"},

									]
								}},
								// interface config
								// operation
								// file
								{ view:"button", type:"form", value:"Execute",
									click:function () {
										var form = $$("execute_command_form");
										if(form.validate()) {
											// TODO post?
											console.log(form.getValues());
											modem.execute_command(form.getValues(), function(data){
												console.log("server response: " + JSON.stringify(data));
											})
											// socket.emit('execute_command', form.getValues(), function(data){
											// 	console.log("server response: " + JSON.stringify(data));
											// });
										}
									}
								}
							]
						}
					},
					{
						header: "Read system file",
						body: {
							view:"form", id:"read_local_system_file_form", elements:[
								{ view:"select", label:"System file", value: 0, name:"system_file_id", options:"/systemfiles"},
								{ view:"button", type:"form", value:"Read file",
									click:function () {
										var form = $$("read_local_system_file_form")
										if(form.validate()) {
											// TODO post?
											console.log(form.getValues())
											socket.emit('read_local_system_file', form.getValues())
										}
									}
								}
							]
						}
					},
					{
						header: "Execute raw ALP command",
						body: {
							view:"form", id:"execute_raw_alp_form", elements:[
								{ view:"text", "label":"Raw ALP command", "placeholder":"Raw ALP command", name:"raw_alp"},
								{ view:"button", type:"form", value:"Execute",
									click:function () {
										var form = $$("execute_raw_alp_form")
										if(form.validate()) {
											// TODO post?
											console.log(form.getValues())
											socket.emit('execute_raw_alp', form.getValues());
										}
									}
								}
							]
						}
					}]
				},
				{template:"col 2"}
			]},
			command_log
		]
	};

	return {
		$ui: ui,
		$oninit:function(){
			//view.parse(records.data);
		}
	};
	
});
