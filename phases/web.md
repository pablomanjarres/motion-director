# Web track: motion inside a site or app

Runs after the brief and direction. Output: motion implemented in the codebase,
tokens in one module, a reduced-motion path, and browser evidence.

## 1. The lightest runtime that keeps the intent

Extend the library the project already uses before adding another.

| Need | Start with | Move up when |
|---|---|---|
| hover, focus, color or shadow change | CSS transitions | the state spans components or must be interruptible: Motion |
| mount fade | CSS `@starting-style` | it needs an exit on unmount: Motion `AnimatePresence` |
| layout change, shared element, reorder, height to auto | Motion (`layout`, `layoutId`, `Reorder`) | |
| scroll reveal | Motion `whileInView` or `inView`, or CSS scroll-driven animation | pinning, scrubbing, snapping or long scroll stories: GSAP ScrollTrigger |
| choreographed timelines, SVG draw and morph, split text | GSAP | it becomes a video: the film track |
| designed vector loop (icon, illustration, loader) | dotLottie | it reacts to input: dotLottie state machines |

## 2. Tokens in one place

Durations by element: tooltip 80-120 ms, button 120-180 ms, card 200-350 ms, modal
300-400 ms, page transition 400-600 ms, a signature moment 600-900 ms. Exits run at
65 to 75 percent of the entrance. Hover feedback starts within 100 ms, press
feedback within 150 ms. Longer travel gets a longer duration.

Easing comes from the motion-language spec (`phases/direction.md`). With Motion,
prefer visual springs (`{ type: "spring", visualDuration: 0.4, bounce: 0.2 }`) and
no bounce on serious interfaces such as finance. Put every token in one module
(CSS custom properties or a `motion.ts`) owned by the design system; components
import it and never hardcode their own numbers.

## 3. Signature moments and the still-frame gate

Budget one hero moment, one proof moment and one interaction pattern shared across
components. A page where every section uses the same reveal fails. With motion
turned off, the page must still be complete and strong.

## 4. Reduced motion is a designed path

- React with Motion: `<MotionConfig reducedMotion="user">` at the app root, and `useReducedMotion()` for bespoke cases.
- GSAP: `gsap.matchMedia()` with a `reduceMotion: "(prefers-reduced-motion: reduce)"` condition.
- CSS: `@media (prefers-reduced-motion: reduce)`.
- Substitutes: slides become fades, parallax becomes static, scroll stories become numbered static sections, autoplay loops become poster frames. Focus and hover feedback stay, through color and border.

## 5. Correctness and performance

- Animate `transform` and `opacity`; never animate layout properties per frame. Set `will-change` only while something animates.
- Motion in React imports from `motion/react` (never `framer-motion`); server components use `motion/react-client`; hooks need `"use client"`. Keep `AnimatePresence` mounted with the condition inside and stable keys; make `layoutId` unique per instance with `useId()`; never read a MotionValue during render.
- GSAP: register plugins once; in React use `useGSAP` with a scope and let it clean up; wrap event-handler tweens with `contextSafe`; attach ScrollTrigger to top-level timelines only, call `ScrollTrigger.refresh()` after layout or font changes, and animate a pinned element's children rather than the element.
- dotLottie: prefer `.lottie` files, use workers when many animations run at once, lazy-load below the fold, destroy instances on unmount in vanilla code, and load it client-side only in SSR frameworks.
- Targets: 60 fps on a mid-range device, zero layout shift, no more than about 10 to 15 elements animating at once, and nothing above the fold hidden behind a scroll reveal.
- Read installed versions from `package.json` and check current docs before writing API calls (motion.dev serves every page as Markdown when `.md` is appended).

## 6. Evidence

Record the interaction in a real browser at normal and at reduced motion
(Playwright video, or a browser-automation tool that records a GIF). Grab start, middle and end frames. Then score the rubric.

## 7. Web rubric

Score each from 0 to 3: purpose, timing, hierarchy, brand fit, accessibility,
performance, implementation. Pass at 15 for internal tools, 18 for launches, 20 for
premium surfaces. Automatic fails: no reduced-motion path, motion that hides
controls or shifts layout, scroll pinning that traps reading, a page that is
weaker with motion off, or no browser evidence.

## Library reads for this track

| Need | Read |
|---|---|
| Motion for React, JS and Vue: official practices, CSS or Motion | `motion/motion` |
| Spring presets, parallax bands, magnetic and tilt recipes (trust `motion/motion` on API details) | `motion-dev/motion-dev-animations` |
| GSAP: core, timelines, ScrollTrigger, plugins, React, frameworks, utils, performance | `gsap/gsap-core`, `gsap/gsap-timeline`, `gsap/gsap-scrolltrigger`, `gsap/gsap-plugins`, `gsap/gsap-react`, `gsap/gsap-frameworks`, `gsap/gsap-utils`, `gsap/gsap-performance` |
| dotLottie playback, theming, state machines | `dotlottie/dotlottie-web` |
| UI motion principles, personality, reduced-motion substitutes | `motion-principles/motion-principles` |
| Logo animation and ambient backgrounds | `iart/logo-animation`, `iart/motion-background` |
| A motion audit of an existing site | `awesome-motion/web-motion-auditor` |
| Interface design and React quality | installed interface-design and React review skills |
