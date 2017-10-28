(function ($) {
 "use strict";
    
/*-----------------------------
	Menu Stick
---------------------------------*/
    $(window).on('scroll',function() {
        if ($(this).scrollTop() > 1){  
            $('.sticker').addClass("stick");
        }   
        else{
            $('.sticker').removeClass("stick");
        }
    });
	
/*----------------------------
    Wow js active
------------------------------ */
    new WOW().init();
    
/*----------------------------
    jQuery MeanMenu
------------------------------ */
	jQuery('nav#dropdown').meanmenu();	
    
/*----------------------------
    About Carousel
------------------------------ */  
    $('.about-carousel').owlCarousel({
        autoPlay: false, 
        smartSpeed: 2000,
        fluidSpeed: true,
        dotData:true,
        items : 1,
        responsiveClass:true,
        responsive:{
            0:{
                items:1
            },
            480:{
                items:1
            },
            768:{
                items:1
            }
        }        
    });     
    
/*----------------------------
    Featured Carousel
------------------------------ */  
    $('.featured-carousel').owlCarousel({
        autoPlay: false, 
        smartSpeed: 2000,
        fluidSpeed: true,
		nav:true,
		navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
        items : 1,
        responsiveClass:true,
        responsive:{
            0:{
                items:1
            },
            480:{
                items:1
            },
            768:{
                items:1
            }
        }        
    });     
/*----------------------------
    Single Item Carousel
------------------------------ */  
    $('.single-item-carousel').owlCarousel({
        autoPlay: false, 
        smartSpeed: 2000,
        fluidSpeed: true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1 // from 0px up to 479px screen size 
            },
            480:{
                items:1, // from 480 to 677 
                nav:false // from 480 to max 
            },
            678:{
                items:1, // from this breakpoint 678 to 959
            },
            960:{
                items:2, // from this breakpoint 960 to 1199
            },
            1200:{
                items:3,
                loop:false,
            }
        }        
    }); 
    
/*---------------------
    testimonial-curosel
--------------------- */
	$('.testimonial-carousel').owlCarousel({
		loop:true,
		margin:0,
		nav:true,
		animateOut: 'slideOutDown',
		animateIn: 'zoomInLeft',		
		autoplay:false,
		smartSpeed:3000,
		navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
		responsive:{
			0:{
				items:1
			},
			600:{
				items:1
			},
			1000:{
				items:1
			}
		}
	})	
    
/*----------------------------
    Single Item Carousel
------------------------------ */  
    $('.brand-carousel').owlCarousel({
        autoPlay: false, 
        smartSpeed: 2000,
        fluidSpeed: true,
        dotData:false,
        items : 4,
        responsiveClass:true,
        responsive:{
            0:{
                items:1 
            },
            480:{
                items:2, 
                nav:false 
            },
            678:{
                items:3, 
            },
            960:{
                items:3,
            },
            1200:{
                items:4,
                loop:false,
            }
        }        
    });  
    
/*--------------------------
    ScrollUp
---------------------------- */	
	$.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    }); 	   
    
/*------------------------------------
	Textilate Activation
--------------------------------------*/
    $('.tlt').textillate({
        loop: true,
        minDisplayTime: 2500
    });
    
/*------------------------------------
	Video Player
--------------------------------------*/
    $(".player").YTPlayer({
        showControls: false
    });    
    
    $(".player-small").YTPlayer({
        showControls: true
    });
    
    $(".player-blog").YTPlayer({
        showControls: true
    });
   
/*------------------------------------
	MailChimp
--------------------------------------*/
    $('#mc-form').ajaxChimp({
        language: 'en',
        callback: mailChimpResponse,
        // ADD YOUR MAILCHIMP URL BELOW HERE!
        url: 'http://themeshaven.us8.list-manage.com/subscribe/post?u=759ce8a8f4f1037e021ba2922&amp;id=a2452237f8'
    });
    
    function mailChimpResponse(resp) {
        
        if (resp.result === 'success') {
            $('.mailchimp-success').html('' + resp.msg).fadeIn(900);
            $('.mailchimp-error').fadeOut(400);
            
        } else if(resp.result === 'error') {
            $('.mailchimp-error').html('' + resp.msg).fadeIn(900);
        }  
    }
    
/*------------------------------------
	ColorSwitcher
--------------------------------------*/
    $('.ec-handle').on('click', function(){
        $('.ec-colorswitcher').trigger('click')
        $(this).toggleClass('btnclose');
        $('.ec-colorswitcher') .toggleClass('sidebarmain');
        return false;
    });
    $('.ec-boxed,.pattren-wrap a,.background-wrap a').on('click', function(){
        $('.as-mainwrapper').addClass('wrapper-boxed');
        $('.as-mainwrapper').removeClass('wrapper-wide');
    });
    $('.ec-wide').on('click', function(){
        $('.as-mainwrapper').addClass('wrapper-wide');
        $('.as-mainwrapper').removeClass('wrapper-boxed');
    });
    
})(jQuery); 