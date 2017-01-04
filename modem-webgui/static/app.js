define([
	"libs/webix-mvc-core/core",
	"libs/webix-mvc-core/plugins/menu",
], function(core, menu){
	var app = core.create({
		id:			"oss7-modem-webgui",
		name:		"OSS-7 Modem webgui",
		version:	"0.0.1",
		debug:		true,
		start:		"/top/commands"
	});

	app.use(menu);

	return app;
});