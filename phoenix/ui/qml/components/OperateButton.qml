import QtQuick
import QtQuick.Controls

Button {
    id: control
    property string kind: "primary" // primary, secondary, quiet, danger
    property var palette: ({})
    property int controlRadius: 12
    property color fillColor: palette.accent || "#167CC2"
    property color hoverColor: palette.accentHover || "#1168A5"
    property color textColor: kind === "primary" ? (palette.onAccent || "#FFFFFF")
                       : kind === "danger" ? "#FFFFFF"
                       : (palette.text || "#172536")
    implicitHeight: 42
    leftPadding: 16
    rightPadding: 16
    topPadding: 8
    bottomPadding: 8
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

    background: OperateMaterial {
        palette: control.palette
        cornerRadius: control.controlRadius
        variant: control.kind === "primary" ? "accent"
               : control.kind === "danger" ? "danger"
               : control.kind === "secondary" ? "glass" : "quiet"
        fillColor: control.kind === "danger" ? (control.palette.danger || "#B73550") : control.fillColor
        hoverColor: control.kind === "danger" ? Qt.lighter(control.palette.danger || "#B73550", 1.08) : control.hoverColor
        hovered: control.hovered
        pressed: control.down
        focused: control.activeFocus
        enabled: control.enabled
        elevated: control.kind === "primary" || control.kind === "danger"
        materialOpacity: control.kind === "quiet" ? 0.92 : 1.0
    }

    onDownChanged: scale = down ? 0.985 : 1.0
    Behavior on scale { NumberAnimation { duration: 110; easing.type: Easing.OutCubic } }
}
