# Rendering the profile animations
Real-time Three.js scenes, captured frame by frame with Playwright and encoded to GIF.

    npm i three@0.160.0 playwright
    python3 -m http.server 8765 &
    node render.js hero 120 && node render.js mods,roblox,city 72
    # then for each scene:
    ffmpeg -framerate 24 -i frames/<scene>/%03d.png -vf "split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse" -loop 0 <scene>.gif
