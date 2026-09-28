# 📋 INSTRUCTIONS FOR AI AGENT: RESTORE & INTEGRATE SECTIONS 01 & 02

> **ROLE / PURPOSE:**  
> You are an expert frontend and animation engineer. Your task is to update `core/templates/landing.html` by **removing the existing hero / intro section(s)** and **replacing them with the two clean, modular sections** provided in this folder:
> 1. **Section 01: Hero Section** (Dynamic wordmark flight, headline, copy, discipline pills, ambient spotlight).
> 2. **Section 02: Frame Scrub Section** (24-tile staggered blur reveal, duck poster hold, stage fullscreen expansion, and video scrubbing).

---

## 📁 Manifest of This Folder

| File | Purpose |
|---|---|
| [`section-01-hero.html`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/section-01-hero.html) | Standalone HTML markup for Section 01 (Hero). |
| [`section-02-video.html`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/section-02-video.html) | Standalone HTML markup for Section 02 (Mosaic & Video Scrub). |
| [`sections-combined.html`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/sections-combined.html) | **Combined drop-in markup** containing both Section 01 and Section 02. |
| [`section-01-hero.js`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/section-01-hero.js) | JavaScript controller for Section 01 (`initHeroLogoFlight()`). |
| [`section-02-video.js`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/section-02-video.js) | JavaScript controller for Section 02 (`initSection2Controller()`). |
| [`sections-01-02.css`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/sections-01-02.css) | Supporting CSS styles for stages, mosaic tiles, and responsiveness. |

---

## 🎯 Step-by-Step Integration Protocol

### Step 1: Target Location in `landing.html`
Open:
`c:\Users\acer\Desktop\specmedia\core\templates\landing.html`

Find the start of the hero section right after the navigation language bar:
```html
<a href="/ar/" id="spec-landing-lang-ar" ...>العربية</a>
```
and right before Section 03:
```html
<section ref="{{ cardsRef }}" data-screen-label="03 Work grid" ...>
<!-- OR -->
<section ref="{{ cardsRef }}" id="work" data-screen-label="03 Work grid" ...>
```

### Step 2: Remove the Existing Section(s)
Delete whatever section is currently placed between the language bar and Section 03 (e.g. `<section id="spec-intro-hero" ...>` and its entire contents).

### Step 3: Insert the New Sections HTML
In that exact location, insert the full contents of:
[`sections-combined.html`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/sections-combined.html)

> ⚠️ **CRITICAL REQUIREMENT:** Keep all `ref="{{ ... }}"` nodes intact (`logoRef`, `heroCueRef`, `heroCopyRef`, `scrubBoxRef`, `canvasScrubRef`, etc.) as they are already included inside `sections-combined.html` to guarantee flawless React / DCLogic runtime hydration.

---

### Step 4: Verify CSS Styles in `<style>`
Make sure the rules from [`sections-01-02.css`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/sections-01-02.css) are present in the `<style>` block:
- `#spec-scene2-stage` dimensions, aspect ratios, and media queries.
- `.spec-tile` and `.spec-tile img` styles.
- `.spec-hero-title`, `.spec-hero-desc`, and `#spec-hero-ambient-glow`.

---

### Step 5: Replace / Register JavaScript Controllers
In the `<script>` block of `landing.html`:
1. Include the function `initHeroLogoFlight()` from [`section-01-hero.js`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/section-01-hero.js).
2. Include the function `initSection2Controller()` from [`section-02-video.js`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/section-02-video.js).
3. Update `bootAllControllers()` to initialize both:
```js
function bootAllControllers() {
  var f = initHeroLogoFlight();
  var s = initSection2Controller();
  var r = initReviewsScrollOnly();
  return f && s && r;
}
```

---

## 🔍 Step 6: Verification Checklist
After applying the changes:
1. **Section 01 (Hero):**
   - Wordmark centers dynamically on page load.
   - On scroll, wordmark scales down smoothly and docks into the navbar.
   - Dynamic contrast: turns black when scrolling past light sections (`03 Work grid`), turns white on dark sections.
2. **Section 02 (Frame Scrub):**
   - 24 mosaic tiles reveal and assemble with cubic easing.
   - Master reference poster holds briefly.
   - Central frame expands to fullscreen (100vw × 100vh).
   - Video scrubs accurately without blocking smooth page scroll.
   - Transitions smoothly into Section 03 Work Grid.
