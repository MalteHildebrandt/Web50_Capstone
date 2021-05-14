document.addEventListener('DOMContentLoaded', function() {

    // Add an event listener on all add to cart buttons
    var addToCart= document.getElementsByClassName("addToCart");

    for (var i=0; i<addToCart.length; i++) {
        addToCart[i].addEventListener('click', addToCart_clicked);
    }

});

function addToCart_clicked(e) {
    const articleId = e.target.dataset.id;
    const qty = document.getElementById(`CartQty_${articleId}`).value;
    

    // update the cart over the api
    fetch(`/cartAPI?articleId=${articleId}&qty=${qty}`, {
        method: 'POST'
    })
    // Update the dom if success
    .then(response => {
        if (response.ok) {
            response.json()
            .then(result => {
                document.getElementById("cartCounter").innerHTML = result.cartQty;
                if (result.cartArticleQty != 0) {
                    document.getElementById(`inCartQty_${articleId}`).innerHTML = `${result.cartArticleQty} in Cart`;
                }
                else {
                    document.getElementById(`inCartQty_${articleId}`).innerHTML = '';
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

}