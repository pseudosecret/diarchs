/** The JavaScript is only to make any anchor scrolls less jarring.
*** As a side note, I snagged it from here:
*** https://paulund.co.uk/SMOOTH-SCROLL-TO-INTERNAL-LINKS-WITH-JQUERY
**/

jQuery(function(){
    $('a[href^="#"]').not('a[href="#close"]').on('click',function (e) {
        e.preventDefault()

        let target = this.hash
        let $target = $(target)

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 300, 'swing', function () {
            window.location.hash = target;
        })
    })
})