// LiquidGlassSlider.qml - Slider with Liquid Glass track and knob
// Features: glass track + enhanced glass knob during drag

import QtQuick
import QtQuick.Controls

Slider {
    id: root
    
    // ============================================================
    // Public Properties
    // ============================================================
    
    // Source item for background blur
    property Item backgroundSource: null
    
    // Slider styling
    property real trackHeight: 8
    property real knobSize: 28
    property color trackColor: Qt.rgba(1, 1, 1, 0.15)
    property color activeTrackColor: Tokens.accentPrimary
    
    // Material overrides
    property real blurRadius: Tokens.effectiveBlurRadius
    property real baseOpacity: Tokens.effectiveOpacity
    property real highlightIntensity: Tokens.effectiveHighlightIntensity
    
    // Accessibility
    Accessible.role: Accessible.Slider
    Accessible.name: "Liquid glass slider"
    Accessible.description: "Value: " + Math.round(value * 100) / 100
    
    // Default size
    implicitWidth: 200
    implicitHeight: Math.max(knobSize, trackHeight) + 16
    
    // Focus handling
    focusPolicy: Qt.StrongFocus
    
    // ============================================================
    // Internal State
    // ============================================================
    
    property real _dragProgress: pressed ? 1.0 : 0.0
    property real _hoverProgress: hovered ? 1.0 : 0.0
    property bool _knobHovered: knobHoverHandler.hovered
    
    Behavior on _dragProgress {
        NumberAnimation {
            duration: Tokens.durationNormal
            easing.type: Tokens.easingStandard
        }
    }
    
    Behavior on _hoverProgress {
        NumberAnimation {
            duration: Tokens.durationNormal
            easing.type: Tokens.easingStandard
        }
    }
    
    // ============================================================
    // Background (Track)
    // ============================================================
    
    background: Item {
        id: trackContainer
        width: root.availableWidth
        height: root.trackHeight
        y: (root.availableHeight - height) / 2
        x: root.leftPadding
        
        // Track background (inactive portion)
        Rectangle {
            id: trackBackground
            anchors.fill: parent
            radius: height / 2
            color: root.trackColor
            
            // Subtle glass effect on track
            layer.enabled: true
            layer.effect: Item {
                // Simple blur simulation for track
                Rectangle {
                    anchors.fill: parent
                    radius: parent.height / 2
                    color: Qt.rgba(1, 1, 1, 0.05)
                }
            }
            
            // Track hover glow
            Rectangle {
                anchors.fill: parent
                anchors.margins: -2
                radius: (height + 4) / 2
                color: "transparent"
                border.color: Qt.rgba(1, 1, 1, 0.2 * root._hoverProgress)
                border.width: 1
                
                Behavior on border.color {
                    ColorAnimation { duration: Tokens.durationNormal }
                }
            }
        }
        
        // Active track portion (filled)
        Rectangle {
            id: activeTrack
            width: root.visualPosition * parent.width
            height: parent.height
            radius: height / 2
            
            // Gradient for active portion
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { 
                    position: 0.0
                    color: Qt.darker(root.activeTrackColor, 1.2)
                }
                GradientStop { 
                    position: 1.0
                    color: root.activeTrackColor
                }
            }
            
            // Glow effect during drag
            Rectangle {
                anchors.fill: parent
                anchors.margins: -3
                radius: (height + 6) / 2
                color: "transparent"
                border.color: Qt.rgba(
                    root.activeTrackColor.r,
                    root.activeTrackColor.g,
                    root.activeTrackColor.b,
                    0.4 * root._dragProgress
                )
                border.width: 2
                
                Behavior on border.color {
                    ColorAnimation { duration: Tokens.durationNormal }
                }
            }
        }
    }
    
    // ============================================================
    // Handle (Knob)
    // ============================================================
    
    handle: Item {
        id: knobContainer
        x: root.leftPadding + root.visualPosition * (root.availableWidth - width)
        y: root.topPadding + (root.availableHeight - height) / 2
        width: root.knobSize
        height: root.knobSize
        
        HoverHandler {
            id: knobHoverHandler
        }
        
        // Knob scale animation
        transform: Scale {
            origin.x: knobContainer.width / 2
            origin.y: knobContainer.height / 2
            
            // Scale up during drag for "liquid glass" feel
            xScale: 1.0 + 0.15 * root._dragProgress + 0.05 * (root._knobHovered ? 1 : 0)
            yScale: xScale
            
            Behavior on xScale {
                SpringAnimation {
                    spring: Tokens.springStiffness
                    damping: Tokens.springDamping
                    mass: Tokens.springMass
                }
            }
        }
        
        // Knob glass surface
        LiquidGlassSurface {
            id: knobGlass
            anchors.fill: parent
            backgroundSource: root.backgroundSource
            cornerRadius: width / 2
            
            // Enhanced glass during drag
            blurRadius: root.blurRadius * (1 + 0.3 * root._dragProgress)
            baseOpacity: root.baseOpacity + 0.15 * root._dragProgress
            highlightIntensity: root.highlightIntensity + 
                0.3 * root._dragProgress +
                0.15 * (root._knobHovered ? 1 : 0)
            distortionStrength: Tokens.distortionStrength * (1 + 2 * root._dragProgress)
            elevation: Tokens.elevation * (1 + 0.5 * root._dragProgress)
            
            hovered: root._knobHovered
            pressed: root.pressed
            
            // Inner highlight for depth
            Rectangle {
                anchors.centerIn: parent
                width: parent.width * 0.6
                height: parent.height * 0.6
                radius: width / 2
                
                gradient: Gradient {
                    GradientStop { position: 0.0; color: Qt.rgba(1, 1, 1, 0.3) }
                    GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.1) }
                    GradientStop { position: 1.0; color: "transparent" }
                }
                
                rotation: -45
                opacity: 0.5 + 0.5 * root._dragProgress
                
                Behavior on opacity {
                    NumberAnimation { duration: Tokens.durationNormal }
                }
            }
            
            // Bright rim during drag (enhanced Fresnel)
            Rectangle {
                anchors.fill: parent
                radius: width / 2
                color: "transparent"
                border.color: Qt.rgba(1, 1, 1, 0.6 * root._dragProgress)
                border.width: 2
                
                Behavior on border.color {
                    ColorAnimation { duration: Tokens.durationNormal }
                }
            }
        }
        
        // Focus ring
        Rectangle {
            anchors.fill: parent
            anchors.margins: -Tokens.focusRingWidth - 2
            radius: width / 2 + Tokens.focusRingWidth + 2
            color: "transparent"
            border.color: Tokens.focusRingColor
            border.width: Tokens.focusRingWidth
            visible: root.activeFocus
            opacity: root.activeFocus ? 1.0 : 0.0
            
            Behavior on opacity {
                NumberAnimation { duration: Tokens.durationFast }
            }
        }
    }
    
    // ============================================================
    // Value Tooltip (shown during drag)
    // ============================================================
    
    Item {
        id: tooltip
        x: handle.x + handle.width / 2 - width / 2
        y: handle.y - height - 8
        width: tooltipText.width + 16
        height: tooltipText.height + 8
        
        visible: opacity > 0
        opacity: root._dragProgress
        
        Behavior on opacity {
            NumberAnimation { duration: Tokens.durationFast }
        }
        
        Rectangle {
            anchors.fill: parent
            radius: 6
            color: Qt.rgba(0, 0, 0, 0.7)
            
            // Slight glass effect
            border.color: Qt.rgba(1, 1, 1, 0.2)
            border.width: 1
        }
        
        Text {
            id: tooltipText
            anchors.centerIn: parent
            text: Math.round(root.value * 100) / 100
            color: Tokens.textPrimary
            font.pixelSize: 12
            font.weight: Font.Medium
        }
        
        // Tooltip arrow
        Rectangle {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.bottom
            anchors.topMargin: -2
            width: 8
            height: 8
            rotation: 45
            color: Qt.rgba(0, 0, 0, 0.7)
        }
    }
    
    // ============================================================
    // Keyboard Handling
    // ============================================================
    
    Keys.onLeftPressed: decrease()
    Keys.onRightPressed: increase()
    Keys.onDownPressed: decrease()
    Keys.onUpPressed: increase()
}
