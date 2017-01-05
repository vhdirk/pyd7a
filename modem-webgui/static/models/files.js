define([],function(){

	var files = new webix.DataCollection({
		url: '/systemfiles'
	});

	return {
		data: files,

		update_file:function(file_id, data){
			files.data.each(function(file){
				if(file.file_id == file_id){
					console.log(file);
					file.data = data;
					files.updateItem(file.id);
				}
			});
		}
	};
});