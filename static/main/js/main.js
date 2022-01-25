/* Javascript for main content */


function closeMessage(argument) {
    document.getElementById("close-message").style.display="none";
}
var dropdown=false;//*states whether the dropdown is shown or hidden
function dropdown_toggle(){
    if(dropdown){
        document.getElementById("custom-dropdown-menu").style.display="none";
        dropdown=false
        }
        else{
            document.getElementById("custom-dropdown-menu").style.display="block";
            dropdown=true
        } 
}
navbar=false;//*states whether the navbar is shown or hidden
function navbar_toggle(){
    if(navbar){
        document.getElementById("navbarToggle").style.display="none"
        navbar=false
    }
    else{
        document.getElementById("navbarToggle").style.display="block"
        navbar=true
    }
}
var prev_id=null;
function filter(id){
    elem=$('.'+id) 
    $('.dropdown-toggle').text(id.charAt(0).toUpperCase()+id.substring(1)+' Posts')
    if(id=="all"){
        $('.approved').css({display:"block"})
        $('.pending').css({display:"block"})
        $('.rejected').css({display:"block"})
    }
    if(id=="approved"){
        $('.'+id).css({display:"block"})
        $('.pending').css({display:"none"})
        $('.rejected').css({display:"none"})
    }
    if(id=="pending"){
        $('.'+id).css({display:"block"})
        $('.approved').css({display:"none"})
        $('.rejected').css({display:"none"})
    }
    if(id=="rejected"){
        $('.'+id).css({display:"block"})
        $('.approved').css({display:"none"})
        $('.pending').css({display:"none"})
    }
}