document.addEventListener('DOMContentLoaded', function() {

    // Add an event listener on all +/- cart Buttons
    var btn_p = document.getElementsByClassName("btn-p");
    var btn_m = document.getElementsByClassName("btn-m");
    for (var i=0; i<btn_p.length; i++) {
        btn_p[i].addEventListener('click', qtyChange_clicked);
        btn_m[i].addEventListener('click', qtyChange_clicked);
    }
});

function qtyChange_clicked(e) {
    const btn = e.target;
    
    // Get the article id that has been clicked on
    const article_Id=btn.dataset.id;

    // Get the UI elements that eventually will be needed later
    const cartArticleQty = document.getElementById(`cartQty_${article_Id}`);
    const totalPrice = document.getElementById(`totalPrice_${article_Id}`);
    const price = document.getElementById(`price_${article_Id}`);
    const grandTotal = document.getElementById('grandTotal');
    const cartCounter = document.getElementById('cartCounter');
    const containers = document.getElementsByClassName(`container_${article_Id}`);

    // Check which button has been clicked: if negative Button changeQty is -1 else is 1
    var qty = 1;
    if (btn.classList.contains("btn-m")) {
        qty = -1;
    }

    // Make the api call to change the article qty in the cart and update the UI
    // update the cart over the api
    fetch(`/cartAPI?articleId=${article_Id}&qty=${qty}`, {
        method: 'POST'
    })
    // Update the dom if success
    .then(response => {
        if (response.ok) {
            response.json()
            .then(result => {
                cartCounter.innerHTML = result.cartQty;
                if (result.cartArticleQty != 0) {
                    cartArticleQty.innerHTML = result.cartArticleQty;
                    const oldGrandTotal = parseFloat(grandTotal.innerHTML);
                    const oldTotalPrice = parseFloat(totalPrice.innerHTML);
                    totalPrice.innerHTML = (parseFloat(price.innerHTML) * parseFloat(result.cartArticleQty)).toFixed(2);
                    grandTotal.innerHTML = (oldGrandTotal - oldTotalPrice + parseFloat(totalPrice.innerHTML)).toFixed(2);

                }
                else {
                    for (var i=containers.length-1; i>=0; i--) {
                        containers[i].remove();
                    }
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
