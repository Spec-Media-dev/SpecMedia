# 📋 INSTRUCTIONS FOR AI AGENT: ALL-IN-ONE SERVER VERSION

> **PURPOSE:**  
> This folder contains the **exact 1:1 server version** of the Hero & Video reveal sequence with all animations, timeline scrubbing, tile shuffle/convergence, and transitions bundled into a single file.

---

## 🌟 The All-in-One File: `intro-server-complete.html`

The primary file is:
👉 **[`intro-server-complete.html`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/intro-server-complete.html)** (or [`specmedia/intro-server-complete.html`](file:///c:/Users/acer/Desktop/specmedia/intro-server-complete.html))

It contains **EVERYTHING** inside one single HTML file:
1. **CDNs Included:** GSAP 3.12.5, ScrollTrigger, and Lenis 1.1.18.
2. **Styles Included:** All CSS rules (`.si-hero`, `.si-frame`, `.si-vid`, `.si-tiles`, `.si-tile`, `@media` queries, typography, dark background).
3. **Markup Included:** The full HTML structure with the fixed navbar logo dock, wordmark SVG, 24-slice dynamic container, video container, copy text, status circle, and skip button.
4. **JavaScript Included:** The complete 7-Phase GSAP timeline with ScrollTrigger scrub, fastseek video controller, 24-mosaic slice generator, on-load entrance animation, and debounced responsive resize.

---

## 🎯 How to Use This in the Website (`landing.html`)

When an agent is asked to replace the website's hero/first two sections:

1. **Open:** `c:\Users\acer\Desktop\specmedia\core\templates\landing.html`
2. **Remove:** Everything from the end of the navigation language bar down to right before `<section ref="{{ cardsRef }}" data-screen-label="03 Work grid">`.
3. **Paste:** The `<section id="spec-intro-hero" ...>` and `<style id="spec-intro-bundle-styles">` and `<script>` from [`intro-server-complete.html`](file:///c:/Users/acer/Documents/spec-intro-bundle/sections-01-and-02-bundle/intro-server-complete.html).
4. **Preserve:** Keep the React / DCLogic ref nodes (`logoRef`, `heroCueRef`, `heroCopyRef`, `scrubBoxRef`, etc.) which are already embedded in the markup.
