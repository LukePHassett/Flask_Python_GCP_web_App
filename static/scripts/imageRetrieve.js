function getImage(){
    var location = "https://firebasestorage.googleapis.com/v0/b/ad-lab-project-1.appspot.com/o/img";
        // "%2Fcompass.jpg?alt=media&token=0104defb-c724-4a83-aff4-0cae0c40f4d0";

    var file = 'compass.jpg';
    // var token =location.accessToken("token");

    firebase.auth()

    token = fetch(location+file);

    return location+file+token;
}