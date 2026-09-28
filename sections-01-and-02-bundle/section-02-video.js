// ============================================================================
// SECTION 02 CONTROLLER: 24-Square Mosaic Tile Reveal -> Duck Master Hold -> Fast-Seek Scrubbing
// ============================================================================
var sec2Inited = false;

function initSection2Controller() {
  if (sec2Inited) return true;
  var sec = document.getElementById('spec-scene2-section');
  var stage = document.getElementById('spec-scene2-stage');
  var tilesCont = document.getElementById('spec-tiles-container') || document.getElementById('spec-slices-container');
  var masterImg = document.getElementById('spec-master-image');
  var masterImgEl = document.getElementById('spec-master-img-el');
  var video = document.getElementById('spec-scene2-video');
  if (!sec || !stage || !tilesCont || !masterImg || !video) return false;
  sec2Inited = true;

  // Never trap scroll
  stage.style.pointerEvents = 'none';
  tilesCont.style.pointerEvents = 'none';
  masterImg.style.pointerEvents = 'none';
  video.style.pointerEvents = 'none';

  // High performance video seek management
  var pendingSeekTime = null;
  var seekWatchdog = null;

  function onVideoSeeked() {
    if (seekWatchdog) { clearTimeout(seekWatchdog); seekWatchdog = null; }
    if (pendingSeekTime !== null) {
      var t = pendingSeekTime;
      pendingSeekTime = null;
      if (Math.abs((video.currentTime || 0) - t) > 0.02) {
        seekVideo(t);
      }
    }
  }

  video.addEventListener('seeked', onVideoSeeked);

  function seekVideo(time) {
    var v = document.getElementById('spec-scene2-video') || video;
    if (!v) return;
    if (v.seeking) {
      pendingSeekTime = time;
      if (!seekWatchdog) {
        seekWatchdog = setTimeout(function() {
          seekWatchdog = null;
          if (pendingSeekTime !== null) {
            var pt = pendingSeekTime;
            pendingSeekTime = null;
            try { v.currentTime = pt; } catch(_) {}
          }
        }, 80);
      }
      return;
    }
    try {
      v.currentTime = time;
      if (!seekWatchdog) {
        seekWatchdog = setTimeout(function() {
          seekWatchdog = null;
          if (pendingSeekTime !== null && !v.seeking) {
            var pt = pendingSeekTime;
            pendingSeekTime = null;
            try { v.currentTime = pt; } catch(_) {}
          }
        }, 80);
      }
    } catch (_) {}
  }

  // Set mobile vs desktop fastseek video source
  function updateVideoSource() {
    var isMobile = window.innerWidth <= 768;
    var targetSrc = isMobile ? '/static/Main_vir_fastseek.mp4' : '/static/Main_hir_fastseek.mp4';
    var srcEl = document.getElementById('spec-scene2-video-src');
    var curSrc = video.currentSrc || video.src || '';
    if (!curSrc.includes(targetSrc)) {
      if (srcEl) srcEl.src = targetSrc;
      video.src = targetSrc;
      try { video.load(); } catch(_) {}
    }
  }
  updateVideoSource();
  window.addEventListener('resize', updateVideoSource, { passive: true });

  // Preload starting frame (t = 2.0s: matching duck master image)
  try {
    if (video.readyState >= 1) {
      video.currentTime = 2.0;
    } else {
      video.addEventListener('loadedmetadata', function() {
        try { video.currentTime = 2.0; } catch(_) {}
      }, { once: true });
    }
  } catch (_) {}

  function onSec2Scroll() {
    var liveSec = document.getElementById('spec-scene2-section') || sec;
    var liveStage = document.getElementById('spec-scene2-stage') || stage;
    var liveTilesCont = document.getElementById('spec-tiles-container') || tilesCont;
    var liveMasterImg = document.getElementById('spec-master-image') || masterImg;
    var liveVideo = document.getElementById('spec-scene2-video') || video;
    if (!liveSec || !liveStage || !liveTilesCont || !liveMasterImg || !liveVideo) return;

    var vh = window.innerHeight;
    var maxScroll = Math.max(1, liveSec.offsetHeight - vh);
    var rect = liveSec.getBoundingClientRect();
    var currentScroll = -rect.top;
    var p = Math.max(0, Math.min(1, currentScroll / maxScroll));

    var isMobile = window.innerWidth <= 768;
    var liveTiles = liveTilesCont.querySelectorAll('.spec-tile');

    // --- PHASE 1 (0.00 <= p < 0.38): 24 Square Tiles Staggered Blur Reveal & Assembly ---
    var a = Math.max(0, Math.min(1, p / 0.38));

    liveTiles.forEach(function(tile) {
      var s = parseFloat(tile.getAttribute('data-stagger') || 0);
      var start = s * 0.42;
      var progress = Math.max(0, Math.min(1, (a - start) / 0.58));
      var ease = 1 - Math.pow(1 - progress, 3); // Cubic ease out

      var c = parseInt(tile.getAttribute('data-col'), 10) || 0;
      var r = parseInt(tile.getAttribute('data-row'), 10) || 0;
      
      var driftX = (c - 2.5) * 36 * (1 - ease);
      var driftY = (r - 1.5) * 28 * (1 - ease);
      var scale = 0.76 + 0.24 * ease;
      var blurPx = (28 * (1 - ease)).toFixed(1);

      tile.style.opacity = (0.35 + 0.65 * ease).toFixed(3);
      tile.style.transform = 'translate3d(' + driftX.toFixed(1) + 'px, ' + driftY.toFixed(1) + 'px, 0) scale(' + scale.toFixed(3) + ')';
      tile.style.filter = blurPx > 0.2 ? 'blur(' + blurPx + 'px)' : 'none';
    });

    // --- PHASE 2 (0.36 <= p < 0.48): Pristine Master Reference Image Hold ---
    if (p >= 0.36 && p < 0.48) {
      liveMasterImg.style.opacity = '1';
      liveTilesCont.style.opacity = p < 0.42 ? '1' : String(Math.max(0, 1 - (p - 0.42) / 0.06));
    } else if (p < 0.36) {
      liveMasterImg.style.opacity = '0';
      liveTilesCont.style.opacity = '1';
    }

    // --- PHASE 3: STAGE EXPANSION & SCROLL-SCRUBBED VIDEO (0.48 <= p < 0.95) ---
    if (p >= 0.48) {
      liveTilesCont.style.opacity = '0';
      liveVideo.style.opacity = '1';

      // Stage expansion to 100vw x 100vh
      var expP = Math.max(0, Math.min(1, (p - 0.48) / 0.16));
      var expEase = 1 - Math.pow(1 - expP, 3);

      if (expP <= 0.001) {
        liveStage.style.width = isMobile ? 'min(88vw, 420px)' : 'min(90vw, 1120px)';
        liveStage.style.aspectRatio = isMobile ? '9 / 16' : '16 / 9';
        liveStage.style.maxHeight = isMobile ? '75vh' : '80vh';
        liveStage.style.height = 'auto';
        liveStage.style.borderRadius = isMobile ? '14px' : '18px';
        liveStage.style.boxShadow = '0 24px 60px rgba(0,0,0,0.8)';
        liveMasterImg.style.opacity = '1';
      } else if (expP >= 0.999) {
        liveStage.style.width = '100vw';
        liveStage.style.aspectRatio = 'unset';
        liveStage.style.maxHeight = '100vh';
        liveStage.style.height = '100vh';
        liveStage.style.borderRadius = '0px';
        liveStage.style.boxShadow = 'none';
        liveMasterImg.style.opacity = '0';
      } else {
        var curWidth = 90 + 10 * expEase;
        var curHeight = 80 + 20 * expEase;
        liveStage.style.width = curWidth.toFixed(1) + 'vw';
        liveStage.style.aspectRatio = 'unset';
        liveStage.style.maxHeight = curHeight.toFixed(1) + 'vh';
        liveStage.style.height = curHeight.toFixed(1) + 'vh';
        var rad = (isMobile ? 14 : 18) * (1 - expEase);
        liveStage.style.borderRadius = rad.toFixed(1) + 'px';
        liveStage.style.boxShadow = '0 ' + (24 * (1 - expEase)).toFixed(1) + 'px ' + (60 * (1 - expEase)).toFixed(1) + 'px rgba(0,0,0,' + (0.8 * (1 - expEase)).toFixed(2) + ')';
        liveMasterImg.style.opacity = (1 - expEase).toFixed(2);
      }

      // Video scrub mapping: t = 2.0s to 13.0s
      var vidP = Math.max(0, Math.min(1, (p - 0.48) / 0.47));
      var targetTime = 2.0 + vidP * 11.0;
      if (Math.abs((liveVideo.currentTime || 0) - targetTime) > 0.03) {
        seekVideo(targetTime);
      }
    } else {
      liveVideo.style.opacity = '0';
      liveStage.style.width = isMobile ? 'min(88vw, 420px)' : 'min(90vw, 1120px)';
      liveStage.style.aspectRatio = isMobile ? '9 / 16' : '16 / 9';
      liveStage.style.maxHeight = isMobile ? '75vh' : '80vh';
      liveStage.style.height = 'auto';
      liveStage.style.borderRadius = isMobile ? '14px' : '18px';
      liveStage.style.boxShadow = '0 24px 60px rgba(0,0,0,0.8)';
      if (liveVideo.currentTime > 2.05 || liveVideo.currentTime < 1.95) {
        try { liveVideo.currentTime = 2.0; } catch(_) {}
      }
    }
  }

  window.__specUpdateSection2 = onSec2Scroll;

  var s2Ticking = false;
  function queueSec2Update() {
    if (!s2Ticking) {
      s2Ticking = true;
      requestAnimationFrame(function() {
        s2Ticking = false;
        onSec2Scroll();
      });
    }
  }

  window.addEventListener('scroll', queueSec2Update, { passive: true });
  window.addEventListener('resize', queueSec2Update, { passive: true });

  if (window.lenis && typeof window.lenis.on === 'function') {
    window.lenis.on('scroll', queueSec2Update);
  } else {
    var s2Timer = setInterval(function() {
      if (window.lenis && typeof window.lenis.on === 'function') {
        window.lenis.on('scroll', queueSec2Update);
        clearInterval(s2Timer);
      }
    }, 100);
    setTimeout(function() { clearInterval(s2Timer); }, 5000);
  }

  onSec2Scroll();
  return true;
}
