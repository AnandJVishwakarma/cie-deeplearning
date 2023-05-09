// let uploadButton = document.getElementById("imageUpload");

// let chosenImage = document.getElementById("chosen-image");
// let fileName = document.getElementById("file-name");

// uploadButton.onchange = () => {
//     let reader = new FileReader();
//     reader.readAsDataURL (uploadButton.files[0]); 
//     console.log(uploadButton.files[0]); 
//     reader.onload = ()  => {
//     chosenImage, setAttribute("src", reader.result);

//     }
//     fileName.textContent = uploadButton.files[0].name; 

// }


//Windy
const options = {
    // Required: API key
    key: '4yG3lcWqeuDQQTDa2TxeVNN674TrmBDe', // REPLACE WITH YOUR KEY !!!

    // Put additional console output
    verbose: false,

    // Optional: Initial state of the map
    lat: 15,
    lon: 81.8262,
    zoom: 5,
};

// Initialize Windy API

windyInit(options, windyAPI => {
    // windyAPI is ready, and contain 'map', 'store',
    // 'picker' and other usefull stuff

    const {map}  = windyAPI;
    // .map is instance of Leaflet map
    document.getElementById("map-button").addEventListener("click", function(){
        let lat = document.getElementById("Lat").value;
        let lng = document.getElementById("Lng").value;
        map.panTo(new L.LatLng(lat, lng));
        L.popup()
        .setLatLng(new L.LatLng(lat, lng))
        .setContent('Latitude: ' + lat + '  Longitude: '  + lng)
        .openOn(map);
    });
});




$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });



    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },
        });
    });

});