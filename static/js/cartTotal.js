window.onload = function(){
    let itemTotals = document.getElementsByClassName('item-total')
    let totalCost = 0
    for (i = 0; i < itemTotals.length; i++){
        let cost = itemTotals[i].innerText
        totalCost = totalCost + parseFloat(cost)
    }
    document.getElementById("total").innerText = totalCost
    
}