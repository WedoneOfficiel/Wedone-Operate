# Qt Liquid Glass Widget Library

A PySide6/QML component library implementing Apple-style "Liquid Glass" material effects with translucent glass surfaces, background blur, context-aware tinting, reflection/refraction-like feel, edge highlights (Fresnel/specular), soft shadows, and dynamic interaction responses.

## Features

- **Translucent Glass Material**: Frosted glass appearance with configurable opacity and blur
- **Background Blur**: Qt6 MultiEffect-based blur with downsampling for performance
- **Context-Aware Tinting**: Subtle colorization based on background content
- **Fresnel Edge Highlights**: Realistic edge lighting that intensifies at angles
- **Specular Highlights**: Moving highlight that follows pointer position
- **Soft Shadows**: Elevation-based shadows for depth
- **Dynamic Interactions**: Hover/press/drag states with smooth animations
- **Accessibility**: Keyboard focus support, readable contrast modes

## Components

| Component | Description |
|-----------|-------------|
| `LiquidGlassSurface` | Base glass material container with blur, tint, and effects |
| `LiquidGlassButton` | Interactive button with ripple and specular sweep effects |
| `LiquidGlassPanel` | Card/dialog surface with header, content, and footer |
| `LiquidGlassSlider` | Slider with glass track and enhanced knob during drag |

## Requirements

- Python 3.8+
- PySide6 >= 6.5.0 (Qt 6.5+ required for QtQuick.Effects)
- OpenGL 3.3+ capable graphics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the demo application:

```bash
python main.py
```

### Using Components in Your QML

```qml
import QtQuick
import "path/to/components" as LG

// Use the singleton tokens for consistent styling
LG.Tokens.baseOpacity = 0.4
LG.Tokens.readabilityMode = true

// Create a glass button
LG.LiquidGlassButton {
    text: "Click Me"
    backgroundSource: yourBackgroundItem
    onClicked: console.log("Clicked!")
}

// Create a glass panel
LG.LiquidGlassPanel {
    title: "Settings"
    subtitle: "Configure your preferences"
    backgroundSource: yourBackgroundItem
    showFooter: true
    
    // Panel content
    Text { text: "Content goes here" }
    
    // Footer buttons
    footerContent: [
        LG.LiquidGlassButton { text: "Save" }
    ]
}
```

## Design Tokens

All visual properties are centralized in `Tokens.qml`:

| Token | Default | Description |
|-------|---------|-------------|
| `blurRadius` | 48 (High) | Background blur amount |
| `downsampleFactor` | 1.0 (High) | Blur input downsampling for performance |
| `baseOpacity` | 0.35 | Glass surface opacity |
| `tintColor` | white@10% | Glass tint color |
| `tintStrength` | 0.15 | Tint intensity |
| `highlightIntensity` | 0.6 | Specular highlight strength |
| `edgeFresnelPower` | 2.5 | Edge highlight sharpness |
| `cornerRadius` | 16 | Surface corner radius |
| `elevation` | 8 | Shadow depth |
| `readabilityMode` | false | Enhanced contrast for text |

### Quality Presets

```qml
// Set quality preset (affects blur and downsample)
LG.Tokens.qualityPreset = LG.Tokens.QualityPreset.High   // Best quality
LG.Tokens.qualityPreset = LG.Tokens.QualityPreset.Medium // Balanced
LG.Tokens.qualityPreset = LG.Tokens.QualityPreset.Low    // Best performance
```

## Performance Tips

1. **Use `downsampleFactor`**: Lower values (0.25-0.5) significantly improve blur performance
2. **Limit blur region**: Components automatically clip to their bounds
3. **Enable caching**: `ShaderEffectSource` caching is enabled by default
4. **Quality presets**: Use `Low` or `Medium` on integrated graphics

## Project Structure

```
Qt-liquid-glass-widgets/
├── main.py                 # PySide6 entry point
├── requirements.txt        # Python dependencies
├── qml/
│   ├── Main.qml           # Demo application
│   └── components/
│       ├── qmldir         # QML module definition
│       ├── Tokens.qml     # Design tokens (singleton)
│       ├── LiquidGlassSurface.qml
│       ├── LiquidGlassButton.qml
│       ├── LiquidGlassPanel.qml
│       └── LiquidGlassSlider.qml
└── README.md
```

## Shader Implementation Notes

The glass effect uses custom GLSL fragment shaders with:

- **Noise-based distortion**: Procedural 2D noise for subtle refraction
- **Pointer-influenced distortion**: Distortion follows cursor on hover/press
- **Fresnel calculation**: Edge factor from UV distance for rim lighting
- **Dual specular highlights**: Primary + secondary for depth

## License

See [LICENSE](LICENSE) file.
