define([
    "app",
    "models/modem",
    "models/files",
],function(app, modem, files){
    function showFileDetail(file){
		console.log("show detail: " + file.file_id);
		$$("file_details_title").parse({'file_name': file.file_name, 'file_id': file.file_id});

        // dynamically load form based on filename
        var filename = file.file_name;
        if(filename.startsWith("ACCESS_PROFILE"))
            filename = "access_profile"; // remove access specifier

        app.show("/top/files/file_" + filename.toLowerCase());
        $$('file_contents_form').setValues(file); // TODO forms for all files now have the same id, find a better way
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
                        select: true,
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
                    {
                        rows: [
                            {
                                view: "toolbar" ,css: "highlighted_header header1", height: 40, cols: [
                                    {id: "file_details_title", template: "File details - #file_name# (#file_id#)",
                                        data: {"file_name": "", "file_id": ""}}
                                ]
                            },
                            { $subview: true }
                        ]
                    }

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
        $oninit:onInit()
	};
});