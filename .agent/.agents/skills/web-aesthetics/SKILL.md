---
name: web-aesthetics
description: Ensures any generated vanilla CSS/JS web app features a premium, modern design. Enforces vibrant colors, glassmorphism, micro-animations, and high-quality typography over MVP placeholders.
origin: Custom Ensemble
---

# Premium Web Aesthetics

Never deliver "minimum viable" or generic designs. Web applications and simulations must visually "Wow" the user immediately.

## When to Activate

- Generating a new vanilla HTML/CSS/JS frontend.
- Styling interactive simulations (e.g., physics/math visualizations).
- Refactoring UI components.
- Building a web-based lab report.

## Core Rules

1. **Vibrant & Harmonious Palettes**: Avoid basic web colors (`red`, `blue`, `green`). Use HSL color palettes tailored for modern dark/light modes.
2. **Modern Typography**: Never use browser defaults (Times New Roman). Always link to modern Google Fonts (e.g., Inter, Roboto, Outfit) and establish a clear typography hierarchy.
3. **Dynamic Interactions**: Interfaces must feel alive. Apply smooth CSS transitions (`transition: all 0.3s ease`) to all interactive elements (buttons, cards, links). Use micro-animations on hover and focus states.
4. **Premium Techniques**: Utilize modern CSS features like Glassmorphism (`backdrop-filter: blur()`), subtle gradients, and soft box-shadows to create depth.
5. **No Placeholders**: If a design requires an image or icon, generate a working demonstration asset or use high-quality SVGs, do not use ugly text placeholders like "[IMAGE HERE]".

## Implementation Checklist

Before presenting UI code:
- [ ] Are custom fonts imported and applied to the `body`?
- [ ] Does every button and link have a `:hover` and `:active` state with a smooth transition?
- [ ] Is the color palette sophisticated (e.g., using CSS variables for `--primary`, `--surface`, `--text-muted`)?
- [ ] Are spacing (margins/padding) consistent, using relative units (`rem`, `em`) or a standardized spacing system?
- [ ] Does the design look better than a basic bootstrap template?

## Banned Patterns

- Using generic `<button>` styles without custom padding, border-radius, and hover states.
- Hardcoding `px` values for fonts instead of responsive `rem` sizing.
- Stark `#000000` text on `#FFFFFF` backgrounds. Use softer contrasts (e.g., `#111827` on `#F9FAFB`).
- Completely static elements that do not react to user interaction.
