(function() {
    interval = 7000;
	
	function Slideshow( element , musics ) {
		this.el = document.querySelector( element );
        this.init(musics);
    }
	
	Slideshow.prototype = {
		init: function(musics) {
			this.wrapper = this.el.querySelector( ".slider-wrapper" );
			this.slides = this.el.querySelectorAll( ".slide" );
			this.previous = this.el.querySelector( ".slider-previous" );
			this.next = this.el.querySelector( ".slider-next" );
			this.index = 0;
			this.total = this.slides.length;
			this.timer = null;
			this.musics = musics;
			//this.action();
			//this.stopStart();	
		},
		_slideTo: function( slide ) {
            var currentSlide = this.slides[slide];
			currentSlide.style.opacity = 1;
			
			for( var i = 0; i < this.slides.length; i++ ) {
				var slide = this.slides[i];
				if( slide !== currentSlide ) {
					slide.style.opacity = 0;
				}
			}
		},
		action: function() {
			var self = this;
			self.timer = setInterval(function() {
				self.index++;
				if( self.index == self.slides.length ) {
					self.index = 0;
				}
				MIDIjs.play(self.musics[self.index]);
				self._slideTo( self.index );
				
			}, interval);
		},
		stopStart: function() {
			var self = this;
			MIDIjs.play(self.musics[0]);
			self._slideTo(0);
			self.action();
			/*self.el.addEventListener( "mouseover", function() {
				clearInterval( self.timer );
				self.timer = null;
				
			}, false);
			self.el.addEventListener( "mouseout", function() {
				self.action();
				
			}, false);*/
		},
		stop: function() {
			var self = this;
			self._slideTo(0);
			clearInterval( self.timer );
		}
		
		
	};

	var isPlaying = false;
	
	document.addEventListener( "DOMContentLoaded", function() {
		var musics = [];
        for (var i = 1; i <=5; i++)
        {
            e = document.getElementById('music'+String(i));
            musics.push(e.value);
        }

		var slider = new Slideshow( "#main-slider", musics );
		
        document.getElementById('playbt').onclick = function () {
			if (isPlaying) {
				slider.stop();
				MIDIjs.stop();
				document.getElementById('playbt').style.backgroundImage = 'url("../static/play.svg")';
				document.getElementById('playbt').style.opacity = 0.5;
				// change to Play, if neccessary
			} else {
				slider.stopStart();
				document.getElementById('playbt').style.backgroundImage = 'url("../static/pause.svg")';
				document.getElementById('playbt').style.opacity = 0;
				isPlaying = true;
			}
		} 
	});
	
	
})();
