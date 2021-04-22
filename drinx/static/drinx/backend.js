function form_changed(e) {
    const saveForm = e.target.form;
    saveForm.elements['save'].hidden = false;   
}

function form_save(e) {
    
    // get Form data
    const saveForm = e.submitter.form;
    const saveButton = saveForm.elements['save'];
    const deleteButton = saveForm.elements['delete'];
    const saveFormData = new FormData(saveForm);

    // prevent Form from actually submiting
    e.preventDefault();

    // determine which action to perform on the api
    var action = 'update';

    // clear the popup animation class if still present from previous round
    var popup = document.getElementById("myPopup");
    popup.classList.remove("show");

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
                if (action === 'insert') {
                    //insert new empty row
                    var newForm = saveForm.cloneNode(true);
                    newForm.elements['name'].value = '';
                    newForm.elements['description'].value = '';
                    newForm.elements['is_active'].checked = false;
                    newForm.elements['display_order'].value = '';
                    saveForm.parentElement.appendChild(newForm);

                    //update the saved row
                    saveButton.value ='Save';
                    deleteButton.hidden = false;
                    saveForm.elements['id'].value = result.newid;

                }
                if (action === 'delete') {
                    saveForm.remove();
                }
                
                //show success Popup
                popup.classList.toggle("show");
                saveButton.hidden = true;
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