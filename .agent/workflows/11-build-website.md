# Workflow: Build Website

**Objective**: End-to-end pipeline for building a production-quality website or web application from specification to deployment-ready state. Enforces premium aesthetics, SEO best practices, and responsive design.

## Trigger Conditions
- User wants to build a website or web UI
- User says "build a website for..." or "create a landing page"
- Invoked via `/build-website`

## Execution Sequence

### Phase 1 — Requirements & Design
1. **Gather Requirements**: Identify:
   - Purpose (landing page, dashboard, portfolio, e-commerce, SaaS)
   - Target audience and devices (mobile-first vs. desktop-first)
   - Content inventory (pages, sections, media assets)
   - Branding inputs (colors, fonts, logo, tone)
2. **Technology Selection**: Choose stack based on complexity:
   - **Static site**: HTML + CSS + vanilla JS (simple landing pages)
   - **SPA**: Vite + React/Vue (interactive applications)
   - **Full-stack**: Next.js (SSR, API routes, authentication)
3. **Design System**: Define before writing any component:
   - Color palette (primary, secondary, accent, neutral scale)
   - Typography scale (font family, sizes, weights, line heights)
   - Spacing system (4px base grid)
   - Border radius, shadow, and animation tokens
4. **Wireframe**: Describe the page layout in structured markdown or generate a visual mockup.

**Gate**: Confirm technology choice and design tokens with user before building.

### Phase 2 — Foundation
1. **Project Init**: Use `npx -y` with appropriate framework (e.g., `npx -y create-vite@latest ./ --template react`).
2. **Design System CSS**: Create `index.css` or equivalent with all design tokens as CSS custom properties.
3. **Layout Shell**: Build the responsive layout container (header, main, footer).
4. **Typography**: Import Google Fonts and apply the type scale.
5. **Dark Mode**: Implement `prefers-color-scheme` media query support from the start.

### Phase 3 — Component Development
For each page section:
1. **Build Component**: Write semantic HTML with proper heading hierarchy.
2. **Style Component**: Apply design system tokens — NO ad-hoc colors or magic numbers.
3. **Add Interactivity**: Hover effects, scroll animations, micro-interactions.
4. **Responsive Check**: Test at 320px, 768px, 1024px, 1440px breakpoints.
5. **Accessibility**: Proper alt text, ARIA labels, keyboard navigation, color contrast (4.5:1 minimum).

### Phase 4 — Content & Assets
1. **Copy**: Write or integrate all text content. No lorem ipsum in final output.
2. **Images**: Generate or source all images. Use `generate_image` tool for hero sections and illustrations — NO placeholder images.
3. **SEO**: For every page:
   - Unique `<title>` tag (50-60 characters)
   - `<meta name="description">` (150-160 characters)
   - Single `<h1>` per page
   - Semantic HTML5 elements (`<nav>`, `<main>`, `<article>`, `<section>`)
   - Open Graph tags for social sharing
4. **Performance**: Lazy-load images below the fold, minimize CSS/JS.

### Phase 5 — Verification
1. **Visual Review**: Open in browser and verify at all breakpoints.
2. **Lighthouse Audit**: Run performance, accessibility, SEO, and best practices checks.
3. **Link Check**: Verify all internal and external links work.
4. **Form Validation**: Test all interactive elements (forms, buttons, modals).
5. **Cross-Browser**: Verify in Chrome and Firefox at minimum.

**Gate**: All Lighthouse scores must be > 80. If any are below, fix before proceeding.

### Phase 6 — Delivery
1. **Build**: Run `npm run build` to generate production bundle.
2. **Deploy Instructions**: Write deployment steps for the chosen platform (Vercel, Netlify, GitHub Pages).
3. **Log**: Record the website creation in `session-context.md`.

## Failure Paths
- **Design Disagreement**: If user rejects the design direction, return to Phase 1 step 4 and iterate on the wireframe.
- **Build Errors**: If `npm run build` fails, fix all errors before delivery. Never deliver a broken build.
- **Performance Issues**: If Lighthouse performance < 80, optimize images, defer scripts, and minimize CSS.
- **Missing Content**: If user hasn't provided copy, generate professional placeholder content and mark as "NEEDS REVIEW."

## Quality Standards
- ❌ NO generic colors (plain red, blue, green) — use curated palettes
- ❌ NO browser default fonts — always import modern typography
- ❌ NO placeholder images in final delivery
- ✅ Smooth gradients and micro-animations
- ✅ Glassmorphism, dark mode, or other modern design patterns
- ✅ Mobile-first responsive design

## Output Organization (Rule 20)
Website code lives in the project directory (not in `docs/`). Log creation to `session-context.md`.
