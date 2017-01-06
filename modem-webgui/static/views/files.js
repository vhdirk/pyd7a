define([
    "app",
    "models/modem",
    "models/files",
],function(app, modem, files){
    function showFileDetail(file){
		console.log("show detail: " + file.file_id);
		$$("file_data").parse({'file_data': file.data});
    }

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
                            {id:"file_name", header:"Filename", fillspace:true}
                        ],
                        data:files.data,
                        on:{
                            'onItemClick':function(id){
                               modem.read_file(this.getItem(id).file_id);
                                showFileDetail(this.getItem(id));
                            }
                        }
                    },
                    {template:"#file_data#", id:"file_data", data:{"file_data":""}}
                ]
            }

        ]
    };

    function onInit() {
        // make sure changes to the file are updated in the file details pane, update the UI after details have been received.
        // TODO check if we can get this through databinding, like it is used for the datatable.
        files.data.attachEvent("onDataUpdate", function(id, obj){
            showFileDetail(files.data.getItem(id));
            return true;
        });

    }

	return {
		$ui: ui,
		$menu: "top:menu",
        $oninit: onInit()
	};
});