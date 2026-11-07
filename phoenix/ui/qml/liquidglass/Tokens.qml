// Tokens.qml - Centralized Design Tokens for Liquid Glass Components
// All components reference these tokens rather than hardcoding values
pragma Singleton
import QtQuick

QtObject {
    id: tokens

    // ============================================================
    // Quality Presets (Low/Medium/High) - affects performance
    // ============================================================
    enum QualityPreset { Low, Medium, High }
    property int qualityPreset: 2  // Default to High (enum value 2)

    // Computed values based on quality preset
    readonly property real downsampleFactor: {
        switch (qualityPreset) {
            case Tokens.QualityPreset.Low: return 0.25
            case Tokens.QualityPreset.Medium: return 0.5
            case Tokens.QualityPreset.High: return 1.0
        }
    }
    
    readonly property real blurRadius: {
        switch (qualityPreset) {
            case Tokens.QualityPreset.Low: return 20
            case Tokens.QualityPreset.Medium: return 32
            case Tokens.QualityPreset.High: return 48
        }
    }

    // ============================================================
    // Glass Material Properties
    // ============================================================
    
    // Base opacity of the glass surface (0.0 - 1.0)
    // Lower = more transparent, Higher = more frosted
    property real baseOpacity: 0.35
    
    // Tint color applied to the glass
    // Context-aware: can be changed dynamically based on background
    property color tintColor: Qt.rgba(1.0, 1.0, 1.0, 0.1)
    
    // Strength of the tint effect (0.0 - 1.0)
    property real tintStrength: 0.15
    
    // ============================================================
    // Distortion & Refraction
    // ============================================================
    
    // Amount of noise-based distortion for refraction effect
    // Higher = more warped/liquid appearance
    property real noiseAmount: 0.02
    
    // Overall distortion strength (0.0 - 0.1 typical)
    property real distortionStrength: 0.015
    
    // ============================================================
    // Highlight & Fresnel Effects
    // ============================================================
    
    // Intensity of specular highlights (0.0 - 1.0)
    property real highlightIntensity: 0.6
    
    // Fresnel power for edge highlighting
    // Higher = sharper edge effect, Lower = softer gradient
    property real edgeFresnelPower: 2.5
    
    // Edge highlight color
    property color edgeHighlightColor: Qt.rgba(1.0, 1.0, 1.0, 0.8)
    
    // ============================================================
    // Shape & Shadow
    // ============================================================
    
    // Corner radius for glass surfaces
    property real cornerRadius: 16
    
    // Elevation level (affects shadow size and blur)
    property real elevation: 8
    
    // Shadow color
    property color shadowColor: Qt.rgba(0, 0, 0, 0.25)
    
    // ============================================================
    // Readability & Accessibility
    // ============================================================
    
    // Enable readability mode for better text contrast
    // When true: increases opacity, reduces background contrast
    property bool readabilityMode: false
    
    // Readability overlay opacity (applied when readabilityMode is true)
    property real readabilityOverlayOpacity: 0.3
    
    // Focus ring color for keyboard navigation
    property color focusRingColor: Qt.rgba(0.4, 0.6, 1.0, 0.8)
    
    // Focus ring width
    property real focusRingWidth: 2
    
    // ============================================================
    // Motion Tokens - Animation Durations & Easing
    // ============================================================
    
    // Standard animation duration (ms)
    property int durationFast: 100
    property int durationNormal: 200
    property int durationSlow: 350
    
    // Spring animation properties
    property real springMass: 1.0
    property real springStiffness: 200
    property real springDamping: 20
    
    // Easing curves
    readonly property int easingStandard: Easing.OutCubic
    readonly property int easingEnter: Easing.OutQuart
    readonly property int easingExit: Easing.InQuart
    readonly property int easingBounce: Easing.OutBack
    
    // ============================================================
    // Interactive State Modifiers
    // ============================================================
    
    // Hover state modifications
    property real hoverHighlightBoost: 0.3
    property real hoverScaleBoost: 1.02
    property real hoverDistortionBoost: 0.005
    
    // Pressed state modifications - elastic expansion effect
    property real pressedScaleExpand: 1.08  // Button expands on press
    property real pressedHighlightBoost: 0.5
    property real pressedDistortionBoost: 0.01
    
    // Disabled state modifications
    property real disabledOpacity: 0.5
    
    // ============================================================
    // Color Palette
    // ============================================================
    
    // Text colors
    property color textPrimary: Qt.rgba(1.0, 1.0, 1.0, 0.95)
    property color textSecondary: Qt.rgba(1.0, 1.0, 1.0, 0.7)
    property color textDisabled: Qt.rgba(1.0, 1.0, 1.0, 0.4)
    
    // Accent colors
    property color accentPrimary: Qt.rgba(0.4, 0.6, 1.0, 1.0)
    property color accentSecondary: Qt.rgba(0.6, 0.4, 1.0, 1.0)
    
    // ============================================================
    // Computed Properties for Readability Mode
    // ============================================================
    
    readonly property real effectiveOpacity: readabilityMode ? 
        Math.min(baseOpacity + 0.2, 0.8) : baseOpacity
    
    readonly property real effectiveBlurRadius: readabilityMode ?
        blurRadius * 1.2 : blurRadius
    
    readonly property real effectiveHighlightIntensity: readabilityMode ?
        highlightIntensity * 0.7 : highlightIntensity
}
