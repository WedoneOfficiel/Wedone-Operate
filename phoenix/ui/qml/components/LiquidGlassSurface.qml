import QtQuick
import "../liquidglass" as LiquidGlass

Item {
    id: root
    default property alias content: material.content
    property Item backdropItem
    property color tint: "#DDFBFDFF"
    property real cornerRadius: 18
    property real refraction: 4.0
    property real blurAmount: 1.0
    property real materialOpacity: 0.96
    property real borderOpacity: 0.72
    property color rimColor: "#BFFFFFFF"
    property bool shadowEnabled: false
    property real shadowOpacity: 0.18
    property bool reduceMotion: false
    property real pointerLift: 0
    property vector2d pointerPosition: Qt.vector2d(width * 0.5, height * 0.25)
    readonly property bool _hovered: hoverHandler.hovered
    readonly property bool _pressed: pressHandler.pressed

    HoverHandler {
        id: hoverHandler
        onPointChanged: {
            if (hovered)
                root.pointerPosition = Qt.vector2d(point.position.x, point.position.y)
        }
    }
    TapHandler { id: pressHandler }

    LiquidGlass.LiquidGlassSurface {
        id: material
        anchors.fill: parent
        backgroundSource: root.backdropItem
        cornerRadius: root.cornerRadius
        blurRadius: Math.max(0, Math.min(64, root.blurAmount * 24))
        downsampleFactor: 1.0
        // Keep the upstream library's material defaults instead of remapping
        // them through the old hand-written shader's unrelated opacity scale.
        baseOpacity: 0.35
        tintColor: root.tint
        tintStrength: 0.15
        distortionStrength: Math.max(0.0, root.refraction) * 0.0025
        highlightIntensity: Math.max(0.0, Math.min(1.0, root.borderOpacity * 0.83))
        edgeHighlightColor: root.rimColor
        elevation: root.shadowEnabled ? 8 : 0
        shadowColor: Qt.rgba(0, 0, 0, root.shadowOpacity)
        hovered: root._hovered || root.pointerLift > 0
        pressed: root._pressed
        pointerPosition: Qt.point(root.pointerPosition.x, root.pointerPosition.y)
        reduceMotion: root.reduceMotion
    }
}
