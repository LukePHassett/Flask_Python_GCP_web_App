function includeSQR() {
  var z, i, elmnt, file, xhttp;
  /* Loop through a collection of all HTML elements: */
  z = document.getElementsByTagName("*");
  for (i = 0; i < z.length; i++) {
    elmnt = z[i];
    /*search for elements with a certain atrribute:*/
    file = elmnt.getAttribute("include-sqr");
    if (file) {
      /* Make an HTTP request using the attribute value as the file name: */
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          if (this.status == 200) {elmnt.innerHTML = this.responseText;}
          if (this.status == 404) {elmnt.innerHTML = "Page not found.";}
          /* Remove the attribute, and call this function once more: */
          elmnt.removeAttribute("include-html");
          document.getElementsByTagName("head")[0].insertAdjacentHTML(
    "beforeend",
    "<link rel=\"stylesheet\" href=\"static/styles/styling.css\" />");
          includeSQR();
        }
      }
      xhttp.open("GET", file, true);
      xhttp.send();
      /* Exit the function: */
      return;
    }
  }
}

function cleanHTML(file) {
  var z,i, elmnt, xhttp;

  z = document.getElementById("*")
  for(i = 0; i < z.length; i++) {
    elmnt = z[i];
  }
}

// function includeCSS() {
//   if(document.createStyleSheet) {
//   document.createStyleSheet('/static/styles/navBar.css');
// }
// else {
//   var styles = "@import url(' http://server/stylesheet.css ');";
//   var newSS=document.createElement('link');
//   newSS.rel='stylesheet';
//   newSS.href='data:text/css,'+escape(styles);
//   document.getElementsByTagName("head")[0].appendChild(newSS);
// }
// }