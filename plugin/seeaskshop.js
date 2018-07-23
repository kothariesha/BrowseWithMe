var images = [];
var current_images = [];
var num_images = 0;
var zoom_factor = 2;
var image_id = 0;


chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
     var url = tabs[0].url;
     get_data(url);

});


function get_data(a){
  a=a.replace("https","http");
  $('#message').html("Processing...");
    $.ajax({
        //url:'http://127.0.0.1:5000/seeaskshop',
        url:'http://192.155.86.85:5000/seeaskshop',
        data:{
         url:a
        },
        type:"GET",
        dataType:"json",
        success: function (data) {
            $('#message').html("");
            run_plugin(data);
        },
        error: function(){
          // will fire when timeout is reached
          $('#message').html("Error");
          setTimeout(function(){
            $('#message').html("");
          }, 2000);
        },
        timeout: 20000
    });
    //$('#message').html(a);
}


function run_plugin(data)
{
  images = data;
  num_images = images.length;

  for(i=0; i<num_images;i=i+1)
  {
    current_images.push(i);
  }

  var img = new Image();
  img.src = images[current_images[image_id]].url;
  img.onload = function() {
    draw(this);
  }

  document.getElementById('mysearch').addEventListener("keyup",search_entered);
  document.addEventListener("keyup",space);

}

var space = function(event)
{
  const keyCode = event.keyCode;
  if (keyCode == 17){
    startDictation();
  }
  if (keyCode == 16){
    document.getElementById('mysearch').value ="";
    document.getElementById('mysearch').focus();
  }
  console.log("Inside function space..")
}


function zoom_image(item){
  if (item in images[current_images[image_id]].info)
  {
     var box_coordinates = images[current_images[image_id]].info[item].box;
     console.log(box_coordinates);
     var canvas = document.getElementById('canvas');

     var zoomctx_canvas = document.getElementById('zoom')
     var zoomctx = zoomctx_canvas.getContext('2d');
     zoomctx.clearRect(0, 0, zoomctx_canvas.width, zoomctx_canvas.height);

     x = box_coordinates[0];
     y = box_coordinates[1];
     w = box_coordinates[2] - box_coordinates[0];
     h = box_coordinates[3] - box_coordinates[1];
     zoomctx_canvas.width = zoom_factor*w;
     zoomctx_canvas.height = zoom_factor*h;
     zoomctx.drawImage(canvas,x,y,w,h,0,0,zoom_factor*w,zoom_factor*h);
   }
}

function answer(question)
{
  console.log(question);
  var ans = '';
  var str = question.split(" ");
  var cloth_item = str[0]
  var cloth_attribute = str[1]

    if (question == "describe image")
    {
      images_items = images[current_images[image_id]].items
      ans = "This image has ".concat(images_items);
    }
    else if (cloth_item == "dress"|| cloth_item == "skirt"||cloth_item=="top"
            ||cloth_item=="pant"||cloth_item=="pants"||cloth_item=="hat"
            ||cloth_item=="sunglasses" ||cloth_item=="scarf"||cloth_item=="bag")
    {
       if(cloth_attribute =="color"||cloth_attribute=="pattern"
          ||cloth_attribute=="length"||cloth_attribute=="colors")
       {
         console.log(str);
         if (cloth_attribute=="colors")
         {
           cloth_attribute="color";
         }
         if(cloth_item=="pant")
         {
           cloth_item=="pants"
         }

         ans =images[current_images[image_id]]['info'][cloth_item][cloth_attribute];
         console.log(images[current_images[image_id]]['info'])
         zoom_image(cloth_item);
       }
     }
     else if (question=="price")
     {
      ans =images[current_images[image_id]]['price'] + " of " + images[current_images[image_id]]['title'];
     }
     else if (question == "details" || question=="detail")
     {
      ans = images[current_images[image_id]]['details'];
     }
     else if (question =="title")
     {
      ans = images[current_images[image_id]]['title'];
     }
     else if (question =="material")
     {
      ans = images[current_images[image_id]]['material'];
     }
     else
     {
       ans = 'Dont know'
     }

   //responsiveVoice.speak(ans);
   var utterance = new SpeechSynthesisUtterance(ans);
   window.speechSynthesis.speak(utterance);

}

function startDictation() {
  if (window.hasOwnProperty('webkitSpeechRecognition')) {
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(e) {
      var question = e.results[0][0].transcript;
      console.log(question);
      recognition.stop();
      document.getElementById("mysearch").value = question;
      answer(question);
     };

    recognition.onerror = function(e) {
      console.log("This is not working")
      recognition.stop();
    }
  }
}


function search_entered(event){
  const keyCode = event.keyCode;
  if(keyCode == 13){
    var question = document.getElementById("mysearch").value;
    var utterance = new SpeechSynthesisUtterance(question);
    window.speechSynthesis.speak(utterance);
    //responsiveVoice.speak(question);
    answer(question);
    console.log(question);
  }

}

function draw(img) {

  console.log(images[current_images[image_id]]);

  var image_width = images[current_images[image_id]].width;
  var image_height = images[current_images[image_id]].height;

  //var image_width = 217;
  //var image_height = 326;

  var canvas = document.getElementById('canvas');
  var ctx = canvas.getContext('2d');


  var zoomctx_canvas = document.getElementById('zoom')
  var zoomctx = zoomctx_canvas.getContext('2d');

  canvas.width = image_width;
  canvas.height = image_height;
  zoomctx_canvas.width = image_width;
  zoomctx_canvas.height = image_height;

  ctx.drawImage(img, 0, 0, image_width, image_height);
  img.style.display = 'none';

  zoomctx.clearRect(0, 0, zoomctx_canvas.width, zoomctx_canvas.height);
}
