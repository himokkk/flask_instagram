function loadFile(event) {
    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src)
        if(this.width>=1000){
            document.getElementById("output").style.marginLeft = -200 +'px';
        }
        else {
            if(document.getElementById("output").clientWidth>800) {
                document.getElementById("output").style.marginLeft = -this.width / 2 + 'px';
            }
        }
        document.getElementById("scale").style.marginTop = '-600px';
        document.getElementById("scale").style.marginLeft = '0px';
        if(document.getElementById("output").clientHeight>600) {
            document.getElementById("scale").style.marginTop =-600-(this.height-600)/2 +'px';
        }

    }
  };

window.onload = init;
function init() {
	if (window.Event) {
	document.captureEvents(Event.MOUSEMOVE);
	}
	document.onmousemove = getCursorXY;
}
let x = 0;
let y = 0;
function getCursorXY(e) {
    x = (window.Event) ? e.pageX : event.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
	y = (window.Event) ? e.pageY : event.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
	document.getElementById('x').value = x
    document.getElementById('y').value = y
}
let moving = false;
let item = document.getElementById('scale');
let xx = 0;
let yy = 0;
item.addEventListener('mousedown', function(e){
  xx = x;
  yy = y;
  moving = true;
});

item.addEventListener('mousemove', function(e){
  if (moving === true) {
    move(xx, yy, x, y);
    xx = x;
    yy = y;
  }
});

window.addEventListener('mouseup', function(e){
  if (moving === true) {
    move(xx, yy, x, y);
    xx = 0;
    yy = 0;
    moving = false;
  }
});
var moved_x = 0;
var moved_y = 0;
var move_x = 0;
var move_y = 0;
var tempx = 0;
var tempy = 0;

function move(x1,y1,x2,y2) {
    var img = document.getElementById('output');
    var img_width = img.clientWidth;
    var img_height = img.clientHeight;
   	var width = parseInt(document.getElementById("output").clientWidth,10);
	var height = parseInt(document.getElementById("output").clientHeight,10);
	var margin_top = parseInt(document.getElementById("scale").style.marginTop,10);
	var margin_left = parseInt(document.getElementById("scale").style.marginLeft,10);
	var currenty = parseInt(document.getElementById("y").value,10);
	var currentx = parseInt(document.getElementById("x").value,10);

	move_x = -x1 + x2;
    move_y = -y1 + y2;
    margin_top = margin_top + move_y;
    margin_left = margin_left + move_x;

    if(tempx!=0 || tempy!=0){
        if(margin_left*2 > width - 600 && currentx > tempx){ //right edge
                margin_left = (width-600)/2;
            }
            if(margin_left*2 < 600 - width && currentx < tempx){ //left edge
                margin_left = -(width-600)/2;
            }
            if(margin_top<-height && currenty<tempy){ //top edge
                margin_top= -height;
            }
            if(margin_top> - 600 && currenty>tempy){ //bottom edge
                margin_top = -600;
            }
        }

    document.getElementById("scale").style.marginTop=margin_top+'px';
    document.getElementById("scale").style.marginLeft=margin_left+'px';

    tempx=parseInt(document.getElementById("x").value,10);
    tempy=parseInt(document.getElementById("y").value,10);

    var defaulty = -600;
    var defaultx = 0;
    if(height>600) {
            defaulty =-600-(img_height-600)/2;
    }

    var movedx = defaultx + margin_left;
    var movedy = defaulty - margin_top;

    document.getElementById("moved_x").value = parseInt(movedx,10);
    document.getElementById("moved_y").value = parseInt(movedy,10);
}

var sent = 0;

$('#button').click(function(){
    if(sent==0){
        console.log($('#image').val());
        if($('#image').val().length>0){
            $('#newpost_form').submit();
        }
        sent=1;
    }
});
