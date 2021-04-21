function form_changed(id) {
    document.getElementById(`save_btn_${id}`).hidden = false;
}

function form_save(e, id) {
    
    // get Form data
    const saveButton = document.getElementById(`save_btn_${id}`);
    const saveForm = document.getElementById(`category_form_${id}`);
    const saveFormData = new FormData(saveForm);

    // prevent Form from actually submiting
    e.preventDefault();

    // determine which action to perform on the api
    var action = 'update';

    if (e.submitter.value === 'Delete') {
        action = 'delete';
    }

    if (e.submitter.value === 'Add') {
        action = 'insert';
    }
    
    // push it to the api
    fetch('/savecategory', {
        method: 'POST',
        body: JSON.stringify({
            action: action,
            id: saveFormData.get('id'),
            name: saveFormData.get('name'),
            description: saveFormData.get('description'),
            is_active: saveFormData.get('is_active'),
            display_order: saveFormData.get('display_order')
            })
    })
    // Update the dom if success
    .then(response => {
        if (response.ok) {
            response.json()
            .then(result => {
                //alert('dataset updated');
                saveButton.hidden = true;
                if (action === 'insert') {
                    saveButton.value ='Save';
                    saveForm.elements['id'].value = result.newid;
                }
                if (action === 'delete') {
                    const rowIndex = e.submitter.parentElement.parentElement.rowIndex;
                    e.submitter.parentElement.parentElement.parentElement.parentElement.deleteRow(rowIndex);
                }
            })
            .catch(error => {
                alert(error);
            });
        }
        else {
            alert(response.error);
        }
    })
    .catch(error => {
        alert(error);
    });
    
    return false;

}