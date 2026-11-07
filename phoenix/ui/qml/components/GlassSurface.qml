import QtQuick
import QtQuick.Effects
import "../liquidglass" as LiquidGlass

Item {
    id: root
    default property alias content: glass.content
    property Item backdropItem: null
    property Item backgroundSource: backdropItem
    property var palette: ({})
    property string variant: "surface"
    property real cornerRadius: 16
    property bool hovered: false
    property bool pressed: false
    property bool focused: false
    property bool selected: false
    property bool elevated: false
    property real materialOpacity: 0.96
    property color fillColor: palette.accent || "#287FBE"
    property color hoverColor: palette.accentHover || fillColor
    readonly property color dangerColor: palette.danger || "#B73550"
    property color tint: variant === "accent" ? Qt.rgba(fillColor.r, fillColor.g, fillColor.b, 0.68)
                        : variant === "danger" ? Qt.rgba(dangerColor.r, dangerColor.g, dangerColor.b, 0.72)
                        : variant === "quiet" ? Qt.rgba(1, 1, 1, hovered ? 0.12 : 0.035)
                        : variant === "control" ? (focused ? Qt.rgba(fillColor.r, fillColor.g, fillColor.b, 0.20) : Qt.rgba(1, 1, 1, 0.15))
                        : variant === "glass" ? Qt.rgba(1, 1, 1, 0.18)
                        : Qt.rgba(1, 1, 1, 0.12)
    property real refraction: variant === "quiet" ? 1.4 : variant === "control" ? 2.4 : 4.6
    property real blurAmount: variant === "quiet" ? 0.35 : variant === "control" ? 0.85 : 1.35
    property real borderOpacity: focused || selected ? 0.98 : hovered ? 0.82 : 0.56
    property color rimColor: "#EFFFFFFF"
    property bool shadowEnabled: elevated
    property real shadowOpacity: hovered ? 0.24 : 0.16
    property bool reduceMotion: false
    property point pointerPosition: Qt.point(width * 0.5, height * 0.28)
    HoverHandler {
        id: pointerTracker
        onPointChanged: if (hovered)
            root.pointerPosition = Qt.point(point.position.x, point.position.y)
    }
    TapHandler { id: pressTracker }

    implicitWidth: glass.implicitWidth
    implicitHeight: glass.implicitHeight
    opacity: enabled ? materialOpacity : 0.58

    LiquidGlass.LiquidGlassSurface {
        id: glass
        anchors.fill: parent
        backgroundSource: root.backgroundSource
        cornerRadius: root.cornerRadius
        blurRadius: Math.max(8, Math.min(64, root.blurAmount * 34))
        downsampleFactor: 0.7
        baseOpacity: root.variant === "quiet" ? 0.16 : root.variant === "accent" || root.variant === "danger" ? 0.30 : 0.25
        tintColor: root.variant === "danger" ? (root.palette.danger || "#B73550") : root.tint
        tintStrength: root.variant === "quiet" ? 0.16 : 0.34
        distortionStrength: Math.max(0.018, Math.min(0.18, root.refraction * 0.025))
        highlightIntensity: root.borderOpacity
        edgeFresnelPower: 2.1
        edgeHighlightColor: root.rimColor
        elevation: root.shadowEnabled ? (root.hovered || pointerTracker.hovered ? 13 : 8) : 0
        shadowColor: root.palette.shadow || "#33000000"
        shadowOpacity: root.shadowOpacity
        hovered: root.hovered || pointerTracker.hovered
        pressed: root.pressed || pressTracker.pressed
        pointerPosition: root.pointerPosition
        reduceMotion: root.reduceMotion

        Rectangle {
            anchors.fill: parent
            radius: root.cornerRadius
            color: "transparent"
            border.width: root.focused || root.selected ? 1.7 : 1
            border.color: root.focused || root.selected
                         ? (root.palette.accent || "#287FBE")
                         : Qt.rgba(1, 1, 1, root.borderOpacity * 0.64)
        }
        Rectangle {
            anchors.fill: parent
            radius: root.cornerRadius
            color: root.variant === "accent" ? Qt.rgba(root.fillColor.r, root.fillColor.g, root.fillColor.b, 0.48)
                 : root.variant === "danger" ? Qt.rgba(root.dangerColor.r, root.dangerColor.g, root.dangerColor.b, 0.48)
                 : root.variant === "control" ? Qt.rgba(1, 1, 1, root.focused ? 0.18 : 0.10)
                 : root.variant === "quiet" ? Qt.rgba(1, 1, 1, root.hovered ? 0.14 : 0.025)
                 : Qt.rgba(1, 1, 1, 0.075)
        }
        Rectangle {
            anchors.fill: parent
            anchors.margins: 1
            radius: Math.max(0, root.cornerRadius - 1)
            gradient: Gradient {
                GradientStop { position: 0; color: Qt.rgba(1, 1, 1, root.hovered ? 0.27 : 0.18) }
                GradientStop { position: 0.22; color: "transparent" }
                GradientStop { position: 1; color: Qt.rgba(0.12, 0.20, 0.32, root.pressed ? 0.14 : 0.045) }
            }
        }
    }
}
