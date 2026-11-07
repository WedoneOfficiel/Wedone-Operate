// LiquidGlassButton.qml - Interactive button with Liquid Glass material
// Features: real glass volume effect with lens distortion, edge highlights, chromatic aberration
// Press interaction: elastic expansion with spring-back animation

import QtQuick
import QtQuick.Controls
import QtQuick.Effects

AbstractButton {
    id: root
    
    // ============================================================
    // Public Properties
    // ============================================================
    
    // Source item for background blur
    property Item backgroundSource: null
    
    // Button styling
    property real cornerRadius: Tokens.cornerRadius
    property color textColor: enabled ? Tokens.textPrimary : Tokens.textDisabled
    property real fontSize: 14
    property bool showIcon: false
    property string iconSource: ""
    
    // Material overrides
    property real blurRadius: Tokens.effectiveBlurRadius
    property real baseOpacity: Tokens.effectiveOpacity
    property color tintColor: Tokens.tintColor
    property real highlightIntensity: Tokens.effectiveHighlightIntensity
    
    // Accessibility
    Accessible.role: Accessible.Button
    Accessible.name: text
    Accessible.description: "Liquid glass button"
    
    // Default size
    implicitWidth: Math.max(100, contentRow.implicitWidth + 32)
    implicitHeight: 44
    
    // Focus handling
    focusPolicy: Qt.StrongFocus
    
    // ============================================================
    // Internal State
    // ============================================================
    
    property real _hoverProgress: 0
    property real _pressScale: 1.0  // Animated scale for press effect
    property point _pointerPos: Qt.point(width / 2, height / 2)
    
    // Track hover position
    HoverHandler {
        id: hoverHandler
        onPointChanged: {
            if (hovered) {
                root._pointerPos = Qt.point(point.position.x, point.position.y)
            }
        }
    }
    
    // Smooth state transitions
    Behavior on _hoverProgress {
        NumberAnimation {
            duration: Tokens.durationNormal
            easing.type: Tokens.easingStandard
        }
    }
    
    // State bindings
    states: [
        State {
            name: "disabled"
            when: !root.enabled
            PropertyChanges { target: root; _hoverProgress: 0 }
        },
        State {
            name: "pressed"
            when: root.pressed && root.enabled
        },
        State {
            name: "hovered"
            when: root.hovered && root.enabled && !root.pressed
            PropertyChanges { target: root; _hoverProgress: 1 }
        },
        State {
            name: "default"
            when: !root.hovered && !root.pressed && root.enabled
            PropertyChanges { target: root; _hoverProgress: 0 }
        }
    ]
    
    // Elastic press animation - expand on press, spring back on release
    onPressedChanged: {
        if (pressed) {
            pressExpandAnimation.stop()
            pressReleaseAnimation.stop()
            pressExpandAnimation.start()
        } else {
            pressExpandAnimation.stop()
            pressReleaseAnimation.start()
        }
    }
    
    // Press expand animation - quick expansion
    NumberAnimation {
        id: pressExpandAnimation
        target: root
        property: "_pressScale"
        to: Tokens.pressedScaleExpand
        duration: Tokens.durationFast
        easing.type: Easing.OutCubic
    }
    
    // Release animation - spring back with overshoot
    // Note: SpringAnimation spring/damping expect values in range 0-5 typically
    // Tokens.springStiffness (200) / 50 = 4.0 spring rate
    // Tokens.springDamping (20) / 100 = 0.2 damping ratio
    SpringAnimation {
        id: pressReleaseAnimation
        target: root
        property: "_pressScale"
        to: 1.0
        spring: Tokens.springStiffness / 50
        damping: Tokens.springDamping / 100
        mass: Tokens.springMass
    }
    
    // ============================================================
    // Visual Representation
    // ============================================================
    
    background: Item {
        id: buttonBackground
        
        // Elastic scale animation centered on button
        transform: Scale {
            id: scaleTransform
            origin.x: buttonBackground.width / 2
            origin.y: buttonBackground.height / 2
            xScale: root._pressScale * (1 + (Tokens.hoverScaleBoost - 1) * root._hoverProgress)
            yScale: xScale
        }
        
        // Glass surface with lens effect
        LiquidGlassSurface {
            id: glassSurface
            anchors.fill: parent
            backgroundSource: root.backgroundSource
            cornerRadius: root.cornerRadius
            blurRadius: root.blurRadius
            baseOpacity: root.enabled ? 
                (root.baseOpacity + 0.05 * root._hoverProgress) :
                (root.baseOpacity * Tokens.disabledOpacity)
            tintColor: root.tintColor
            highlightIntensity: root.highlightIntensity + 
                Tokens.hoverHighlightBoost * root._hoverProgress
            distortionStrength: Tokens.distortionStrength +
                Tokens.hoverDistortionBoost * root._hoverProgress
            hovered: root.hovered
            pressed: root.pressed
            pointerPosition: root._pointerPos
            elevation: Tokens.elevation * (1 + 0.3 * root._hoverProgress)
            
            // No harsh sweep or ripple effects - the glass shader handles all visual effects
        }
    }
    
    // ============================================================
    // Content
    // ============================================================
    
    contentItem: Row {
        id: contentRow
        anchors.centerIn: parent
        spacing: 8
        
        // Optional icon
        Image {
            id: iconImage
            source: root.iconSource
            width: 20
            height: 20
            visible: root.showIcon && root.iconSource !== ""
            anchors.verticalCenter: parent.verticalCenter
            opacity: root.enabled ? 1.0 : Tokens.disabledOpacity
            
            Behavior on opacity {
                NumberAnimation { duration: Tokens.durationNormal }
            }
        }
        
        // Text label
        Text {
            id: buttonText
            text: root.text
            color: root.textColor
            font.pixelSize: root.fontSize
            font.weight: Font.Medium
            anchors.verticalCenter: parent.verticalCenter
            
            Behavior on color {
                ColorAnimation { duration: Tokens.durationNormal }
            }
        }
    }
    
    // ============================================================
    // Keyboard Handling
    // ============================================================
    
    Keys.onReturnPressed: {
        if (enabled) {
            clicked()
        }
    }
    
    Keys.onSpacePressed: {
        if (enabled) {
            clicked()
        }
    }
}
