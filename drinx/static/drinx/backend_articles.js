document.addEventListener('DOMContentLoaded', function() {

    // Add an event listener on all article entries
    var articleEntries = document.getElementsByClassName("article");

    for (var i=0; i<articleEntries.length; i++) {
        articleEntries[i].addEventListener('click', article_clicked);
    }

    // Add an event listener to the form
    document.getElementsByTagName("FORM")[0].addEventListener('submit', form_submitted);

    // Add an event listener for changed filename
    document.getElementById("formImageSelect").addEventListener('change', image_changed);
  

});

function article_clicked(e) {
    // get the id of the article that has been clicked on
    const id = e.target.dataset.id;

    // load the data of this article over the api
    fetch(`/articleAPI?article_id=${id}`, {
        method: 'GET'
    })
    // Update the dom if success
    .then(response => {
        if (response.ok) {
            response.json()
            .then(result => {
                //update the fields of the form with the reply
                document.getElementById('formArticleName').value = result.fields.name;
                document.getElementById('formContentQty').value = result.fields.content_qty;
                document.getElementById('formArticleDescriptionShort').value = result.fields.description_short;
                document.getElementById('formDescription').value = result.fields.description;
                document.getElementById('formPackageQty').value = result.fields.package_qty;
                document.getElementById('formPrice').value = result.fields.price;
                document.getElementById('formStock').value = result.fields.stock;
                document.getElementById('formImageSelect').value = "";

                const displayImg = document.getElementById('formImageDisplay')
                displayImg.src = `${displayImg.dataset.media}${result.fields.image}`;

                if(result.fields.is_active) {
                    document.getElementById('formIs_active').checked = true;
                }
                else {
                    document.getElementById('formIs_active').checked = false;
                }
                document.getElementById('formStock').value = result.fields.stock;
                
                const unit = document.getElementById('formContentUnit');
                for(var i = 0; i < unit.length; i++){
                    unit[i].selected = false;
                }
                document.getElementById(`unit_${result.fields.content_qty_unit}`).selected = true;

                const categories = document.getElementById('formCategories');
                for(var i = 0; i < categories.length; i++){
                    categories[i].selected = false;
                }
                for(var i = 0; i< result.fields.categories.length; i++){
                    document.getElementById(`category_${result.fields.categories[i]}`).selected = true;
                }
                
                const editForm = document.getElementsByClassName("editArticle")[0].style.visibility = "visible";
                
                
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
    

}

function form_submitted() {
    alert("clicked");
}

function image_changed(e) {
    const displayImg = document.getElementById('formImageDisplay');
    var file = e.target.files[0];
    var reader = new FileReader();
    reader.onload = function() {
            displayImg.src = reader.result;
    }
    reader.readAsDataURL(file);

    //const displayImg = document.getElementById('formImageDisplay');
    //const selectImg = document.getElementById('formImageSelect');
    //displayImg.src = selectImg.value;
}