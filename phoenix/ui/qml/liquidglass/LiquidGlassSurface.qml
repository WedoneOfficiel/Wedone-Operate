// LiquidGlassSurface.qml - General-purpose glass surface/material container
// Base component for all Liquid Glass effects with blur, tint, fresnel, and distortion

import QtQuick
import QtQuick.Effects

Item {
    id: root
    
    // ============================================================
    // Public Properties - Override tokens as needed
    // ============================================================
    
    // Source item to capture for background blur (required)
    property Item backgroundSource: null
    
    // Material properties (default to token values)
    property real blurRadius: Tokens.effectiveBlurRadius
    property real downsampleFactor: Tokens.downsampleFactor
    property real baseOpacity: Tokens.effectiveOpacity
    property color tintColor: Tokens.tintColor
    property real tintStrength: Tokens.tintStrength
    property real noiseAmount: Tokens.noiseAmount
    property real distortionStrength: Tokens.distortionStrength
    property real highlightIntensity: Tokens.effectiveHighlightIntensity
    property real edgeFresnelPower: Tokens.edgeFresnelPower
    property color edgeHighlightColor: Tokens.edgeHighlightColor
    property real cornerRadius: Tokens.cornerRadius
    property real elevation: Tokens.elevation
    property color shadowColor: Tokens.shadowColor
    property bool readabilityMode: Tokens.readabilityMode
    
    // Interactive state (can be controlled externally)
    property bool hovered: false
    property bool pressed: false
    property point pointerPosition: Qt.point(width / 2, height / 2)
    
    // Animation time for shader effects
    property real animationTime: 0
    property bool reduceMotion: false
    
    // Content to display on top of the glass
    default property alias content: contentContainer.data
    
    // ============================================================
    // Private Properties - Computed from state
    // ============================================================
    
    // Animated highlight intensity with state modifiers
    property real _effectiveHighlight: highlightIntensity
    
    // Animated distortion with state modifiers
    property real _effectiveDistortion: distortionStrength
    
    // Normalized pointer position (0-1)
    readonly property point _normalizedPointer: Qt.point(
        pointerPosition.x / Math.max(width, 1),
        pointerPosition.y / Math.max(height, 1)
    )
    
    // Animation timer for subtle effects
    Timer {
        running: !root.reduceMotion && (root.hovered || root.pressed)
        repeat: true
        interval: 16  // ~60fps
        onTriggered: animationTime += 0.016
    }
    
    // State change handler to update animated properties
    onHoveredChanged: updateEffectiveValues()
    onPressedChanged: updateEffectiveValues()
    onHighlightIntensityChanged: updateEffectiveValues()
    onDistortionStrengthChanged: updateEffectiveValues()
    
    function updateEffectiveValues() {
        let baseHighlight = highlightIntensity
        if (pressed) baseHighlight += Tokens.pressedHighlightBoost
        else if (hovered) baseHighlight += Tokens.hoverHighlightBoost
        _effectiveHighlight = baseHighlight
        
        let baseDistortion = distortionStrength
        if (pressed) baseDistortion += Tokens.pressedDistortionBoost
        else if (hovered) baseDistortion += Tokens.hoverDistortionBoost
        _effectiveDistortion = baseDistortion
    }
    
    // Smooth animations for state changes
    Behavior on _effectiveHighlight {
        NumberAnimation {
            duration: Tokens.durationNormal
            easing.type: Tokens.easingStandard
        }
    }
    
    Behavior on _effectiveDistortion {
        NumberAnimation {
            duration: Tokens.durationNormal
            easing.type: Tokens.easingStandard
        }
    }
    
    // ============================================================
    // Shadow Layer
    // ============================================================
    
    Rectangle {
        id: shadowRect
        anchors.fill: parent
        anchors.margins: -elevation
        radius: cornerRadius + elevation / 2
        color: "transparent"
        
        // Use MultiEffect for shadow if available
        layer.enabled: elevation > 0
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: root.shadowColor
            shadowBlur: Math.min(root.elevation / 64, 1.0)  // Normalize to 0-1 range, clamped
            shadowVerticalOffset: root.elevation / 2
            shadowHorizontalOffset: 0
            shadowOpacity: 0.5
        }
    }
    
    // ============================================================
    // Background Capture & Blur
    // ============================================================
    
    // Capture the background content
    ShaderEffectSource {
        id: backgroundCapture
        sourceItem: root.backgroundSource
        anchors.fill: parent
        
        // Map to correct region of the source
        sourceRect: {
            if (!root.backgroundSource)
                return Qt.rect(0, 0, Math.max(1, root.width), Math.max(1, root.height))
            const origin = root.mapToItem(root.backgroundSource, 0, 0)
            return Qt.rect(origin.x, origin.y, Math.max(1, root.width), Math.max(1, root.height))
        }
        
        // Performance: enable texture mirroring and downsampling
        textureSize: Qt.size(
            Math.max(1, Math.round(root.width * root.downsampleFactor)),
            Math.max(1, Math.round(root.height * root.downsampleFactor))
        )
        
        live: true
        recursive: false
        hideSource: false
        visible: false
    }
    
    // ============================================================
    // Glass Effect Container
    // ============================================================
    
    Item {
        id: glassContainer
        anchors.fill: parent
        
        // Clip to rounded rectangle
        layer.enabled: true
        layer.effect: MultiEffect {
            maskEnabled: true
            maskThresholdMin: 0.5
            maskSpreadAtMin: 1.0
            maskSource: ShaderEffectSource {
                sourceItem: Rectangle {
                    width: root.width
                    height: root.height
                    radius: root.cornerRadius
                    color: "white"
                }
            }
        }
        
        // Blurred background with MultiEffect
        Item {
            id: blurredBackground
            anchors.fill: parent
            
            // Source image
            Image {
                id: sourceProxy
                anchors.fill: parent
                visible: false
            }
            
            // Apply blur using MultiEffect
            MultiEffect {
                id: blurEffect
                anchors.fill: parent
                source: backgroundCapture
                
                // Blur settings
                blurEnabled: true
                blurMax: 64
                blur: root.blurRadius / 64  // Normalize to 0-1
                blurMultiplier: 1.0
                
                // Saturation adjustment for glass feel
                saturation: readabilityMode ? -0.1 : 0.1
            }
        }
        
        // ============================================================
        // Glass Shader Effect - Lens Distortion, Chromatic Aberration, Fresnel
        // Creates realistic glass volume with edge highlights and color dispersion
        // ============================================================
        
        ShaderEffect {
            id: glassShader
            anchors.fill: parent
            
            // Shader uniforms
            property variant source: backgroundCapture
            property real time: root.animationTime
            property real opacity_: root.baseOpacity
            property color tint: root.tintColor
            property real tintStr: root.tintStrength
            property real noise: root.noiseAmount
            property real distortion: root._effectiveDistortion
            property real highlight: root._effectiveHighlight
            property real fresnel: root.edgeFresnelPower
            property color edgeColor: root.edgeHighlightColor
            property point pointer: root._normalizedPointer
            property real hoverState: root.hovered ? 1.0 : 0.0
            property real pressState: root.pressed ? 1.0 : 0.0
            property point resolution: Qt.point(root.width, root.height)
            property real cornerRad: root.cornerRadius / Math.min(root.width, root.height)
            
            // ========================================================
            // VERTEX SHADER
            // ========================================================
            vertexShader: "
                #version 440
                layout(location = 0) in vec4 qt_Vertex;
                layout(location = 1) in vec2 qt_MultiTexCoord0;
                layout(location = 0) out vec2 texCoord;
                layout(std140, binding = 0) uniform buf {
                    mat4 qt_Matrix;
                    float qt_Opacity;
                };
                void main() {
                    texCoord = qt_MultiTexCoord0;
                    gl_Position = qt_Matrix * qt_Vertex;
                }
            "
            
            // ========================================================
            // FRAGMENT SHADER - Realistic Glass Lens Effect
            // Features: Lens distortion, chromatic aberration, fresnel edges
            // ========================================================
            fragmentShader: "
                #version 440
                layout(location = 0) in vec2 texCoord;
                layout(location = 0) out vec4 fragColor;
                
                layout(std140, binding = 0) uniform buf {
                    mat4 qt_Matrix;
                    float qt_Opacity;
                };
                
                layout(binding = 1) uniform sampler2D source;
                
                // Custom uniforms
                layout(std140, binding = 2) uniform custom {
                    float time;
                    float opacity_;
                    vec4 tint;
                    float tintStr;
                    float noise;
                    float distortion;
                    float highlight;
                    float fresnel;
                    vec4 edgeColor;
                    vec2 pointer;
                    float hoverState;
                    float pressState;
                    vec2 resolution;
                    float cornerRad;
                };
                
                // Hash function for noise
                float hash(vec2 p) {
                    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
                }
                
                // Small epsilon to prevent division by zero when normalizing vectors near center
                const float NORMALIZE_EPSILON = 0.001;
                
                // 2D noise function
                float noise2D(vec2 p) {
                    vec2 i = floor(p);
                    vec2 f = fract(p);
                    f = f * f * (3.0 - 2.0 * f);
                    
                    float a = hash(i);
                    float b = hash(i + vec2(1.0, 0.0));
                    float c = hash(i + vec2(0.0, 1.0));
                    float d = hash(i + vec2(1.0, 1.0));
                    
                    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
                }
                
                void main() {
                    vec2 uv = texCoord;
                    vec2 center = vec2(0.5);
                    vec2 delta = uv - center;
                    float distFromCenter = length(delta);

                    // Refraction is strongest near the panel perimeter: this bends
                    // the captured image like a lens instead of applying blur alone.
                    float edgeLeft = uv.x;
                    float edgeRight = 1.0 - uv.x;
                    float edgeTop = uv.y;
                    float edgeBottom = 1.0 - uv.y;
                    float nearestEdge = min(min(edgeLeft, edgeRight), min(edgeTop, edgeBottom));
                    float edgeBand = 1.0 - smoothstep(0.015, 0.24, nearestEdge);

                    vec2 edgeNormal = vec2(0.0);
                    if (nearestEdge == edgeLeft) edgeNormal = vec2(1.0, 0.0);
                    else if (nearestEdge == edgeRight) edgeNormal = vec2(-1.0, 0.0);
                    else if (nearestEdge == edgeTop) edgeNormal = vec2(0.0, 1.0);
                    else edgeNormal = vec2(0.0, -1.0);

                    // Edge bending plus a mild convex bulge toward the centre.
                    // Offsets are normalized UV units, so they scale with the surface.
                    vec2 refractedUV = uv
                        + edgeNormal * (distortion * 0.18 * edgeBand)
                        + delta * (distortion * 0.10 * edgeBand);
                    refractedUV = clamp(refractedUV, 0.0, 1.0);
                    float edgeDispersionFactor = edgeBand;

                    // Add subtle noise-based distortion for organic glass feel
                    float n1 = noise2D(uv * 6.0 + time * 0.3);
                    float n2 = noise2D(uv * 8.0 - time * 0.2);
                    vec2 noiseOffset = vec2(n1 - 0.5, n2 - 0.5) * noise * 0.5;
                    
                    // === Real-time Edge Chromatic Dispersion ===
                    // Stronger chromatic aberration at edges, calculated in real-time
                    // Edge distance factor - stronger dispersion at glass perimeter
                    // Reuse the perimeter mask above for both refraction and dispersion.
                    
                    // Dynamic time-based modulation for living glass effect
                    float timeModulation = 1.0 + 0.1 * sin(time * 2.0 + distFromCenter * 6.0);
                    
                    // Chromatic aberration strength increases toward edges
                    // Base strength + edge-dependent strength + time modulation
                    float aberrationStrength = (0.0012 + edgeDispersionFactor * distortion * 0.035) * timeModulation;
                    
                    // Direction of dispersion - radial from center
                    // Add NORMALIZE_EPSILON to prevent NaN when delta is zero (at exact center)
                    vec2 aberrationDir = normalize(delta + vec2(NORMALIZE_EPSILON));
                    
                    // Different wavelengths refract at different angles
                    // Red refracts least, Blue refracts most (like real prism dispersion)
                    float redOffset = aberrationStrength * 0.45;  // Red - least refraction
                    float blueOffset = -aberrationStrength * 0.65; // Blue - most refraction
                    
                    // Sample each color channel with wavelength-dependent offsets
                    vec2 uvR = refractedUV + noiseOffset + aberrationDir * redOffset;
                    vec2 uvG = refractedUV + noiseOffset; // Green - middle (reference, no offset)
                    vec2 uvB = refractedUV + noiseOffset + aberrationDir * blueOffset;
                    
                    // Clamp UVs to valid range
                    uvR = clamp(uvR, 0.0, 1.0);
                    uvG = clamp(uvG, 0.0, 1.0);
                    uvB = clamp(uvB, 0.0, 1.0);
                    
                    // Sample background with chromatic aberration
                    float r = texture(source, uvR).r;
                    float g = texture(source, uvG).g;
                    float b = texture(source, uvB).b;
                    vec3 bgColor = vec3(r, g, b);
                    
                    // === Edge Dispersion Highlight ===
                    // Add subtle rainbow fringe at edges for visible dispersion effect
                    vec3 dispersionTint = vec3(0.0);
                    if (edgeDispersionFactor > 0.3) {
                        // Create rainbow gradient based on angle around center
                        float angle = atan(delta.y, delta.x);
                        float hue = (angle + 3.14159) / (2.0 * 3.14159); // 0-1
                        
                        // Convert hue to RGB (simplified HSV to RGB)
                        vec3 rainbow;
                        rainbow.r = abs(hue * 6.0 - 3.0) - 1.0;
                        rainbow.g = 2.0 - abs(hue * 6.0 - 2.0);
                        rainbow.b = 2.0 - abs(hue * 6.0 - 4.0);
                        rainbow = clamp(rainbow, 0.0, 1.0);
                        
                        // Subtle dispersion tint at edges
                        float dispersionIntensity = (edgeDispersionFactor - 0.3) * 0.15 * highlight;
                        dispersionTint = rainbow * dispersionIntensity;
                    }
                    
                    // === Fresnel Edge Effect ===
                    // Glass edges appear brighter due to internal reflection
                    float edgeFactor = pow(edgeDispersionFactor, fresnel);
                    edgeFactor = clamp(edgeFactor, 0.0, 1.0);
                    
                    // Smooth edge highlight following glass perimeter (white, not colored)
                    vec3 fresnelGlow = vec3(1.0) * edgeFactor * highlight * 0.6;
                    
                    // === Inner Highlight / Caustic Effect ===
                    // Simulates light focusing through the lens
                    float caustic = exp(-distFromCenter * distFromCenter * 6.0) * highlight * 0.3;
                    
                    // Secondary caustic ring
                    float ring = smoothstep(0.3, 0.35, distFromCenter) * smoothstep(0.45, 0.4, distFromCenter);
                    caustic += ring * highlight * 0.15;
                    
                    // === Edge Highlight Arc ===
                    // Top-left light source creates arc highlight
                    vec2 lightDir = normalize(vec2(-0.5, -0.7));
                    // Add NORMALIZE_EPSILON to prevent NaN when delta is zero (at exact center)
                    float lightAngle = dot(normalize(delta + vec2(NORMALIZE_EPSILON)), lightDir);
                    float arcHighlight = pow(max(0.0, lightAngle), 3.0) * edgeFactor * highlight * 0.6;
                    
                    // === Combine Effects ===
                    // Base glass color with subtle tint
                    vec3 glassColor = mix(bgColor, tint.rgb, tintStr * 0.5);
                    
                    // Add edge dispersion rainbow tint
                    glassColor += dispersionTint;
                    
                    // Add fresnel edge glow (white)
                    glassColor += fresnelGlow;
                    
                    // Add caustic/inner highlights
                    glassColor += vec3(1.0) * caustic;
                    
                    // Add arc highlight
                    glassColor += vec3(1.0, 0.98, 0.95) * arcHighlight;
                    
                    // === Glass Volume Opacity ===
                    // Edges slightly more opaque (thicker glass)
                    float volumeOpacity = opacity_ + edgeFactor * 0.15;
                    
                    // Center slightly more transparent (thinner/clearer)
                    volumeOpacity -= (1.0 - distFromCenter) * 0.05;
                    volumeOpacity = clamp(volumeOpacity, 0.1, 0.95);
                    
                    fragColor = vec4(glassColor, volumeOpacity) * qt_Opacity;
                }
            "
        }
        
        // ============================================================
        // Readability Overlay (when enabled)
        // ============================================================
        
        Rectangle {
            id: readabilityOverlay
            anchors.fill: parent
            color: Qt.rgba(0, 0, 0, Tokens.readabilityOverlayOpacity)
            visible: root.readabilityMode
            opacity: root.readabilityMode ? 1.0 : 0.0
            
            Behavior on opacity {
                NumberAnimation {
                    duration: Tokens.durationNormal
                    easing.type: Tokens.easingStandard
                }
            }
        }
        
        // ============================================================
        // Content Container
        // ============================================================
        
        Item {
            id: contentContainer
            anchors.fill: parent
            anchors.margins: 1  // Slight inset to avoid edge clipping
        }
    }
}
