import QtQuick
import QtQuick.Controls

Button {
    id: control
    property string kind: "primary" // primary, secondary, quiet, danger
    property var palette: ({})
    property int controlRadius: 11
    implicitHeight: 42
    leftPadding: 17
    rightPadding: 17
    font.family: "DM Sans"
    font.pixelSize: 13
    font.weight: Font.DemiBold

    contentItem: Text {
        text: control.text
        font: control.font
        color: {
            if (!control.enabled) return control.palette.muted || "#718096"
            if (control.kind === "primary") return control.palette.onAccent || "#FFFFFF"
            if (control.kind === "danger") return "#FFFFFF"
            return control.palette.text || "#172536"
        }
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        radius: control.controlRadius
        color: {
            if (!control.enabled) return control.palette.surfaceAlt || "#F7FAFD"
            if (control.kind === "primary") return control.down ? (control.palette.accentHover || "#1168A5") : (control.hovered ? (control.palette.accentHover || "#1168A5") : (control.palette.accent || "#167CC2"))
            if (control.kind === "danger") return control.down ? "#922B43" : (control.hovered ? "#C94560" : (control.palette.danger || "#B73550"))
            if (control.kind === "secondary") return control.down ? (control.palette.accentSoft || "#E8F3FC") : (control.hovered ? (control.palette.surfaceAlt || "#F7FAFD") : (control.palette.surface || "#FFFFFF"))
            return control.hovered ? (control.palette.surfaceAlt || "#F7FAFD") : "transparent"
        }
        border.width: control.kind === "secondary" ? 1 : 0
        border.color: control.palette.border || "#E1E8F0"
    }
}
