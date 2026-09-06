import base64
import os
import io
from PIL import Image

def main():
    src_img_path = r"C:\Users\Rithish S\.gemini\antigravity\brain\daa1693f-689d-4169-a399-5f01b8a330c4\media__1787797402843.jpg"
    dest_dir = r"C:\Users\Rithish S\.gemini\antigravity\scratch\Rethika-2782"
    dest_svg_path = os.path.join(dest_dir, "rethika_banner.svg")
    
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    print(f"Loading image from {src_img_path}...")
    if not os.path.exists(src_img_path):
        print(f"Error: Source image not found at {src_img_path}")
        return
        
    img = Image.open(src_img_path)
    print(f"Original image size: {img.size}")
    
    # Crop and resize to 1000x380 for a wide banner
    # The character is standing in the center. We want to crop a wide window.
    # To keep her face and upper body, let's crop from the top half.
    width, height = img.size
    target_aspect = 1000.0 / 380.0
    
    # If image is vertical, we crop a 1000x380 aspect ratio box.
    # Let's crop from Y=0.05*height to Y=0.75*height to capture her face and torso.
    crop_width = width
    crop_height = int(width / target_aspect)
    
    # Center horizontally, start slightly from top vertically
    left = 0
    top = int(height * 0.05)
    right = width
    bottom = top + crop_height
    
    if bottom > height:
        # Fallback if crop goes out of bounds
        bottom = height
        crop_height = bottom - top
        crop_width = int(crop_height * target_aspect)
        left = (width - crop_width) // 2
        right = left + crop_width

    print(f"Cropping box: left={left}, top={top}, right={right}, bottom={bottom}")
    cropped_img = img.crop((left, top, right, bottom))
    resized_img = cropped_img.resize((1000, 380), Image.Resampling.LANCZOS)
    
    # Convert to RGB and compress as JPEG
    jpeg_buffer = io.BytesIO()
    resized_img.convert("RGB").save(jpeg_buffer, format="JPEG", quality=75)
    jpeg_data = jpeg_buffer.getvalue()
    
    # Base64 encode
    base64_str = base64.b64encode(jpeg_data).decode("utf-8")
    img_src = f"data:image/jpeg;base64,{base64_str}"
    print("Image compressed and base64 encoded successfully.")
    
    # SVG content with indigo/neon violet theme
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1000 380" width="100%" height="100%">
  <defs>
    <!-- Deep space glass overlay gradient -->
    <linearGradient id="glassGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a0518" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#05030c" stop-opacity="0.92"/>
    </linearGradient>
    
    <!-- Neon violet glow filter -->
    <filter id="violetGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#a855f7" flood-opacity="0.6"/>
    </filter>

    <!-- Scanline pattern -->
    <pattern id="scanlines" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000" stroke-width="1.5" opacity="0.12" />
    </pattern>

    <!-- Path for rotating circular text (centered at X=840, Y=100, Radius=55) -->
    <path id="textCircle" d="M 840, 45 a 55,55 0 1,1 -0.1,0 Z" />
  </defs>

  <style>
    .term-text {{
      font-family: 'Fira Code', Consolas, Monaco, 'Courier New', Courier, monospace;
      font-size: 14.5px;
      fill: #f8f8f2;
    }}
    
    .cursor {{
      fill: #a855f7;
      animation: blink 0.8s infinite;
    }}
    
    .monokai-keyword {{ fill: #ec4899; font-weight: bold; }}
    .monokai-var {{ fill: #f59e0b; }}
    .monokai-string {{ fill: #eab308; }}
    .monokai-type {{ fill: #06b6d4; font-style: italic; }}
    .monokai-val {{ fill: #a855f7; }}

    /* Circular HUD Styles */
    .hud-text {{
      font-family: 'Fira Code', Consolas, Monaco, monospace;
      font-size: 9px;
      font-weight: 600;
      fill: #a855f7;
      letter-spacing: 2px;
    }}

    .hud-circle {{
      fill: none;
      stroke: #a855f7;
      stroke-width: 1;
      opacity: 0.4;
      stroke-dasharray: 4, 4;
    }}

    .hud-center {{
      font-family: 'Fira Code', Consolas, Monaco, monospace;
      font-size: 18px;
      font-weight: bold;
      fill: #ec4899;
    }}
    
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
  </style>

  <!-- BACKGROUND: Cropped & Resized Image -->
  <image xlink:href="{img_src}" width="1000" height="380" preserveAspectRatio="xMidYMid slice" />

  <!-- Scanlines Overlay -->
  <rect width="1000" height="380" fill="url(#scanlines)" />

  <!-- Left Side: Terminal Console Overlay -->
  <g transform="translate(40, 45)">
    <!-- Terminal Window Glass Frame -->
    <rect width="470" height="290" rx="12" fill="url(#glassGrad)" stroke="#a855f7" stroke-width="1.5" filter="url(#violetGlow)" />
    
    <!-- Title Bar -->
    <path d="M 0,12 A 12,12 0 0 1 12,0 L 458,0 A 12,12 0 0 1 470,12 L 470,35 L 0,35 Z" fill="#0d081d" />
    
    <!-- Window Control Buttons -->
    <circle cx="20" cy="18" r="6" fill="#ef4444" /> <!-- Red -->
    <circle cx="38" cy="18" r="6" fill="#eab308" /> <!-- Yellow -->
    <circle cx="56" cy="18" r="6" fill="#10b981" /> <!-- Green -->
    
    <!-- Title Text -->
    <text x="235" y="23" font-family="'Fira Code', monospace" font-size="12" fill="#7c6f9f" text-anchor="middle" font-weight="bold">rethika@ai-engine: ~</text>

    <!-- Terminal Content Area -->
    <g transform="translate(25, 45)">
      <!-- Line 1: init_profile.sh -->
      <g opacity="0">
        <text class="term-text" x="0" y="30">
          <tspan fill="#06b6d4">$</tspan> ./init_profile.sh --verbose
        </text>
        <animate attributeName="opacity" from="0" to="1" begin="0.5s" dur="0.1s" fill="freeze" />
      </g>
      
      <!-- Line 2: Identity loading -->
      <g opacity="0">
        <text class="term-text" x="0" y="65">
          <tspan class="monokai-keyword">[+]</tspan> <tspan class="monokai-var">identity</tspan> = <tspan class="monokai-string">"Rethika S (BE CSE)"</tspan>;
        </text>
        <animate attributeName="opacity" from="0" to="1" begin="1.6s" dur="0.1s" fill="freeze" />
      </g>

      <!-- Line 3: Academic standing -->
      <g opacity="0">
        <text class="term-text" x="0" y="100">
          <tspan class="monokai-keyword">[+]</tspan> <tspan class="monokai-var">academics</tspan> = <tspan class="monokai-string">"CGPA 9.52 / 10.0"</tspan>;
        </text>
        <animate attributeName="opacity" from="0" to="1" begin="2.8s" dur="0.1s" fill="freeze" />
      </g>

      <!-- Line 4: Core Specializations -->
      <g opacity="0">
        <text class="term-text" x="0" y="135">
          <tspan class="monokai-keyword">[+]</tspan> <tspan class="monokai-var">stack</tspan> = <tspan class="monokai-string">"React | Next.js | Django | Python"</tspan>;
        </text>
        <animate attributeName="opacity" from="0" to="1" begin="4.0s" dur="0.1s" fill="freeze" />
      </g>

      <!-- Line 5: Focus / Goal -->
      <g opacity="0">
        <text class="term-text" x="0" y="170">
          <tspan class="monokai-keyword">[+]</tspan> <tspan class="monokai-var">focus</tspan> = <tspan class="monokai-string">"Exploring Agentic AI &amp; Mesh Nodes"</tspan>;
        </text>
        <animate attributeName="opacity" from="0" to="1" begin="5.2s" dur="0.1s" fill="freeze" />
      </g>
      
      <!-- Blinking Cursor -->
      <rect class="cursor" x="355" y="195" width="10" height="18" />
      <text x="0" y="210" font-family="'Fira Code', monospace" font-size="15" fill="#a855f7">$ <tspan fill="#f8f8f2">_</tspan></text>
    </g>
  </g>

  <!-- Right Side: Rotating Cyber-Badge HUD -->
  <g filter="url(#violetGlow)" transform="translate(40, 0)">
    <!-- Rotating Text Path Group -->
    <g>
      <text class="hud-text">
        <textPath xlink:href="#textCircle" startOffset="0%">• FULL STACK DEVELOPER • AI EXPLORER • LEADERSHIP VP •</textPath>
      </text>
      <animateTransform attributeName="transform" type="rotate" from="0 840 100" to="360 840 100" dur="16s" repeatCount="indefinite" />
    </g>

    <!-- HUD Graphics -->
    <circle cx="840" cy="100" r="62" class="hud-circle" stroke-dasharray="2, 6" />
    <circle cx="840" cy="100" r="48" class="hud-circle" stroke-width="0.5" />
    <circle cx="840" cy="100" r="45" class="hud-circle" stroke-dasharray="8, 2" />
    
    <text x="840" y="106" class="hud-center" text-anchor="middle">&gt;_</text>
  </g>
</svg>
"""

    print(f"Writing compiled SVG banner to {dest_svg_path}...")
    with open(dest_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print("SUCCESS: rethika_banner.svg generated successfully.")

if __name__ == "__main__":
    main()
