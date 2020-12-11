function myFunc(vars) {
    return vars
}

function getHTML(){
    var z, i, elmnt,file, value
    var para = document.createElement("P");
    value = document.createTextNode("FUCK OFF");
    para.appendChild(value);
    // document.getElementById("holding");
    z = document.getElementsByTagName("*");

    for(i = 0; i < z.length ; i++){
        elmnt = z[i];
        file = elmnt.getAttribute("holding123");
        //value = file;
         if (file){
             return (file)
         }
         else {
             return(value)
         }
    }

    return("is broke")
}

function setHTML() {
    var para = document.createElement("P");
    var value = document.createTextNode("FUCK OFF");
}