def generate_cover(genre, mood, title):
    
    # Color palettes per genre
    palettes = {
        "Romcom": {
            "bg1": "#2d1b3d", "bg2": "#4a1942",
            "accent": "#ff6b9d", "symbol": "♡",
            "stars": "#ffb3d1"
        },
        "Suspense": {
            "bg1": "#0a0a0f", "bg2": "#1a1a2e",
            "accent": "#00d4ff", "symbol": "◈",
            "stars": "#4fc3f7"
        },
        "Fantasy": {
            "bg1": "#1a0a2e", "bg2": "#0d1b2a",
            "accent": "#c084fc", "symbol": "✦",
            "stars": "#e9d5ff"
        },
        "Sci-Fi": {
            "bg1": "#001a1a", "bg2": "#002a3a",
            "accent": "#00ff9f", "symbol": "◎",
            "stars": "#67e8f9"
        },
        "Horror": {
            "bg1": "#0a0000", "bg2": "#1a0505",
            "accent": "#ff3333", "symbol": "☽",
            "stars": "#fca5a5"
        },
        "Mystery": {
            "bg1": "#0f0a00", "bg2": "#1a1000",
            "accent": "#fbbf24", "symbol": "⊕",
            "stars": "#fde68a"
        }
    }

    # Default palette if genre not found
    palette = palettes.get(genre, {
        "bg1": "#1a1a2e", "bg2": "#0d1b2a",
        "accent": "#a89cf0", "symbol": "✦",
        "stars": "#e9d5ff"
    })

    # Mood-based opacity for atmosphere
    mood_opacity = {
        "Bittersweet": "0.6", "Chaotic": "0.9",
        "Dreamy": "0.4", "Tense": "0.8",
        "Nostalgic": "0.5", "Hopeful": "0.7"
    }
    opacity = mood_opacity.get(mood, "0.6")

    # Truncate title for display
    display_title = title if len(title) <= 20 else title[:18] + "..."

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="280" height="160" viewBox="0 0 280 160">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{palette['bg1']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{palette['bg2']};stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="280" height="160" fill="url(#bg)" rx="12"/>

  <!-- Atmospheric circles -->
  <circle cx="200" cy="40" r="60" fill="{palette['accent']}" opacity="0.08"/>
  <circle cx="80" cy="120" r="40" fill="{palette['accent']}" opacity="0.06"/>

  <!-- Stars/particles -->
  <circle cx="30" cy="20" r="1.5" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="80" cy="15" r="1" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="150" cy="25" r="1.5" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="220" cy="10" r="1" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="260" cy="35" r="1.5" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="40" cy="60" r="1" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="250" cy="80" r="1.5" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="20" cy="100" r="1" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="180" cy="140" r="1.5" fill="{palette['stars']}" opacity="{opacity}"/>
  <circle cx="120" cy="150" r="1" fill="{palette['stars']}" opacity="{opacity}"/>

  <!-- Main symbol -->
  <text x="140" y="85" 
        text-anchor="middle" 
        font-size="42" 
        fill="{palette['accent']}" 
        opacity="0.9"
        filter="url(#glow)">{palette['symbol']}</text>

  <!-- Genre label -->
  <text x="140" y="22" 
        text-anchor="middle" 
        font-family="Georgia, serif" 
        font-size="9" 
        fill="{palette['accent']}" 
        letter-spacing="3"
        opacity="0.8">{genre.upper()}</text>

  <!-- Divider line -->
  <line x1="100" y1="28" x2="180" y2="28" 
        stroke="{palette['accent']}" 
        stroke-width="0.5" 
        opacity="0.4"/>

  <!-- Title -->
  <text x="140" y="118" 
        text-anchor="middle" 
        font-family="Georgia, serif" 
        font-size="13" 
        font-weight="bold"
        fill="#f5f0e8">{display_title}</text>

  <!-- Mood -->
  <text x="140" y="138" 
        text-anchor="middle" 
        font-family="Georgia, serif" 
        font-size="9" 
        fill="{palette['stars']}"
        opacity="0.7"
        font-style="italic">{mood}</text>

  <!-- Bottom border accent -->
  <rect x="0" y="155" width="280" height="5" 
        fill="{palette['accent']}" 
        opacity="0.4" rx="0"/>
</svg>"""

    return svg