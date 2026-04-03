# Accessibility

## Standard
- The Chimera widget must meet WCAG 2.1 Level AA compliance.
- Accessibility is not optional. Every UI component must be accessible from day one.

## Requirements
- All interactive elements must be keyboard navigable (Tab, Enter, Escape, Arrow keys).
- Hints and tours must be announced to screen readers via ARIA live regions (`aria-live="polite"`).
- All hint containers must have appropriate ARIA roles (`role="tooltip"`, `role="dialog"` for tours).
- Focus management: when a hint appears, focus moves to it. When dismissed, focus returns to the trigger element.
- Color contrast: all text meets 4.5:1 ratio against its background. Use `prefers-color-scheme` for dark mode.
- Animations: respect `prefers-reduced-motion`. If set, disable all transitions and animations.
- All images/icons have `alt` text or `aria-label`.
- The spatial overlay (bounding box) must be operable via keyboard (arrow keys to adjust, Enter to confirm).

## Testing
- Run axe-core in CI on all widget components.
- Include keyboard-only navigation tests in the E2E suite.
- Test with at least one screen reader (NVDA or VoiceOver) before major releases.
