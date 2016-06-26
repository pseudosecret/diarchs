$(document).ready(function(){

/** The JavaScript is only to make any anchor scrolls less jarring.
*** As a side note, I snagged it from here:
*** https://paulund.co.uk/SMOOTH-SCROLL-TO-INTERNAL-LINKS-WITH-JQUERY
**/

    $(document).ready(function(){
        $('a[href^="#"]').on('click',function (e) {
            e.preventDefault();
    
            var target = this.hash;
            var $target = $(target);
    
            $('html, body').stop().animate({
                'scrollTop': $target.offset().top
            }, 300, 'swing', function () {
                window.location.hash = target;
            });
        });
    });
   
});