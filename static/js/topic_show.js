$(document).ready(function(){

    var text = function(){
         var content = $('.topic-content')
         var t_temp = content.text().replace(/\n/g,'<br>').replace(/\s/g,'&nbsp;').replace(/\t/g,'&nbsp;')
             content.html(t_temp)
         }

    }
    text()

})
