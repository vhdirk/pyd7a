define([],function(){
    var ui = {
        type: "clean",
        rows: [
            {
                view: "form", id: "file_contents_form", complexData: true, elements: [
                    {
                        view:"text",
                        label:"Active Access Class",
                        name:"data.active_access_class",
                        disabled:true,
                        labelWidth:300 // TODO should not be necessary
                    },
                    {
                        view:"text",
                        label:"VID",
                        name:"data.vid",
                        disabled:true,
                        labelWidth:300 // TODO should not be necessary
                    },
                ]
            },
            {} // spacer
        ]
    };

	return {
		$ui: ui,
		$menu: "top:menu",
	};
});