(function edit(){
    'use-strict';

    var td = document.getElementsByClassName('td');
    var open = false;
    for(var i=0;i<td.length;i++) {
        td[i].addEventListener('click', change, false);
        td[i].addEventListener('blur', changeback, false);
    }
    
    function change(open) {
        if (!open) {
            this.contentEditable = true;
            this.focus();
        }
        else{
            open = true;
            this.removeAttribute("contentEditable");
        }
    }
    function changeback() {

    }
}());