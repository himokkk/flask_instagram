function Enter(text){ //Enter in search bar
    if(event.keyCode === 13){
        window.location.replace('http://127.0.0.1:5000/search/'+text.value);
    }
}

function Enterincomments(item){ //Enter in comments


    if(event.keyCode === 13){
        console.log($(item).attr('rows'));
        var rows = parseInt($(item).attr('rows'),10) +1;

        if(rows<3){
            $(item).attr('rows',rows);
            rows = rows + 1;
        }

    }
}

$('.add_com_button').click(function (){
    id = this.id.replace(/\D/g,'');
    var lang = $('#lang').text();
    if(lang=='pl'){var now='Teraz'}
    if(lang=='en'){var now='Now'}
    var string = $('#input'+id).val();
    const data = id+" "+string;
    if (string.length>0) {
        var username=document.getElementById('username').textContent;
        var new_com="<div style='float:left;'><a class='underline left' href='/user/"+username+"'><b>"+username+"</b></a><div class='select left comment_content'> "+string+" "+" </div></div><div class='date' id='add_date'>"+now+"</div>"
        document.getElementById('add_com'+id).innerHTML=new_com;
        $('#add_com'+id).css('margin-top','0px');
        document.getElementById('add_com'+id).style.position='static';
        $.ajax({
            url: "",
            type: "GET",
            data: {jsdata: data}
        })
    }
    $('#input'+id).val('');
});


var items = document.getElementsByClassName('date');
for(var i=0;i<items.length;i++){
    time_diff(items[i]);
}

function time_diff(time){
    var lang = $('#lang').text();
    var date =  time.textContent;
    date = parseInt(date,10);
    var now = Math.floor(Date.now()/1000);
    var diff = now-date;
    var string;
    if(diff==0){
        string='now';
    }
    else if(diff<60){
        if (diff==1){
            if(lang=='en'){string = '1 second';}
            if(lang=='pl'){string = '1 sekunda';}
        }
        else{
            if(lang=='en'){string = diff.toString() + ' seconds';}
            if(lang=='pl'){string = diff.toString() + ' secondy';}
        }
    }
    else if(diff>=60 && diff<3600) {
        var mins = Math.floor(diff/60);
        if (mins==1){
            if(lang=='en'){string = '1 minute';}
            if(lang=='pl'){string = '1 minuta';}
        }
        else{
            if(lang=='en'){string = mins.toString() + ' minutes';}
            if(lang=='pl'){string = mins.toString() + ' minuty';}
        }
    }
    else if(diff>=3600 && diff<86400 ) {
        var hours = Math.floor(diff/3600);
        if (hours==1){
            if(lang=='en'){string = '1 hour';}
            if(lang=='pl'){string = '1 godzina';}
        }
        else{
            if(lang=='en'){string = hours.toString() + ' hours';}
            if(lang=='pl'){string = hours.toString() + ' godziny';}
        }
    }
    else if(diff>=86400 && diff<604800) {
        var days = Math.floor(diff/86400);
        if (days==1){
            if(lang=='en'){string = '1 day';}
            if(lang=='pl'){string = '1 dzień';}

        }
        else{
            if(lang=='en'){string = days.toString() + ' days';}
            if(lang=='pl'){string = days.toString() + ' dni';}
        }
    }
    else if(diff>604800){
        var weeks = Math.floor(diff/604800);
        if (weeks==1){
            if(lang=='en'){string = '1 week';}
            if(lang=='pl'){string = '1 tydzień';}

        }
        else{
            if(lang=='en'){string = weeks.toString() + ' weeks';}
            if(lang=='pl'){string = weeks.toString() + ' tygodnie';}
        }
    }
    time.textContent=string;
}

$('#icon').click(function (){
    if(document.getElementById('profile').style.visibility == 'visible'){
        document.getElementById('profile').style.visibility = 'hidden';
        document.getElementById('square').style.visibility = 'hidden';
    }
    else {
        document.getElementById('profile').style.visibility = 'visible';
        document.getElementById('square').style.visibility = 'visible';
    }
});

$('html').click(function (e){
    var id=e.target.id;

    if(document.getElementById('profile')!=null) {
        if (document.getElementById('profile').style.visibility == 'visible') {
            if (id != '123' && e.target.className != 'profile') {
                document.getElementById('profile').style.visibility = 'hidden';
                document.getElementById('square').style.visibility = 'hidden';
            }
        }
    }
});

$(document).ready(function (){
    var items = document.getElementsByClassName('like_button');
    for(var i=0;i<items.length;i++){
        var id = items[i].id.replace(/\D/g,'');
        console.log(items[i].id,$('#'+items[i].id));
        if($('#liked_button'+id).length !== 0){
            $('#like_button'+id).css('visibility','hidden');
        }
    }
});

$('.like_button').click(function (){ //click hearth like
    if($(this).css('fill')==='rgb(0, 0, 0)'){
        $(this).css('fill','rgb(255, 0, 0)');
    }
    else{
        $(this).css('fill','rgb(0, 0, 0)');
    }
    id = this.id.replace(/\D/g,'');
    const data=id;
    $.ajax({
            url: "",
            type: "GET",
            data: {like: data}
    })
});

$('.photo').dblclick(function(e){ //double click photo like
    var id = this.id.replace(/\D/g,'');
    console.log(typeof ('#like_button'+id));
    $(('#liked_button'+id)).css('fill','rgb(255, 0, 0)');
    $(('#like_button'+id)).css('fill','rgb(255, 0, 0)');
    const data = this.id;
    $.ajax({
            url: "",
            type: "GET",
            data: {like_dbl: data}
    })
    /*
    var item = document.getElementById('animation'+id);
    var pos = 0;
    item.style.visibility = "visible";
    var id = setInterval(frame, 1000);
    function frame() {
    if (pos == 100) {
        item.style.visibility = "hidden";
        item.style.height=50 + "px";
        item.style.width=50 + "px";
        item.style.top=245 + "px";
        clearInterval(id);
    } else {
        pos+=1;
        item.style.height=pos/100+50 + "px";
        item.style.width=pos/100+50 + "px";
        item.style.top=245-pos/40 + "px";
    }
  }
  */
});
$(document).ready(function() {
    $(".check_data").click(function(){
        var lang = $('#lang').text();
        x = new Boolean(true);
        var email = $('#email').val();
        var name = $('#surname').val();
        var username = $('#username').val();
        var password = $('#password').val();
        var email_test = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (password.length<8 || /[a-z]/.test(password)==false || /[A-Z]/.test(password)==false || /\d/.test(password)==false){
            if(lang=='en'){$('#message').html('Password not correct. Password must contain at least 8 letters, one capital letter and one normal letter.');}
            if(lang=='pl'){$('#message').html('Niepoprawne hasło. Hasło musi mieć przynajmniej 8 znaków, jedną dużą oraz jedną małą literę.');}
            x = false;
        }
        if (username.length<5){
            x = false;
            if(lang=='en'){$('#message').html('Username not correct.');}
            if(lang=='pl'){$('#message').html('Niepoprawna nazwa użytkownika.');}
        }
        if (name.length<3 || /\d/.test(name)==true){
            x = false;
            if(lang=='en'){$('#message').html('Name not correct.');}
            if(lang=='pl'){$('#message').html('Niepoprawne imię.');}
        }
        if (email_test.test(email)==true){}
        else {
            x = false;
            if(lang=='en'){$('#message').html('Email not correct.');}
            if(lang=='pl'){$('#message').html('Niepoprawny email.');}
        }
        if (x==true){
            $('#signup_form').submit();
        }
    });
});


function submit(){
    document.getElementById(upload_profile_pic).submit();
}

$('.12345').click(function(){
    const item= $('#follow');
    const item1= $('#unfollow');
    item.css('opacity',item1.css('opacity'))
    if(item.css('opacity')==1){
        item1.css('opacity',0);
    }
    else{
        item1.css('opacity',1);
    }
    const id = $('#profile_id').text();
    $.ajax({
            url: "",
            type: "GET",
            data: {id: id}
    })
});




