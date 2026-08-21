// Builds the two distributable single-file variants into dist/:
//   dist/green-empire.html — standalone page, open it directly in a browser
//   dist/artifact.html     — same game as a fragment for the Artifact runtime,
//                            which supplies its own <html>/<head>/<body>
// Both inline assets/art.js so they need no sibling files.
// Usage: node assets/bundle.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const ROOT = new URL('../', import.meta.url).pathname;
const FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?' +
  'family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap">';

let html = readFileSync(ROOT + 'index.html', 'utf8');
const art = readFileSync(ROOT + 'assets/art.js', 'utf8');

const tag = '<script src="./assets/art.js"></script>';
if (!html.includes(tag)) throw new Error('art.js script tag not found in index.html');
html = html.replace(tag, '<script>' + art + '</script>');
if (html.includes('assets/art.js')) throw new Error('art.js was not fully inlined');

mkdirSync(ROOT + 'dist', { recursive: true });
writeFileSync(ROOT + 'dist/green-empire.html', html);

// The Artifact runtime wraps the file in its own document skeleton, so ship
// only the stylesheet link, the <style> block and the body content.
const style = html.slice(html.indexOf('<style>'), html.indexOf('</head>'));
const body = html.slice(html.indexOf('<body>') + 6, html.lastIndexOf('</body>'));
writeFileSync(ROOT + 'dist/artifact.html', FONTS + '\n' + style + '\n' + body);

const mb = (p) => (readFileSync(ROOT + p).length / 1048576).toFixed(2) + ' MB';
console.log('dist/green-empire.html', mb('dist/green-empire.html'));
console.log('dist/artifact.html    ', mb('dist/artifact.html'));
