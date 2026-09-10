document.addEventListener('DOMContentLoaded', async function() {
  const loading = document.getElementById('__bundler_loading');
  function setStatus(msg) { if (loading) loading.textContent = msg; }

  const FONT_MIME = /^(font[/]|application[/](x-)?font-|application[/]vnd\.ms-fontobject)/i;
  const MIME_TOKEN = /^[\w.+-]+[/][\w.+-]+$/;
  function toBase64(bytes) {
    let bin = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    }
    return btoa(bin);
  }

  // Error sink persists across replaceWith since it's on window, not the DOM.
  window.addEventListener('error', function(e) {
    // Failed resource loads (CSP-blocked links, scripts, images) fire plain
    // events at the element — warn only; real JS errors carry message/error.
    if (!e.message && !e.error && e.target && e.target !== window) {
      console.warn('[bundle] resource failed to load:',
        e.target.tagName, String(e.target.src || e.target.href || ''));
      return;
    }
    var p = document.body || document.documentElement;
    var d = document.getElementById('__bundler_err') || p.appendChild(document.createElement('div'));
    d.id = '__bundler_err';
    d.style.cssText = 'position:fixed;bottom:12px;left:12px;right:12px;font:12px/1.4 ui-monospace,monospace;background:#2a1215;color:#ff8a80;padding:10px 14px;border-radius:8px;border:1px solid #5c2b2e;z-index:99999;white-space:pre-wrap;max-height:40vh;overflow:auto';
    d.textContent = (d.textContent ? d.textContent + String.fromCharCode(10) : '') +
      '[bundle] ' + (e.message || e.type) +
      (e.filename ? ' (' + e.filename.slice(0, 60) + ':' + e.lineno + ')' : '');
  }, true);

  try {
    const manifestEl = document.querySelector('script[type="__bundler/manifest"]');
    const templateEl = document.querySelector('script[type="__bundler/template"]');
    if (!manifestEl || !templateEl) {
      setStatus('Error: missing bundle data');
      console.error('[bundler] Missing script tags — manifestEl:', !!manifestEl, 'templateEl:', !!templateEl);
      return;
    }

    const manifest = JSON.parse(manifestEl.textContent);
    let template = JSON.parse(templateEl.textContent);

    // Nested page bundles (iframe targets). Each ships ONCE, in the ROOT
    // document's manifest; frame srcs carry an about:blank#<uuid> marker
    // instead of a substitutable uuid. Every document mints the blobs for
    // its OWN frames — from local text at the root, or text obtained from
    // its DIRECT parent over the relay protocol below — so each frame
    // navigation stays same-origin with its initiator and a deduped page
    // loads at any depth on any host, including a file:// download's
    // opaque origins (where a blob minted by one document cannot be
    // navigated to by another).
    const pageOrderEl = document.querySelector('script[type="__bundler/page_order"]');
    const pageOrder = pageOrderEl ? JSON.parse(pageOrderEl.textContent) : [];
    const pageSet = new Set(pageOrder);
    const pageTexts = {};

    // ── Nested-page text protocol (parent-chain relay) ──
    // Page bundles ship once, in the ROOT document's manifest. Every
    // document mints the blobs for its OWN frames, obtaining page text
    // through a strict parent-chain relay: a document only ever SENDS to
    // its direct parent (which, for every document the publisher's own
    // runtime minted, is another publisher document) and only ACCEPTS
    // text from that direct parent; requests from below are honored only
    // for the document's own child frames, and the ROOT never sends
    // upward at all. That last rule is load-bearing: the artifact host's
    // frame-ancestors allows claude.ai (and friends) to frame an
    // artifact, so window.top can be a FOREIGN document — a top-addressed
    // protocol would hand page uuids to that ancestor and accept forged
    // "page text" from it, minting attacker HTML as an artifact-origin
    // blob document. The chain never touches the ancestor: requests stop
    // at the root, replies are origin-addressed per hop (never '*' when
    // an origin exists), and both directions are origin-gated (on https
    // a foreign sender's origin can never equal this document's; in
    // opaque contexts — file:// — everything serializes as 'null', where
    // an embedded EXTERNAL frame still fails the gate by carrying its
    // own real origin, and a sandboxed child of such a frame is excluded
    // by the own-child-frames check plus uuid unguessability). Shape is
    // deny-by-default: one request form, one reply form, no error
    // replies.
    // window.origin is the SERIALIZED SECURITY origin ('null' in opaque
    // contexts such as a sandboxed preview iframe) — location.origin is
    // computed from the URL and stays 'https://…' even when the document
    // is sandboxed, which would misgate every opaque chain.
    const OWN_TARGET = /^https?:[/][/]/.test(window.origin || '')
      ? window.origin
      : '*';
    function trustedOrigin(e) {
      if (e.origin === window.origin) return true; // https chains; opaque==opaque
      // file:// trees: Chrome serializes the file document's origin as
      // 'file://' while the blob: documents it mints serialize as 'null',
      // so the two legitimate shapes can never string-match — accept the
      // pair in both directions. https origins never serialize as either,
      // and sender identity (own child frame / direct parent) is checked
      // separately.
      return (
        (e.origin === 'null' &&
          (window.origin === 'file://' ||
            window.location.protocol === 'file:')) ||
        (/^file:/.test(e.origin) && window.origin === 'null')
      );
    }
    // Non-empty only in the root document (nested bundles ship an empty
    // island), so it doubles as the root marker: the root answers from
    // local text and treats a miss as authoritative — never relaying to
    // its (possibly foreign) parent.
    const isPageRoot = pageOrder.length > 0;
    const blobUrls = {};
    const resourceBlobs = {};
    const UUID_SHAPE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    const pendingFrames = {}; // uuid -> [{el, frag}] awaiting text for own frames
    const pendingRelays = {}; // uuid -> [childWindow] awaiting text to pass down
    function mountPage(el, frag, text) {
      const pageBlob = new Blob([text], { type: 'text/html' });
      const u = URL.createObjectURL(pageBlob);
      resourceBlobs[u] = pageBlob;
      el.src = u + frag;
    }
    function deliverPage(uuid, text) {
      const frames = pendingFrames[uuid];
      delete pendingFrames[uuid];
      if (frames) for (const f of frames) mountPage(f.el, f.frag, text);
      const relays = pendingRelays[uuid];
      delete pendingRelays[uuid];
      if (relays) {
        for (const cw of relays) {
          try { cw.postMessage({ __bundler_page: uuid, __bundler_text: text }, OWN_TARGET); } catch (err) { /* gone */ }
        }
      }
    }
    function ownFrameWindows() {
      const out = [];
      for (const f of Array.from(document.querySelectorAll('iframe'))) {
        try { if (f.contentWindow) out.push(f.contentWindow); } catch (err) { /* detached */ }
      }
      return out;
    }
    window.addEventListener('message', function (e) {
      const d = e.data;
      if (!d || typeof d !== 'object' || !e.source) return;
      // Origin gate first; the structural checks below (own-child-frames
      // for requests, direct-parent + solicited-uuid for replies, the
      // root's never-relay rule) are what hold in fully opaque chains
      // where origin strings can't discriminate — a sandboxed root's
      // FOREIGN wrapper still fails all three even though both serialize
      // as real-vs-'null' rather than matching.
      if (!trustedOrigin(e)) return;
      if (typeof d.__bundler_need === 'string' && UUID_SHAPE.test(d.__bundler_need)) {
        // Requests are honored only for this document's own child frames.
        if (ownFrameWindows().indexOf(e.source) < 0) return;
        const uuid = d.__bundler_need;
        const text = pageTexts[uuid];
        if (typeof text === 'string') {
          try { e.source.postMessage({ __bundler_page: uuid, __bundler_text: text }, OWN_TARGET); } catch (err) { /* gone */ }
          return;
        }
        if (isPageRoot || window.parent === window) return; // authoritative miss
        const waiting = pendingRelays[uuid];
        if (waiting) {
          if (waiting.indexOf(e.source) < 0) waiting.push(e.source);
          return;
        }
        // Never-answered uuids would otherwise accumulate forever under a
        // request spray; past the cap (far above any real page count) new
        // relays are dropped rather than remembered.
        if (Object.keys(pendingRelays).length >= 128) return;
        pendingRelays[uuid] = [e.source];
        window.parent.postMessage({ __bundler_need: uuid }, OWN_TARGET);
      } else if (
        typeof d.__bundler_page === 'string' &&
        UUID_SHAPE.test(d.__bundler_page) &&
        typeof d.__bundler_text === 'string'
      ) {
        // The shape test is load-bearing beyond tidiness: the solicited
        // check below uses the in operator, which matches prototype keys
        // ('__proto__', 'constructor') — an unshaped key would reach
        // deliverPage and throw, painting the error banner.
        // Text is accepted only from the direct parent — the document
        // that minted this one.
        if (e.source !== window.parent || window.parent === window) return;
        if (!(d.__bundler_page in pendingFrames) && !(d.__bundler_page in pendingRelays)) return;
        deliverPage(d.__bundler_page, d.__bundler_text);
      }
    });

    const uuids = Object.keys(manifest);
    setStatus('Unpacking ' + uuids.length + ' assets...');

    await Promise.all(uuids.map(async (uuid) => {
      const entry = manifest[uuid];
      try {
        const binaryStr = atob(entry.data);
        const bytes = new Uint8Array(binaryStr.length);
        for (let i = 0; i < binaryStr.length; i++) bytes[i] = binaryStr.charCodeAt(i);

        let finalBytes = bytes;
        if (entry.compressed) {
          if (typeof DecompressionStream !== 'undefined') {
            const ds = new DecompressionStream('gzip');
            const writer = ds.writable.getWriter();
            const reader = ds.readable.getReader();
            writer.write(bytes);
            writer.close();
            const chunks = [];
            let totalLen = 0;
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              chunks.push(value);
              totalLen += value.length;
            }
            finalBytes = new Uint8Array(totalLen);
            let offset = 0;
            for (const chunk of chunks) { finalBytes.set(chunk, offset); offset += chunk.length; }
          } else {
            console.warn('DecompressionStream not available, asset ' + uuid + ' may not render');
          }
        }

        if (pageSet.has(uuid)) {
          pageTexts[uuid] = new TextDecoder().decode(finalBytes);
          return;
        }
        if (FONT_MIME.test(entry.mime) && MIME_TOKEN.test(entry.mime)) {
          // Strict artifact hosts allow font-src data: but not blob:.
          blobUrls[uuid] = 'data:' + entry.mime + ';base64,' +
            (entry.compressed ? toBase64(finalBytes) : entry.data);
        } else {
          const blob = new Blob([finalBytes], { type: entry.mime });
          blobUrls[uuid] = URL.createObjectURL(blob);
          resourceBlobs[blobUrls[uuid]] = blob;
        }
      } catch (err) {
        console.error('Failed to decode asset ' + uuid + ':', err);
        const blob = new Blob([], { type: entry.mime });
        blobUrls[uuid] = URL.createObjectURL(blob);
        resourceBlobs[blobUrls[uuid]] = blob;
      }
    }));

    const extResEl = document.querySelector('script[type="__bundler/ext_resources"]');
    const extResources = extResEl ? JSON.parse(extResEl.textContent) : [];
    const resourceMap = {};
    for (const entry of extResources) {
      if (blobUrls[entry.uuid]) resourceMap[entry.id] = blobUrls[entry.uuid];
    }

    // Artifact-host CSP (connect-src 'self') refuses fetch() of blob: URLs —
    // consumers read these Blobs directly. Survives the swap like the error sink.
    window.__resourceBlobs = resourceBlobs;

    setStatus('Rendering...');
    // Page uuids have no blob here — they ride inside about:blank#<uuid>
    // frame markers the pass below resolves after the swap.
    for (const uuid of uuids) {
      if (pageSet.has(uuid)) continue;
      template = template.split(uuid).join(blobUrls[uuid]);
    }

    // Strip integrity + crossorigin — blob URLs from a file:// document inherit
    // a null origin, so crossorigin forces a CORS fetch that SRI then rejects.
    // The manifest bytes are ours; SRI protects against CDN compromise, not this.
    template = template.replace(/\s+integrity="[^"]*"/gi, '').replace(/\s+crossorigin="[^"]*"/gi, '');

    const resourceScript = '<script>window.__resources = ' +
      JSON.stringify(resourceMap).replace(/<\//g, '<\\/') +
      ';</' + 'script>';
    // Inject after <head> so the DOCTYPE stays first; prepending the script
    // would push the parser into quirks mode. DOMParser always emits a <head>
    // (synthesizing one if the source HTML omitted it) but may carry
    // attributes through, so match the full opening tag. slice() rather than
    // replace() keeps us clear of $-pattern substitution in resourceScript.
    const headOpen = template.match(/<head[^>]*>/i);
    if (headOpen) {
      const i = headOpen.index + headOpen[0].length;
      template = template.slice(0, i) + resourceScript + template.slice(i);
    }

    // Parse the template and swap the root element. Scripts inserted via
    // DOMParser/replaceWith are inert per spec — re-create each with
    // createElement so they execute, awaiting onload for src scripts to
    // preserve ordering (React before ReactDOM before Babel before text/babel).
    const doc = new DOMParser().parseFromString(template, 'text/html');
    document.documentElement.replaceWith(doc.documentElement);

    // Resolve page-frame markers: mint this document's own blob for each
    // framed page — from local text when this is the root, otherwise by
    // asking the direct parent over the relay protocol above. An
    // unanswered request leaves the frame on about:blank, the same
    // degraded state as a refused embed.
    {
      const MARKER = /^about:blank#([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(#.*)?$/;
      const needed = [];
      for (const el of Array.from(document.querySelectorAll('iframe'))) {
        const m = MARKER.exec(el.getAttribute('src') || '');
        if (!m) continue;
        const text = pageTexts[m[1]];
        if (typeof text === 'string') {
          mountPage(el, m[2] || '', text);
        } else if (window.parent !== window && !isPageRoot) {
          const had = pendingFrames[m[1]];
          (pendingFrames[m[1]] = had || []).push({ el: el, frag: m[2] || '' });
          if (!had) needed.push(m[1]);
        }
      }
      for (const uuid of needed) {
        window.parent.postMessage({ __bundler_need: uuid }, OWN_TARGET);
      }
    }

    const dead = Array.from(document.scripts);
    for (const old of dead) {
      const s = document.createElement('script');
      for (const a of old.attributes) s.setAttribute(a.name, a.value);
      s.textContent = old.textContent;
      // text/babel scripts with a src: read and inline. transformScriptTags
      // does XHR against the src, but blob:null/ from a file:// origin is
      // silently dropped. Inlining makes it a plain inline babel script,
      // which transformScriptTags handles unconditionally.
      if ((s.type === 'text/babel' || s.type === 'text/jsx') && s.src) {
        const pre = resourceBlobs[s.src.split('#')[0]];
        s.textContent = pre ? await pre.text() : await (await fetch(s.src)).text();
        s.removeAttribute('src');
      }
      const p = s.src ? new Promise(function(r) { s.onload = s.onerror = r; }) : null;
      old.replaceWith(s);
      if (p) await p;
    }
    // Babel standalone auto-transforms type=text/babel on DOMContentLoaded,
    // which fired before we swapped the document. Trigger manually if present.
    if (window.Babel && typeof window.Babel.transformScriptTags === 'function') {
      window.Babel.transformScriptTags();
    }

    // --- Spec Media Non-Intrusive Integration Layer ---
    setTimeout(function initSpecIntegration() {
      // 1. Rewire footer links to dedicated pages
      try {
        var links = document.querySelectorAll('footer a, footer span, a');
        links.forEach(function(a) {
          var txt = (a.textContent || '').trim().toLowerCase();
          if (txt === 'work') { a.href = '/work/'; }
          else if (txt === 'studio') { a.href = '/studio/'; }
          else if (txt === 'capabilities') { a.href = '/capabilities/'; }
        });
      } catch(e) { console.warn('Footer rewire error:', e); }

      

      // =========================================================================
      // SPEC MEDIA INTERACTIVE SCROLL TEXT ANIMATION ENGINE
      // Dynamically animates all headings, words, paragraphs, badges & labels on scroll
      // =========================================================================
      try {
        var animStyle = document.createElement('style');
        animStyle.id = 'sm-text-scroll-anim-styles';
        animStyle.textContent = `
          .sm-scroll-word {
            display: inline-block;
            white-space: pre;
            will-change: transform, opacity, filter;
            transform-origin: 50% 100%;
            transition: color 0.25s ease;
          }
          .sm-scroll-p {
            will-change: transform, opacity;
            transform-origin: 0% 50%;
          }
          .sm-scroll-badge {
            display: inline-block;
            will-change: transform, opacity, letter-spacing;
            transition: color 0.2s ease, border-color 0.2s ease;
          }
          .sm-scroll-card-title {
            will-change: transform, opacity;
            transform-origin: 0% 50%;
          }
          .sm-scroll-cap-line {
            will-change: transform, opacity;
          }
          .sm-scroll-footer-item {
            will-change: transform, opacity;
          }
        `;
        document.head.appendChild(animStyle);

        // 1. Prepare & wrap major headings with word spans
        var headings = document.querySelectorAll('h1, h2, h3');
        var headingItems = [];

        headings.forEach(function(h) {
          if (h.closest('#sm-ui-container') || h.querySelector('[data-word]')) return;
          var isMajor = h.tagName === 'H1' || h.tagName === 'H2';
          if (isMajor && !h.dataset.smSplit) {
            h.dataset.smSplit = 'true';
            var text = h.textContent.trim();
            var words = text.split(/\s+/);
            h.innerHTML = '';
            var wordSpans = [];
            words.forEach(function(w, i) {
              var span = document.createElement('span');
              span.className = 'sm-scroll-word';
              span.textContent = w + (i < words.length - 1 ? ' ' : '');
              h.appendChild(span);
              wordSpans.push(span);
            });
            headingItems.push({ el: h, words: wordSpans, isMajor: true });
          } else if (h.tagName === 'H3') {
            h.classList.add('sm-scroll-card-title');
            headingItems.push({ el: h, isH3: true });
          }
        });

        // 2. Prepare paragraphs (<p> tags)
        var paragraphs = [];
        document.querySelectorAll('p').forEach(function(p) {
          if (p.closest('#sm-ui-container')) return;
          p.classList.add('sm-scroll-p');
          paragraphs.push(p);
        });

        // 3. Prepare Badges, Scene Labels & Mono Tags
        var badges = [];
        var badgeCandidates = document.querySelectorAll('section [style*="ui-monospace"], section [style*="letter-spacing"], [data-screen-label]');
        badgeCandidates.forEach(function(el) {
          if (el.closest('#sm-ui-container') || el.tagName === 'CANVAS' || el.tagName === 'ARTICLE') return;
          if (el.children.length === 0 && el.textContent.trim().length > 1) {
            el.classList.add('sm-scroll-badge');
            badges.push(el);
          }
        });

        // 4. Prepare Capabilities items
        var capRows = [];
        var capSec = document.querySelector('[data-screen-label*="Capabilities"]');
        if (capSec) {
          var capLinks = capSec.querySelectorAll('a, [style-hover]');
          capLinks.forEach(function(row, idx) {
            capRows.push({ el: row, idx: idx });
          });
        }

        // 5. Prepare Footer text items
        var footerItems = [];
        var footer = document.querySelector('footer#contact');
        if (footer) {
          var fTexts = footer.querySelectorAll('h1, h2, h3, h4, div > span, div > a, div > div');
          fTexts.forEach(function(ft) {
            if (ft.children.length === 0 && ft.textContent.trim().length > 1) {
              ft.classList.add('sm-scroll-footer-item');
              footerItems.push(ft);
            }
          });
        }

        // 6. 60fps Scroll Interaction Loop
        var lastY = window.scrollY;
        var scrollVelocity = 0;
        var smoothVelocity = 0;

        function runTextScrollLoop() {
          var y = window.scrollY;
          var dy = y - lastY;
          lastY = y;
          scrollVelocity = dy;
          smoothVelocity = smoothVelocity * 0.82 + scrollVelocity * 0.18;
          var vh = window.innerHeight;

          // A. Headings & Words
          headingItems.forEach(function(item) {
            var rect = item.el.getBoundingClientRect();
            if (rect.bottom < -80 || rect.top > vh + 80) return;

            if (item.isMajor && item.words) {
              var progress = Math.max(0, Math.min(1, (vh * 0.92 - rect.top) / (vh * 0.55)));
              var totalWords = item.words.length;

              item.words.forEach(function(word, idx) {
                var wordThreshold = idx / (totalWords + 2);
                var p = Math.max(0, Math.min(1, (progress - wordThreshold * 0.6) / 0.45));
                var ease = 1 - Math.pow(1 - p, 3);
                
                var ty = (1 - ease) * 30;
                var opacity = 0.18 + 0.82 * ease;
                var blur = (1 - ease) * 4;
                var skew = Math.max(-4, Math.min(4, smoothVelocity * 0.04));

                word.style.transform = 'translateY(' + ty.toFixed(2) + 'px) skewY(' + skew.toFixed(2) + 'deg)';
                word.style.opacity = opacity.toFixed(3);
                word.style.filter = ease < 0.98 ? 'blur(' + blur.toFixed(1) + 'px)' : 'none';

                if (ease > 0.85) {
                  word.style.color = 'var(--color-bg)';
                } else {
                  word.style.color = 'inherit';
                }
              });
            } else if (item.isH3) {
              var p3 = Math.max(0, Math.min(1, (vh * 0.88 - rect.top) / (vh * 0.5)));
              var ease3 = 1 - Math.pow(1 - p3, 3);
              var ty3 = (1 - ease3) * 20;
              var op3 = 0.25 + 0.75 * ease3;
              var skew3 = Math.max(-3, Math.min(3, smoothVelocity * 0.03));
              item.el.style.transform = 'translateY(' + ty3.toFixed(2) + 'px) skewY(' + skew3.toFixed(2) + 'deg)';
              item.el.style.opacity = op3.toFixed(3);
            }
          });

          // B. Paragraphs & Body Descriptions
          paragraphs.forEach(function(p) {
            var rect = p.getBoundingClientRect();
            if (rect.bottom < -60 || rect.top > vh + 60) return;

            var progress = Math.max(0, Math.min(1, (vh * 0.9 - rect.top) / (vh * 0.5)));
            var ease = 1 - Math.pow(1 - progress, 3);
            var drift = (rect.top - vh * 0.5) * 0.032;
            var ty = (1 - ease) * 20 + drift;
            var opacity = Math.max(0.2, Math.min(1, 0.25 + 0.75 * ease));

            p.style.transform = 'translateY(' + ty.toFixed(2) + 'px)';
            p.style.opacity = opacity.toFixed(3);
          });

          // C. Badges & Scene Labels
          badges.forEach(function(b) {
            var rect = b.getBoundingClientRect();
            if (rect.bottom < -40 || rect.top > vh + 40) return;

            var progress = Math.max(0, Math.min(1, (vh * 0.95 - rect.top) / (vh * 0.4)));
            var ease = 1 - Math.pow(1 - progress, 2);
            var tx = (1 - ease) * -16;
            var ty = (1 - ease) * 10;
            var op = 0.3 + 0.7 * ease;

            b.style.transform = 'translateX(' + tx.toFixed(2) + 'px) translateY(' + ty.toFixed(2) + 'px)';
            b.style.opacity = op.toFixed(3);
          });

          // D. Capabilities Rows
          capRows.forEach(function(item) {
            var rect = item.el.getBoundingClientRect();
            if (rect.bottom < -50 || rect.top > vh + 50) return;

            var p = Math.max(0, Math.min(1, (vh * 0.9 - rect.top) / (vh * 0.45)));
            var ease = 1 - Math.pow(1 - p, 3);
            var tx = (1 - ease) * (item.idx % 2 === 0 ? -22 : 22);
            var ty = (1 - ease) * 12;
            var op = 0.3 + 0.7 * ease;

            item.el.style.transform = 'translateX(' + tx.toFixed(2) + 'px) translateY(' + ty.toFixed(2) + 'px)';
            item.el.style.opacity = op.toFixed(3);
          });

          // E. Footer Elements
          footerItems.forEach(function(ft, i) {
            var rect = ft.getBoundingClientRect();
            if (rect.bottom < -50 || rect.top > vh + 50) return;

            var p = Math.max(0, Math.min(1, (vh * 0.98 - rect.top) / (vh * 0.4)));
            var ease = 1 - Math.pow(1 - p, 3);
            var ty = (1 - ease) * (18 + (i % 4) * 4);
            var op = 0.25 + 0.75 * ease;

            ft.style.transform = 'translateY(' + ty.toFixed(2) + 'px)';
            ft.style.opacity = op.toFixed(3);
          });

          requestAnimationFrame(runTextScrollLoop);
        }

        requestAnimationFrame(runTextScrollLoop);
      } catch(err) {
        console.warn('Scroll text animation engine error:', err);
      }

// 2. Inject Modal & Menu HTML and Styles into DOM
      if (document.getElementById('sm-ui-container')) return;

      var uiContainer = document.createElement('div');
      uiContainer.id = 'sm-ui-container';
      uiContainer.innerHTML = `
        <style>
          #sm-ui-container {
            position: relative;
            z-index: 99999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          }
          .sm-overlay-backdrop {
            position: fixed;
            inset: 0;
            background: rgba(14, 13, 12, 0.82);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 100000;
          }
          .sm-overlay-backdrop.sm-active {
            opacity: 1;
            pointer-events: auto;
          }
          /* Menu Drawer */
          #sm-menu-drawer {
            position: fixed;
            top: 0;
            right: 0;
            width: min(480px, 92vw);
            height: 100vh;
            background: #1a1817;
            border-left: 1px solid rgba(198, 113, 57, 0.28);
            transform: translateX(100%);
            transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 100001;
            display: flex;
            flex-direction: column;
            padding: 36px 32px;
            box-sizing: border-box;
            box-shadow: -20px 0 60px rgba(0, 0, 0, 0.7);
            color: #f5ead8;
          }
          #sm-menu-drawer.sm-active {
            transform: translateX(0);
          }
          .sm-drawer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 24px;
            border-bottom: 1px solid rgba(245, 234, 216, 0.12);
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 11px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #c67139;
          }
          .sm-close-btn {
            background: none;
            border: 1px solid rgba(245, 234, 216, 0.25);
            color: #f5ead8;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 11px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            padding: 6px 14px;
            border-radius: 999px;
            cursor: pointer;
            transition: all 0.2s ease;
          }
          .sm-close-btn:hover {
            background: #c67139;
            border-color: #c67139;
            color: #1a1817;
          }
          .sm-nav-links {
            display: flex;
            flex-direction: column;
            gap: 18px;
            margin: 40px 0;
            flex: 1;
          }
          .sm-nav-link-item {
            display: flex;
            align-items: baseline;
            gap: 16px;
            text-decoration: none;
            color: #f5ead8;
            transition: all 0.25s ease;
            padding: 10px 0;
            border-bottom: 1px solid rgba(245, 234, 216, 0.06);
          }
          .sm-nav-link-item:hover {
            color: #c67139;
            transform: translateX(8px);
          }
          .sm-nav-idx {
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 12px;
            letter-spacing: 0.14em;
            color: #c67139;
            opacity: 0.8;
          }
          .sm-nav-label {
            font-size: 24px;
            font-weight: 500;
            letter-spacing: -0.02em;
          }
          .sm-drawer-footer {
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 11px;
            color: #8c8376;
            letter-spacing: 0.12em;
            line-height: 1.6;
            border-top: 1px solid rgba(245, 234, 216, 0.1);
            padding-top: 20px;
          }

          /* Contact Modal */
          #sm-contact-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -46%) scale(0.96);
            width: min(580px, 94vw);
            max-height: 90vh;
            overflow-y: auto;
            background: #1b1918;
            border: 1px solid rgba(198, 113, 57, 0.35);
            box-shadow: 0 30px 90px rgba(0, 0, 0, 0.85);
            border-radius: 12px;
            padding: 36px 36px 32px;
            box-sizing: border-box;
            z-index: 100002;
            opacity: 0;
            pointer-events: none;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            color: #f5ead8;
          }
          #sm-contact-modal.sm-active {
            opacity: 1;
            pointer-events: auto;
            transform: translate(-50%, -50%) scale(1);
          }
          .sm-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
          }
          .sm-modal-title {
            font-size: 22px;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: #f5ead8;
            margin: 0 0 6px;
          }
          .sm-modal-subtitle {
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 11px;
            color: #c67139;
            letter-spacing: 0.14em;
            text-transform: uppercase;
          }
          .sm-form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
          }
          .sm-form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
          }
          .sm-form-group.sm-full {
            grid-column: 1 / -1;
          }
          .sm-label {
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 10px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #a89f91;
          }
          .sm-input, .sm-select, .sm-textarea {
            background: #242120;
            border: 1px solid rgba(245, 234, 216, 0.15);
            border-radius: 6px;
            color: #f5ead8;
            padding: 10px 14px;
            font-size: 13px;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
          }
          .sm-input:focus, .sm-select:focus, .sm-textarea:focus {
            border-color: #c67139;
            box-shadow: 0 0 0 2px rgba(198, 113, 57, 0.2);
          }
          .sm-textarea {
            resize: vertical;
            min-height: 84px;
          }
          .sm-submit-btn {
            width: 100%;
            background: #c67139;
            color: #1a1817;
            border: none;
            border-radius: 6px;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 12px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-weight: 700;
            padding: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
          }
          .sm-submit-btn:hover {
            background: #dd854b;
            box-shadow: 0 6px 20px rgba(198, 113, 57, 0.35);
          }
          .sm-submit-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
          }
          .sm-status-msg {
            margin-top: 14px;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 11px;
            letter-spacing: 0.08em;
            padding: 10px 14px;
            border-radius: 6px;
            display: none;
          }
          .sm-status-msg.sm-success {
            display: block;
            background: rgba(46, 125, 50, 0.25);
            border: 1px solid #4caf50;
            color: #a5d6a7;
          }
          .sm-status-msg.sm-error {
            display: block;
            background: rgba(198, 40, 40, 0.25);
            border: 1px solid #ef5350;
            color: #ef9a9a;
          }
        </style>

        <!-- Backdrop -->
        <div id="sm-backdrop" class="sm-overlay-backdrop"></div>

        <!-- Menu Drawer -->
        <div id="sm-menu-drawer">
          <div class="sm-drawer-header">
            <span>Spec Media — Navigation</span>
            <button type="button" class="sm-close-btn" id="sm-menu-close">[ Close ]</button>
          </div>
          <div class="sm-nav-links">
            <a href="/work/" class="sm-nav-link-item">
              <span class="sm-nav-idx">01</span>
              <span class="sm-nav-label">Selected Work</span>
            </a>
            <a href="/studio/" class="sm-nav-link-item">
              <span class="sm-nav-idx">02</span>
              <span class="sm-nav-label">The Studio</span>
            </a>
            <a href="/capabilities/" class="sm-nav-link-item">
              <span class="sm-nav-idx">03</span>
              <span class="sm-nav-label">Capabilities</span>
            </a>
            <a href="/portal/" class="sm-nav-link-item">
              <span class="sm-nav-idx">04</span>
              <span class="sm-nav-label">CRM & Pipeline Portal</span>
            </a>
            <a href="#contact" class="sm-nav-link-item" id="sm-drawer-contact-trigger">
              <span class="sm-nav-idx">05</span>
              <span class="sm-nav-label">Direct Inquiry</span>
            </a>
          </div>
          <div class="sm-drawer-footer">
            <div>GLOBAL STUDIO: LONDON &bull; NEW YORK &bull; RIYADH</div>
            <div style="margin-top:4px">Connected to Live Supabase DB &bull; 2026</div>
          </div>
        </div>

        <!-- Contact Modal -->
        <div id="sm-contact-modal">
          <div class="sm-modal-header">
            <div>
              <h3 class="sm-modal-title">Start a Project</h3>
              <div class="sm-modal-subtitle">Supabase CRM Pipeline &bull; Direct Studio Ingestion</div>
            </div>
            <button type="button" class="sm-close-btn" id="sm-modal-close">[ Close ]</button>
          </div>
          <form id="sm-lead-form">
            <div class="sm-form-grid">
              <div class="sm-form-group">
                <label class="sm-label" for="sm-lead-name">Your Name *</label>
                <input class="sm-input" type="text" id="sm-lead-name" name="name" required placeholder="e.g. Alex Vance">
              </div>
              <div class="sm-form-group">
                <label class="sm-label" for="sm-lead-email">Work Email *</label>
                <input class="sm-input" type="email" id="sm-lead-email" name="email" required placeholder="alex@company.com">
              </div>
              <div class="sm-form-group">
                <label class="sm-label" for="sm-lead-company">Company / Entity</label>
                <input class="sm-input" type="text" id="sm-lead-company" name="company" placeholder="e.g. Apex Global">
              </div>
              <div class="sm-form-group">
                <label class="sm-label" for="sm-lead-discipline">Primary Discipline</label>
                <select class="sm-select" id="sm-lead-discipline" name="service">
                  <option value="Brand Strategy">Brand Strategy</option>
                  <option value="Campaign Production">Campaign Production</option>
                  <option value="Performance Media">Performance Media</option>
                  <option value="Content Systems">Content Systems</option>
                  <option value="Full Retainer">Full Studio Retainer</option>
                </select>
              </div>
              <div class="sm-form-group sm-full">
                <label class="sm-label" for="sm-lead-budget">Estimated Budget</label>
                <select class="sm-select" id="sm-lead-budget" name="budget">
                  <option value="25k-50k">$25,000 - $50,000</option>
                  <option value="50k-100k">$50,000 - $100,000</option>
                  <option value="100k+">$100,000+</option>
                  <option value="under-25k">Under $25,000</option>
                </select>
              </div>
              <div class="sm-form-group sm-full">
                <label class="sm-label" for="sm-lead-notes">Project Brief & Details *</label>
                <textarea class="sm-textarea" id="sm-lead-notes" name="notes" required placeholder="Outline your brand objectives, timeline, or key deliverables..."></textarea>
              </div>
            </div>
            <button type="submit" class="sm-submit-btn" id="sm-submit-btn">
              <span>Transmit Project Inquiry &rarr;</span>
            </button>
            <div id="sm-status-msg" class="sm-status-msg"></div>
          </form>
        </div>
      `;

      document.body.appendChild(uiContainer);

      var backdrop = document.getElementById('sm-backdrop');
      var drawer = document.getElementById('sm-menu-drawer');
      var modal = document.getElementById('sm-contact-modal');
      var form = document.getElementById('sm-lead-form');
      var statusMsg = document.getElementById('sm-status-msg');
      var submitBtn = document.getElementById('sm-submit-btn');

      function openMenu() {
        closeModal();
        backdrop.classList.add('sm-active');
        drawer.classList.add('sm-active');
      }

      function closeMenu() {
        drawer.classList.remove('sm-active');
        if (!modal.classList.contains('sm-active')) {
          backdrop.classList.remove('sm-active');
        }
      }

      function openModal() {
        closeMenu();
        backdrop.classList.add('sm-active');
        modal.classList.add('sm-active');
        var firstInput = document.getElementById('sm-lead-name');
        if (firstInput) setTimeout(function(){ firstInput.focus(); }, 100);
      }

      function closeModal() {
        modal.classList.remove('sm-active');
        if (!drawer.classList.contains('sm-active')) {
          backdrop.classList.remove('sm-active');
        }
      }

      backdrop.addEventListener('click', function() {
        closeMenu();
        closeModal();
      });

      document.getElementById('sm-menu-close').addEventListener('click', closeMenu);
      document.getElementById('sm-modal-close').addEventListener('click', closeModal);

      var drawerContact = document.getElementById('sm-drawer-contact-trigger');
      if (drawerContact) {
        drawerContact.addEventListener('click', function(ev) {
          ev.preventDefault();
          openModal();
        });
      }

      // Delegate all clicks on [ menu ] and [ contact ] across the entire page
      document.addEventListener('click', function(ev) {
        var target = ev.target;
        var a = target.closest ? target.closest('a') : null;
        if (!a) return;

        var href = a.getAttribute('href') || '';
        var text = (a.textContent || '').trim().toLowerCase();

        if (href === '#menu' || text === '[ menu ]') {
          ev.preventDefault();
          openMenu();
        } else if (href === '#contact' || text === '[ contact ]' || text.indexOf('hello@specmedia.co') !== -1) {
          ev.preventDefault();
          openModal();
        } else if (href === '#top' || text === '[ back to top ]') {
          ev.preventDefault();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }, true);

      // Handle form submission to Django API / Supabase
      form.addEventListener('submit', async function(ev) {
        ev.preventDefault();
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Transmitting to Supabase...</span>';
        statusMsg.className = 'sm-status-msg';
        statusMsg.style.display = 'none';

        var payload = {
          name: document.getElementById('sm-lead-name').value.trim(),
          email: document.getElementById('sm-lead-email').value.trim(),
          company: document.getElementById('sm-lead-company').value.trim(),
          service: document.getElementById('sm-lead-discipline').value,
          budget: document.getElementById('sm-lead-budget').value,
          notes: document.getElementById('sm-lead-notes').value.trim(),
          page_origin: 'landing'
        };

        try {
          var resp = await fetch('/api/contact/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
          });
          var data = await resp.json();

          if (resp.status === 201 && data.status === 'success') {
            statusMsg.textContent = 'Transmission received! Your project lead was recorded in Supabase (Lead #' + (data.lead ? data.lead.id.slice(0,8) : 'OK') + '). Our team will respond promptly.';
            statusMsg.className = 'sm-status-msg sm-success';
            statusMsg.style.display = 'block';
            form.reset();
            setTimeout(function() {
              closeModal();
            }, 3500);
          } else {
            statusMsg.textContent = data.message || 'Error recording submission. Please check all fields.';
            statusMsg.className = 'sm-status-msg sm-error';
            statusMsg.style.display = 'block';
          }
        } catch(err) {
          statusMsg.textContent = 'Network or server error: ' + err.message;
          statusMsg.className = 'sm-status-msg sm-error';
          statusMsg.style.display = 'block';
        } finally {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<span>Transmit Project Inquiry &rarr;</span>';
        }
      });

      // Press ESC to close modal or drawer
      window.addEventListener('keydown', function(ev) {
        if (ev.key === 'Escape') {
          closeMenu();
          closeModal();
        }
      });
    }, 150);

  } catch (err) {
    setStatus('Error unpacking: ' + err.message);
    console.error('Bundle unpack error:', err);
  }
});

  