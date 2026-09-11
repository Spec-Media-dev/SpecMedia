/**
 * Spec Media — Inverted Fluid Glass Orb Cursor Engine
 */
(function() {
  function initSpecOrbCursor() {
    if (window.__specOrbEngineActive) return;
    if (window.matchMedia && window.matchMedia('(hover: none) or (pointer: coarse)').matches) return;
    window.__specOrbEngineActive = true;

    var cursorDot = document.getElementById('spec-cursor-dot');
    var cursorRing = document.getElementById('spec-cursor-ring');

    if (!cursorDot) {
      cursorDot = document.createElement('div');
      cursorDot.id = 'spec-cursor-dot';
      cursorDot.className = 'spec-cursor-dot';
      document.body.appendChild(cursorDot);
    }

    if (!cursorRing) {
      cursorRing = document.createElement('div');
      cursorRing.id = 'spec-cursor-ring';
      cursorRing.className = 'spec-cursor-ring';
      document.body.appendChild(cursorRing);
    }

    // Badge markup inside the orb
    cursorRing.innerHTML = 
      '<div class="spec-cursor-badge">' +
        '<span>VIEW</span>' +
        '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">' +
          '<line x1="7" y1="17" x2="17" y2="7"></line>' +
          '<polyline points="7 7 17 7 17 17"></polyline>' +
        '</svg>' +
      '</div>';

    // Dynamic spotlight injector on cards
    function injectSpotlights() {
      var cards = document.querySelectorAll('[data-card], .work-card');
      cards.forEach(function(card) {
        var mediaBox = card.querySelector('div:first-child') || card.querySelector('a > div:first-child');
        if (mediaBox && !mediaBox.querySelector('.spec-card-spotlight')) {
          var spot = document.createElement('div');
          spot.className = 'spec-card-spotlight';
          mediaBox.style.position = 'relative';
          mediaBox.appendChild(spot);
        }
      });
    }
    injectSpotlights();

    var mouseX = window.innerWidth / 2;
    var mouseY = window.innerHeight / 2;
    var ringX = mouseX;
    var ringY = mouseY;
    var isVisible = false;
    var activeCard = null;

    window.addEventListener('mousemove', function(e) {
      mouseX = e.clientX;
      mouseY = e.clientY;

      if (!isVisible) {
        isVisible = true;
        cursorDot.style.opacity = '1';
        cursorRing.style.opacity = '1';
      }

      // Fast-track core pin (zero latency)
      cursorDot.style.transform = 'translate(' + mouseX + 'px, ' + mouseY + 'px) translate(-50%, -50%)';

      var target = e.target;
      var card = target ? target.closest('[data-card], .work-card') : null;
      var interactive = target ? target.closest('a, button, [role="button"], input, select, textarea, .spec-orbit-logo-item, .tag, .tab-btn') : null;

      if (card) {
        if (activeCard !== card) {
          activeCard = card;
          cursorRing.classList.add('is-card-hover');
          cursorDot.classList.add('is-card-hover');
          cursorRing.classList.remove('is-hovering');
          cursorDot.classList.remove('is-hovering');
        }

        // 3D Magnetic tilt & spotlight coords
        var rect = card.getBoundingClientRect();
        var relX = mouseX - rect.left;
        var relY = mouseY - rect.top;
        card.style.setProperty('--spot-x', relX + 'px');
        card.style.setProperty('--spot-y', relY + 'px');

        var normX = (relX / rect.width) - 0.5;
        var normY = (relY / rect.height) - 0.5;
        var tiltX = (-normY * 12).toFixed(2);
        var tiltY = (normX * 12).toFixed(2);

        card.style.transform = 'perspective(1000px) rotateX(' + tiltX + 'deg) rotateY(' + tiltY + 'deg) translateY(-8px) scale3d(1.025, 1.025, 1.025)';
      } else {
        if (activeCard) {
          activeCard.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale3d(1, 1, 1)';
          activeCard = null;
          cursorRing.classList.remove('is-card-hover');
          cursorDot.classList.remove('is-card-hover');
        }

        if (interactive) {
          cursorRing.classList.add('is-hovering');
          cursorDot.classList.add('is-hovering');
        } else {
          cursorRing.classList.remove('is-hovering');
          cursorDot.classList.remove('is-hovering');
        }
      }
    }, { passive: true });

    document.addEventListener('mouseout', function(e) {
      var card = e.target ? e.target.closest('[data-card], .work-card') : null;
      if (card && (!e.relatedTarget || !card.contains(e.relatedTarget))) {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale3d(1, 1, 1)';
        if (activeCard === card) {
          activeCard = null;
          cursorRing.classList.remove('is-card-hover');
          cursorDot.classList.remove('is-card-hover');
        }
      }
    });

    // Fluid Inertial Follow Loop
    function render() {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      cursorRing.style.transform = 'translate(' + ringX.toFixed(1) + 'px, ' + ringY.toFixed(1) + 'px) translate(-50%, -50%)';
      requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

    window.addEventListener('mousedown', function() {
      cursorRing.classList.add('is-active');
      cursorDot.classList.add('is-active');
    });
    window.addEventListener('mouseup', function() {
      cursorRing.classList.remove('is-active');
      cursorDot.classList.remove('is-active');
    });

    document.addEventListener('mouseleave', function() {
      cursorDot.style.opacity = '0';
      cursorRing.style.opacity = '0';
      isVisible = false;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSpecOrbCursor);
  } else {
    initSpecOrbCursor();
  }
})();
