# Pure OLED Black White desktop verification

Tested theme source **3.5.1** in Obsidian Desktop **1.15.1** on Windows on 24 November 2026. The desktop app loaded the repository stylesheet in an isolated vault with four fictional trail notes and a two-card Canvas. The tested stylesheet blob is 5e686fb5bb8fe99902419cc2d663b8edb9fd426e. [Tested source commit](https://github.com/tutivsoft-com/pure-oled-black-white/commit/ff432cf9f27ecb5c266ca7ce2d10da193fd0f89f)

## Fixes and retest

The previous Light off toggle had a white thumb on a pale blue-gray track. The rendered thumb and track measured **2.62:1**. The thumb and edge now use neutral blue-gray when off and blue when on. The track uses the base surface in both states.

| Scheme | Track | Off thumb and contrast | On thumb and contrast | Keyboard focus |
| --- | --- | --- | --- | --- |
| Dark | Black | #8494ab · 6.81:1 | #9bbfff · 11.29:1 | 2 px blue outline |
| Light | White | #6c7a90 · 4.35:1 | #285fbd · 6.07:1 | 2 px blue outline |

The baseline Light-mode primary button rendered identical idle and hover states. In Settings, the rendered primary button now changes its text and 1 px edge from blue to cyan on hover. Dark uses #9bbfff and #8bd7df. Light uses #285fbd and #087681. The button keeps the black or white surface and shows the native 3 px blue ring on keyboard focus. The hover check used the DevTools pseudo-state on the visible button in the restricted-mode settings page.

All four repository checks passed with `python -B -m unittest discover -s tests`. The suite checks CSS syntax, color values, contrast, button and toggle states, and manifest and README consistency.

## Desktop coverage

| Flow | Verified in Dark and Light |
| --- | --- |
| Notes and editor | Reading view, Live Preview, Source mode, selected text, headings, task states, rendered properties, links, tags, callouts, code, blockquotes, tables and embedded content. Followed an internal link. |
| Navigation and commands | File explorer, highlighted active note and tab, Global Search match colors, command palette selection, keyboard selection in Quick Switcher, note menu open and dismiss. |
| Core views | Canvas file and text cards with an edge on the base surface, Graph view and its filter section, Backlinks, Tags, File properties and Outline. |
| Settings | Appearance mode selector, theme selection and reapplication, font-size slider, toggle on/off clicks and keyboard focus. Opened the CSS snippets page in Light mode. Also opened Editor settings and verified the primary button hover and focus in Community plugins settings. |
| Compact window | Opened the note menu in a 680 × 720 desktop viewport with both sidebars collapsed. The 680 px workspace had no horizontal overflow, and the note had 636 px of content width. |

## Screenshots

These ten PNGs are direct captures of the tested desktop app. The vault contains only fictional test data.

| Capture | Size |
| --- | --- |
| [Dark Reading view with properties, tasks and callout](ui-verification-20261124/01-dark-reading.png) | 1024 × 800 |
| [Dark Source mode with editor selection](ui-verification-20261124/02-dark-source-selection.png) | 1024 × 800 |
| [Dark command palette with selected result](ui-verification-20261124/03-dark-command-palette.png) | 1024 × 800 |
| [Dark Canvas with two connected cards](ui-verification-20261124/04-dark-canvas.png) | 1024 × 800 |
| [Dark Appearance settings with the enabled, focused toggle](ui-verification-20261124/05-dark-appearance.png) | 900 × 700 |
| [Light Live Preview with editor selection](ui-verification-20261124/06-light-live-preview.png) | 1024 × 800 |
| [Light Global Search with highlighted matches](ui-verification-20261124/07-light-global-search.png) | 1024 × 800 |
| [Light Graph view with filters and both toggle states](ui-verification-20261124/08-light-graph.png) | 1024 × 800 |
| [Light note menu in the compact desktop viewport](ui-verification-20261124/09-light-narrow-menu.png) | 680 × 720 |
| [Light Appearance settings with the off toggle](ui-verification-20261124/10-light-appearance.png) | 900 × 700 |
