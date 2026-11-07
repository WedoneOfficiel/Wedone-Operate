import QtQuick
import QtQuick.Controls

Button {
    id: control
    property string kind: "primary" // primary, secondary, quiet, danger
    property var palette: ({})
    property int controlRadius: 12
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
        color: !control.enabled ? (control.palette.muted || "#718096")
             : control.kind === "danger" ? "#FFFFFF"
             : control.kind === "primary" ? (control.palette.onAccent || "#FFFFFF")
             : (control.palette.text || "#172536")
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
