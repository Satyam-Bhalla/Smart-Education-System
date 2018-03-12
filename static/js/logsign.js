$('.form').find('input, textarea').on('keyup blur focus', function (e){
  var $this = $(this),
      label = $this.prev('label');
	  if (e.type === 'keyup'){
			if ($this.val() === ''){
          label.removeClass('active highlight');
        }else{
          label.addClass('active highlight');
        }
    }else if (e.type === 'blur'){
    	if( $this.val() === '' ){
    		label.removeClass('active highlight'); 
			}else{
		    label.removeClass('highlight');   
			}   
    }else if (e.type === 'focus'){ 
      if( $this.val() === '' ){
    		label.removeClass('highlight'); 
			}else if( $this.val() !== '' ){
		    label.addClass('highlight');
			}
    }
});

$('.tab a').on('click', function (e) {
  e.preventDefault();
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  target = $(this).attr('href');
  $('.tab-content > div').not(target).hide(); 
  $(target).fadeIn(600);
});

document.getElementById('signform').onsubmit = function(){
  if(document.getElementById('spassword').value != document.getElementById('cpassword').value){
    document.getElementById('cperror').style.display = "block";
    return false;
  }else{
    document.getElementById('cperror').style.display = "none";
  }
  if(document.getElementById('srole').value == "0"){
    document.getElementById('srerror').style.display = "block";
    return false;
  }else{
    document.getElementById('srerror').style.display = "none";
  }
  return true;
}

document.getElementById('logform').onsubmit = function(){
  if(document.getElementById('lrole').value == "0"){
    document.getElementById('lrerror').style.display = "block";
    return false;
  }else{
    document.getElementById('lrerror').style.display = "none";
  }
  return true;
}