// ============================================================================
// SECTION 01 CONTROLLER: Hero Logo Flight & Dynamic Ambient Spotlight
// ============================================================================
function initHeroLogoFlight() {
  try {
    document.querySelectorAll('.spec-logo-char-img img').forEach(function(img) {
      if (!img.crossOrigin) {
        img.crossOrigin = 'anonymous';
      }
    });
  } catch(_) {}

  function getLiveNavLogo() {
    return document.querySelector('.spec-chrome-nav-logo');
  }

  var cachedNatW = 167.5;
  var cachedNatH = 20;
  var cachedNatX = 80;
  var cachedNatY = 38;
  var metricsCached = false;

  function cacheNaturalMetrics() {
    var navLogo = getLiveNavLogo();
    if (!navLogo) return;
    var prevT = navLogo.style.transform;
    var prevO = navLogo.style.transformOrigin;
    navLogo.style.transform = 'none';
    var rect = navLogo.getBoundingClientRect();
    navLogo.style.transform = prevT;
    navLogo.style.transformOrigin = prevO;
    if (rect && rect.width > 30) {
      cachedNatW = rect.width;
      cachedNatH = rect.height;
      cachedNatX = rect.left;
      cachedNatY = rect.top;
      metricsCached = true;
    }
  }

  var cachedHeroLeft = 48;
  var cachedTargetHeroW = 512.7;
  var heroMetricsCached = false;

  function cacheHeroMetrics() {
    var vw = window.innerWidth;
    var title = document.querySelector('.spec-hero-title');
    var desc = document.querySelector('.spec-hero-desc');
    var startLeft = 48;
    var identitiesRight = 1381.1;

    if (title) {
      var titleRect = title.getBoundingClientRect();
      if (titleRect.left > 0) startLeft = titleRect.left;
    }
    if (desc) {
      for (var nodeIdx = 0; nodeIdx < desc.childNodes.length; nodeIdx++) {
        var node = desc.childNodes[nodeIdx];
        if (node.nodeType === Node.TEXT_NODE && node.textContent.indexOf('identities') !== -1) {
          try {
            var range = document.createRange();
            var idx = node.textContent.indexOf('identities');
            range.setStart(node, idx);
            range.setEnd(node, idx + 'identities'.length);
            var r = range.getBoundingClientRect();
            if (r && r.right > startLeft + 100) {
              identitiesRight = r.right;
            }
          } catch(e) {}
          break;
        }
      }
    }
    var targetHeroW = identitiesRight - startLeft;
    if (vw <= 640) {
      targetHeroW = Math.max(targetHeroW, vw - startLeft * 2);
    }
    cachedHeroLeft = startLeft;
    cachedTargetHeroW = targetHeroW;
    heroMetricsCached = true;
  }

  function updateFlight() {
    var navLogo = getLiveNavLogo();
    if (!navLogo) return;
    var chromeNav = document.querySelector('.spec-landing-chrome');
    var actions = chromeNav ? chromeNav.querySelector('.spec-chrome-actions') : null;

    var scrollY = (window.lenis && typeof window.lenis.scroll === 'number')
      ? window.lenis.scroll
      : (window.pageYOffset || document.documentElement.scrollTop || window.scrollY || 0);

    var vh = window.innerHeight;
    var vw = window.innerWidth;

    var flightDist = Math.max(220, Math.min(450, vh * 0.48));
    var p = Math.max(0, Math.min(1, scrollY / flightDist));
    var ease = p < 0.5 ? 2 * p * p : -1 + (4 - 2 * p) * p;

    if (!metricsCached) cacheNaturalMetrics();
    if (!heroMetricsCached) cacheHeroMetrics();

    var natW = cachedNatW;
    var natH = cachedNatH;
    var natX = cachedNatX;
    var natY = cachedNatY;

    var startLeft = cachedHeroLeft;
    var targetHeroW = cachedTargetHeroW;

    var scaleHero = targetHeroW / natW;
    var startX = startLeft - natX;
    var topMargin = Math.max(16, Math.min(24, vh * 0.024));
    var startY = topMargin - natY;

    var curX = startX * (1 - ease);
    var curY = startY * (1 - ease);
    var curScale = 1.0 + (scaleHero - 1.0) * (1 - ease);
    window.__specLogoCurrentScale = curScale;

    navLogo.style.transformOrigin = '0 0';
    if (p >= 0.999) {
      navLogo.style.transform = 'none';
      navLogo.classList.add('spec-docked-nav');
      document.documentElement.classList.add('spec-scrolled');
    } else {
      navLogo.style.transform = 'translate3d(' + curX.toFixed(2) + 'px, ' + curY.toFixed(2) + 'px, 0) scale(' + curScale.toFixed(4) + ')';
      navLogo.classList.remove('spec-docked-nav');
      if (scrollY < 80) {
        document.documentElement.classList.remove('spec-scrolled');
      }
    }

    if (!navLogo._clickScrollBound) {
      navLogo._clickScrollBound = true;
      navLogo.addEventListener('click', function(e) {
        e.preventDefault();
        if (window.lenis && typeof window.lenis.scrollTo === 'function') {
          window.lenis.scrollTo(0, { duration: 1.2 });
        } else {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    }
    navLogo.style.opacity = '1';
    navLogo.style.visibility = 'visible';

    // Synchronize Navbar Actions
    if (actions) {
      if (p <= 0.08) {
        actions.style.opacity = '0';
        actions.style.pointerEvents = 'none';
        actions.style.transform = 'translateY(-8px)';
      } else {
        var aAlpha = Math.max(0, Math.min(1, (p - 0.08) / 0.82));
        actions.style.opacity = aAlpha.toFixed(3);
        actions.style.pointerEvents = p > 0.5 ? 'auto' : 'none';
        actions.style.transform = 'translateY(' + ((1 - aAlpha) * -8).toFixed(1) + 'px)';
      }
    }

    if (chromeNav) {
      chromeNav.style.opacity = '1';
      chromeNav.style.pointerEvents = 'auto';
    }

    // Zero-overhead dynamic contrast: detects intersection with light sections
    var isLight = false;
    if (document.documentElement.classList.contains('spec-light-mode')) {
      isLight = true;
    } else {
      var checkY = 48;
      var lightEls = document.querySelectorAll('[data-screen-label="03 Work grid"], [data-screen-label="03b Statement"]');
      for (var li = 0; li < lightEls.length; li++) {
        var lr = lightEls[li].getBoundingClientRect();
        if (lr.top <= checkY && lr.bottom >= checkY) {
          isLight = true;
          break;
        }
      }
    }
    var targetColor = isLight ? '#000000' : '#FFFFFF';
    document.documentElement.style.setProperty('--spec-nav-logo-color', targetColor);
    navLogo.style.setProperty('--spec-nav-logo-color', targetColor);
    navLogo.style.color = targetColor;

    return { scrollY: scrollY, p: p, ease: ease, curX: curX, curY: curY, curScale: curScale };
  }

  window.__specUpdateFlight = updateFlight;

  function onFlightResize() {
    metricsCached = false;
    heroMetricsCached = false;
    updateFlight();
  }
  window.addEventListener('resize', onFlightResize, { passive: true });

  var flightTicking = false;
  function queueFlightUpdate() {
    if (!flightTicking) {
      flightTicking = true;
      requestAnimationFrame(function() {
        flightTicking = false;
        updateFlight();
      });
    }
  }

  window.addEventListener('scroll', queueFlightUpdate, { passive: true });

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function() {
      onFlightResize();
    });
  }

  window.addEventListener('load', function() {
    onFlightResize();
    setTimeout(onFlightResize, 200);
    setTimeout(onFlightResize, 800);
  });

  if (window.lenis && typeof window.lenis.on === 'function') {
    window.lenis.on('scroll', queueFlightUpdate);
  } else {
    var fTimer = setInterval(function() {
      if (window.lenis && typeof window.lenis.on === 'function') {
        window.lenis.on('scroll', queueFlightUpdate);
        clearInterval(fTimer);
      }
    }, 100);
    setTimeout(function() { clearInterval(fTimer); }, 5000);
  }

  updateFlight();
  return true;
}
