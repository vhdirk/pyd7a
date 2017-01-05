define([
    "app",
    "models/modem",
    "models/files",
],function(app, modem, files){
    var ui = {
        rows:[
            { view: "toolbar", css: "highlighted_header header1", height: 40, cols: [
                {template: "Files"}
            ]},
            {
                cols: [
                    {
                        view:"datatable",
                        id:"file_list",
                        columns:[
                            {id:"file_id", header:"ID", sort:"int"},
                            {id:"file_name", header:"Filename", fillspace:true},
                            {id:"data", header:"data", fillspace:true}
                        ],
                        data:files.data,
                        on:{
                            'onItemClick':function(id){
                               modem.read_file(this.getItem(id).file_id);
                            }
                        }
                    },
                    {template:"#file_data#", id:"file_data", data:{"file_data":""}}
                ]
            }

        ]
    };

	return {
		$ui: ui,
		$menu: "top:menu",
	};
});