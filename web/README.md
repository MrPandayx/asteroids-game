# Asteroids Game - Web Deployment Guide

## 🚀 Web Version Setup

This folder contains the web-compatible version of your Asteroids Game that can be deployed to Cloudflare Pages.

### 📁 Files Structure:

```
web/
├── index.html          # Main HTML page
├── main.py            # Web-compatible game code (async)
├── constants.py       # Game constants
├── circleshape.py     # Base game object class
├── player.py          # Player ship class
├── asteroid.py        # Asteroid class
├── asteroidfield.py   # Asteroid spawning system
├── shot.py           # Bullet class
├── shake.py          # Power-up class
├── shakefield.py     # Power-up spawning
├── save_system.py    # Simplified save system for web
└── requirements.txt  # Python dependencies
```

## 🛠️ Local Development

### 1. Install Dependencies

```bash
pip install pygame-ce pygbag
```

### 2. Build Web Version

```bash
cd web
python -m pygbag main.py --width 1280 --height 720 --name "Asteroids Game"
```

### 3. Test Locally

The command above will:

- Compile your Python game to WebAssembly
- Start a local web server
- Open the game in your browser

## ☁️ Cloudflare Pages Deployment

### Option 1: Direct Upload

1. Run the pygbag build command above
2. Copy the generated `dist/` folder contents
3. Upload to Cloudflare Pages dashboard
4. Set custom domain if desired

### Option 2: GitHub Integration

1. Push the `web/` folder to a GitHub repository
2. Connect Cloudflare Pages to your GitHub repo
3. Set build command: `python -m pygbag main.py --width 1280 --height 720`
4. Set output directory: `dist/`
5. Deploy automatically on git push

### Build Settings for Cloudflare Pages:

- **Build command**: `pip install pygame-ce pygbag && python -m pygbag main.py --width 1280 --height 720 --name "Asteroids Game"`
- **Output directory**: `dist`
- **Node.js version**: Not required (Python project)

## 🎮 Game Features (Web Version)

✅ **Full Game Functionality**:

- 1000 levels of increasing difficulty
- Player movement with WASD keys
- Shooting with spacebar
- Collision detection
- Lives system (3 hearts)
- Space background with animated stars

✅ **Menu System**:

- Main menu with Play/Shop/Quit buttons
- Shop interface for skin customization
- Game over screen with stats

✅ **Coin & Shop System**:

- Earn 1 coin per level completed
- 10 different ship skins to purchase
- Special rainbow skin with animated effects
- Persistent coin storage (session-based in web)

✅ **Power-ups**:

- McDonald's shake power-ups
- Rapid-fire shooting ability
- Visual power-up collection effects

## 🌐 Web-Specific Changes

### Differences from Desktop Version:

1. **Async Game Loop**: Uses `asyncio` for web compatibility
2. **Simplified Save System**: Session-based storage (no file I/O)
3. **No Browser Opening**: GitHub link shows message instead
4. **Optimized Performance**: Reduced complexity for web deployment

### Browser Compatibility:

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (responsive design)

## 📱 Mobile Support

The web version includes responsive design:

- Automatically scales on mobile devices
- Touch-friendly interface
- Optimized canvas size for different screens

## 🎨 Customization

### Styling:

- Edit `index.html` for visual changes
- Modify CSS for custom themes
- Add your own branding/colors

### Game Settings:

- Adjust constants in `constants.py`
- Modify difficulty progression
- Add new features to game classes

## 🚀 Deployment Tips

1. **Performance**: Keep the game under 50MB for faster loading
2. **Assets**: Minimize external dependencies
3. **SEO**: Update meta tags in `index.html`
4. **Analytics**: Add tracking code if needed
5. **Domain**: Use custom domain for professional appearance

## 🔧 Troubleshooting

### Common Issues:

- **Black screen**: Check browser console for errors
- **Controls not working**: Ensure canvas has focus
- **Slow performance**: Try reducing screen resolution
- **Build errors**: Verify pygame-ce and pygbag versions

### Debug Mode:

Add `--debug` flag to pygbag command for detailed error messages.

## 📊 Features Comparison

| Feature        | Desktop Version | Web Version   |
| -------------- | --------------- | ------------- |
| Full Gameplay  | ✅              | ✅            |
| Save System    | File-based      | Session-based |
| Performance    | Native          | WebAssembly   |
| Installation   | Required        | None          |
| Sharing        | Executable      | URL Link      |
| Mobile Support | No              | Yes           |

## 🎯 Next Steps

1. **Test the web version locally**
2. **Deploy to Cloudflare Pages**
3. **Share your game URL**
4. **Collect player feedback**
5. **Add analytics and improvements**

Your Asteroids Game is now ready for the web! 🌟
