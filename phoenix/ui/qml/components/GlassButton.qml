import QtQuick
import QtQuick.Controls

Button {
    id: control
    property string kind: "primary"
    property var palette: ({})
    property Item backgroundSource: null
    property int controlRadius: 13
    property color fillColor: palette.accent || "#167CC2"
    property color hoverColor: palette.accentHover || "#1168A5"
    property color textColor: kind === "primary" ? (palette.onAccent || "#FFFFFF")
                       : kind === "danger" ? "#FFFFFF" : (palette.text || "#172536")
    implicitHeight: 44
    leftPadding: 17
    rightPadding: 17
    topPadding: 9
    bottomPadding: 9
    font.family: "DM Sans"
    font.pixelSize: 13
    font.weight: Font.DemiBold
    contentItem: Text {
        text: control.text
        font: control.font
        color: !control.enabled ? (control.palette.muted || "#718096") : control.textColor
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: GlassSurface {
        backgroundSource: control.backgroundSource
        palette: control.palette
        cornerRadius: control.controlRadius
        variant: control.kind === "primary" ? "accent" : control.kind === "danger" ? "danger"
               : control.kind === "secondary" ? "glass" : "quiet"
        fillColor: control.kind === "danger" ? (control.palette.danger || "#B73550") : control.fillColor
        hoverColor: control.hoverColor
        hovered: control.hovered
        pressed: control.down
        focused: control.activeFocus
        enabled: control.enabled
        elevated: control.kind === "primary" || control.kind === "danger"
        materialOpacity: control.kind === "quiet" ? 0.94 : 1
    }
    onDownChanged: scale = down ? 0.985 : 1
    Behavior on scale { NumberAnimation { duration: 130; easing.type: Easing.OutCubic } }
}
