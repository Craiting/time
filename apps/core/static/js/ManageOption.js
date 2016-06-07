function newProject(){
		return  '<form action="/manage/addProject" method="get" class="form-horizontal" onsubmit="">' +
			'<label for="projectName">Project Name</label>' +
			'<input type="text" name="projectName" class="form-control" id="firstName" placeholder="Project Name" />' +

			'<label for="description">Description</label>' +
				'<input type="text" name="description" class="form-control" id="lastName" placeholder="Description" />' +
			'<input type="submit" class="btn btn-info" name="submit" value="Submit">'+
			'</form>';
}

function createEmployeeGroup(){
	return '<form action="/manage/addGroup" method="get" class="form-horizontal" onsubmit=""' +
			'<label for="name">Group Name</label>' +
				'<input type="text" name="name" class="form-control" id="name" placeholder="Group Name" />' +
			'<input type="submit" class="btn btn-info" name="Submit" value="Submit">'+
			'</form>';
}

function companySettings(){

}