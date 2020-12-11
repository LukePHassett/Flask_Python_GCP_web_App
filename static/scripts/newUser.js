document.getElementById("RegisterForm").addEventListener("load", validateForm);

function validateForm() {
  var name = document.forms["registerForm"]["name"].value;
  var email = document.forms["registerForm"]["email"].value;
  var pass = document.forms["registerForm"]["pass"].value;

  var errors = false;
  var emessage = "";
// window.alert(emessage);
    var c1 = email.toLowerCase().indexOf('@' && '.c');
    var c2 = length(pass) < 6;
    var c3 = name == null;
    const conditions = [c1,c2,c3];

window.alert(emessage);
    if (conditions.indexOf(false) === -1) {
        if (c1) {
            emessage += "Please Enter a Valid Email Address \r \n";
            window.alert(emessage);
        }
        if (c2) {
            emessage += "Password must be more than 6 characters \r \n";
            window.alert(emessage);
        }
        if (c3) {
        emessage += "Name must be filled out \r \n"
        window.alert(emessage);
        }
    }
  if (errors){
      window.alert(emessage);
      return false;
  }
  else{
      return true;
  }
}