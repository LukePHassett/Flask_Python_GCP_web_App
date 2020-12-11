function addItems(){
    var db = firebase.database();
    var newItem = {Items: "1,1,1,1,1"}

    db.ref('Basket/'+'0').set({
        Items: "1,1,1,1,1"
    })

    var addItm = {};
    // addItm['/Basket/' + newKey] = newItem;
    addItm['/Basket/'+'0'+'/'+ newKey] = newItem;

    db.update(newItem);
    return "HIT"
}

