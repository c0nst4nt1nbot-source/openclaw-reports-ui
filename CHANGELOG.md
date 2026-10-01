# Changelog - OpenClaw Reports UI

## Version 1.1 (2026-03-05)

### Changed
- **Renamed application** from "OpenClaw Intelligence Dashboard" to "OpenClaw Reports UI"
- **Directory renamed** from `/home/dg/openclaw-ui/` to `/home/dg/openclaw-reports-ui/`
- All documentation updated to reflect new branding

### Added
- **Dark Mode** - Toggle between light and dark themes
  - Theme toggle button in navigation bar
  - Preference persists using localStorage
  - Smooth color transitions
  - Comprehensive dark theme with proper contrast
  - Icons: 🌙 (light mode) / ☀️ (dark mode)

### Technical Details

**Dark Mode Implementation:**
- CSS custom properties (variables) for all colors
- `data-theme="dark"` attribute on `<html>` element
- JavaScript toggle function with localStorage persistence
- Automatic theme loading on page load
- 0.3s transition animations for smooth theme switching

**Color Scheme:**
- Light mode: Clean white/gray palette
- Dark mode: Professional dark gray (#1a1a1a, #2d2d2d) with blue accents
- High contrast for accessibility
- Consistent badge and alert colors in both themes

**Files Modified:**
- `/templates/base.html` - Complete rewrite with dark mode CSS and JavaScript
- `/app.py` - Updated branding
- `/start.sh` - Updated branding
- `/README.md` - Updated name and paths
- `/QUICKSTART.md` - Updated name, paths, and added dark mode section
- `/DEPLOYMENT_SUMMARY.md` - Updated all references
- All template files - Updated page titles

## Version 1.0 (2026-03-05)

### Initial Release
- Report browser with search
- Database explorer with SQL query interface
- Markdown rendering
- Read-only security model
- Lightweight Flask backend

---

**Current Version**: 1.1  
**Last Updated**: 2026-03-05  
**Status**: ✅ Production Ready
