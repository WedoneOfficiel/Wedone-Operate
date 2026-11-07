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
    property bool enabled: true
    property real materialOpacity: 0.96
    property color fillColor: palette.accent || "#287FBE"
    property color hoverColor: palette.accentHover || fillColor
    property color tint: variant === "accent" ? Qt.rgba(fillColor.r, fillColor.g, fillColor.b, 0.68)
                        : variant === "danger" ? Qt.rgba((palette.danger || "#B73550").r, (palette.danger || "#B73550").g, (palette.danger || "#B73550").b, 0.72)
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
        elevation: root.shadowEnabled ? (root.hovered ? 13 : 8) : 0
        shadowColor: root.palette.shadow || "#33000000"
        hovered: root.hovered
        pressed: root.pressed
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
