import QtQuick
import QtQuick.Effects

Rectangle {
    id: root
    property var palette: ({})
    property string variant: "surface"
    property real cornerRadius: 14
    property bool hovered: false
    property bool pressed: false
    property bool focused: false
    property bool selected: false
    property bool elevated: false
    property real materialOpacity: 1.0
    property color fillColor: palette.accent || "#287FBE"
    property color hoverColor: palette.accentHover || fillColor

    readonly property color _accent: fillColor
    readonly property color _surface: palette.surface || "#FFFFFF"
    readonly property color _surfaceAlt: palette.surfaceAlt || "#F6F8FC"
    readonly property color _border: palette.border || "#DDE5EF"

    readonly property color topColor: {
        if (!enabled) return _surfaceAlt
        if (variant === "accent") return Qt.lighter(pressed || hovered ? hoverColor : fillColor, 1.10)
        if (variant === "danger") return Qt.lighter(palette.danger || "#B73550", pressed ? 1.0 : 1.08)
        if (variant === "quiet") return hovered || pressed ? _surfaceAlt : "transparent"
        if (variant === "glass") return palette.glassTop || "#EFFFFFFF"
        if (variant === "control") return focused ? (palette.glassTop || _surface) : _surface
        return selected ? (palette.accentSoft || _surfaceAlt) : _surface
    }
    readonly property color bottomColor: {
        if (!enabled) return _surfaceAlt
        if (variant === "accent") return pressed ? hoverColor : fillColor
        if (variant === "danger") return pressed ? Qt.darker(palette.danger || "#B73550", 1.14) : (palette.danger || "#B73550")
        if (variant === "quiet") return hovered || pressed ? _surfaceAlt : "transparent"
        if (variant === "glass") return palette.glassBottom || "#DDF2F7FC"
        if (variant === "control") return focused ? (palette.accentSoft || _surfaceAlt) : (palette.panel || _surface)
        return selected ? (palette.accentSoft || _surfaceAlt) : (palette.panel || _surface)
    }

    radius: cornerRadius
    color: bottomColor
    opacity: enabled ? materialOpacity : 0.72
    gradient: Gradient {
        GradientStop { position: 0.0; color: root.topColor }
        GradientStop { position: 1.0; color: root.bottomColor }
    }
    border.width: focused ? 1.7 : selected ? 1.5 : (variant === "glass" || variant === "surface" || variant === "control" ? 1 : 0)
    border.color: focused || selected ? _accent
                : variant === "danger" ? Qt.darker(palette.danger || "#B73550", 1.12)
                : (palette.glassBorder || _border)

    layer.enabled: elevated
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowColor: root.palette.shadow || "#260D2940"
        shadowBlur: root.hovered ? 0.42 : 0.30
        shadowOpacity: root.hovered ? 0.22 : 0.14
        shadowVerticalOffset: root.hovered ? 7 : 4
    }
    Rectangle {
        anchors.fill: parent
        anchors.margins: 1
        radius: Math.max(0, parent.radius - 1)
        color: "transparent"
        border.width: 1
        border.color: root.palette.glassHighlight || "#55FFFFFF"
        opacity: root.enabled && (root.variant === "glass" || root.variant === "accent" || root.variant === "danger") ? 0.42 : 0
    }
    Behavior on border.color { ColorAnimation { duration: 130 } }
    Behavior on border.width { NumberAnimation { duration: 110 } }
    Behavior on opacity { NumberAnimation { duration: 120 } }
}
