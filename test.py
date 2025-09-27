from nicegui import ui

# --- CSS: page, card, lens (lens is constrained to the card) ---
ui.add_css("""
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%}
body{background:linear-gradient(120deg,#1e1e2f,#111827);color:white;display:flex;align-items:center;justify-content:center}
#card{position:relative;overflow:hidden;width:min(860px,92vw);border-radius:16px;background:rgba(0,0,0,.55);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.12);padding:24px}
h1{font:700 28px/1.2 system-ui,ui-sans-serif,sans-serif;text-align:center;margin:8px 0 16px}
p{opacity:.9;text-align:center;margin:0 0 12px}

svg{position:fixed;top:-10000px}  /* keep helper SVGs off-screen */
#lens-map{width:0}

/* animated lens confined to the card */
@property --angle{syntax:"<angle>";inherits:false;initial-value:0deg}
#lens{
  --angle:0deg;
  --x:calc(50% + 40% * cos(var(--angle)));
  --y:calc(50% + 40% * sin(var(--angle)));
  position:absolute;left:var(--x);top:var(--y);
  width:200px;aspect-ratio:1/1;transform:translate(-50%,-50%);
  animation:10s linear infinite move;
  border-radius:50%;
  backdrop-filter:url(#drop);            /* 🔴 key line: SVG filter */
  box-shadow:inset 0 0 20px #3F51B5;     /* rim */
  mix-blend-mode:exclusion;              /* stylistic; try 'screen' too */
  pointer-events:none;
}
@keyframes move{0%{--angle:0deg}100%{--angle:359deg}}
""")

# --- SVG gradient map used by the displacement filter (same structure you shared) ---
ui.html('''
<svg id="lens-map" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">
  <style>#mix{mix-blend-mode:screen}</style>
  <linearGradient id="red">
    <stop offset="0%" stop-color="red"/><stop offset="100%" stop-color="red" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="blue" gradientTransform="rotate(90)">
    <stop offset="0%" stop-color="blue"/><stop offset="100%" stop-color="blue" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="grey">
    <stop offset="10%" stop-color="grey" stop-opacity="1"/>
    <stop offset="90%" stop-color="grey" stop-opacity="0"/>
    <stop offset="100%" stop-color="grey" stop-opacity="1"/>
  </radialGradient>
  <g>
    <rect width="1" height="1" fill="black"/>
    <rect width="1" height="1" fill="url(#red)"/>
    <rect width="1" height="1" fill="url(#blue)" id="mix"/>
    <rect width="1" height="1" fill="url(#grey)"/>
  </g>
</svg>
''')

# --- SVG filter that turns the map into a displacement lens (exact pattern) ---
ui.html('''
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="drop" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feImage href="#lens-map" />
      <feDisplacementMap in="SourceGraphic" scale="50" xChannelSelector="R" yChannelSelector="B" result="LENS"/>
      <feFlood flood-color="white" result="FLOOD"/>
      <feMerge><feMergeNode in="FLOOD"/><feMergeNode in="LENS"/></feMerge>
    </filter>
  </defs>
</svg>
''')

# --- CARD CONTENT (the lens sits inside this card and distorts its backdrop only) ---
ui.element('div').props('id="card"')
ui.label('Liquid-Glass Card with SVG Lens').style('display:block').classes('text-2xl font-bold')
ui.label('Backdrops inside this black translucent card are distorted by an animated SVG displacement lens.')
ui.separator().props('inset')

# Add a subtle textured background inside the card so the lens has something to “grab”.
# (You can remove this if your real app has imagery or colorful UI behind the lens.)
ui.element('div').style(
    'position:absolute;inset:0;z-index:0;opacity:.22;'
    'background:radial-gradient(800px 400px at 20% 0%,#60a5fa 0%,transparent 60%),'
    'radial-gradient(600px 500px at 85% 80%,#a78bfa 0%,transparent 60%),'
    'radial-gradient(400px 400px at 40% 70%,#34d399 0%,transparent 55%);'
)

# Foreground content wrapper (above the texture, below the lens rim)
ui.element('div').classes('relative z-10').style('display:grid;gap:12px')
ui.label('This text stays crisp.').style('opacity:.9')
ui.label('Tip: change filter scale=30–80, lens width, or animation speed to taste.').style('opacity:.7')

# The actual lens overlay (absolute, inside the card)
ui.element('section').props('id="lens"').style('z-index:20')

ui.run(native=False)
