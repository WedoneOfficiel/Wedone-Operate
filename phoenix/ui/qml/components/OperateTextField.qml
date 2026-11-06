import QtQuick
import QtQuick.Controls

TextField {
    id: field
    property var palette: ({})
    property int fieldRadius: 10
    implicitHeight: 42
    leftPadding: 13
    rightPadding: 13
    font.family: "DM Sans"
    font.pixelSize: 13
    color: palette.text || "#172536"
    placeholderTextColor: palette.muted || "#718096"
    selectionColor: palette.accent || "#167CC2"
    selectedTextColor: "#FFFFFF"

    background: Rectangle {
        radius: field.fieldRadius
        color: field.enabled ? (field.palette.surface || "#FFFFFF") : (field.palette.surfaceAlt || "#F7FAFD")
        border.width: field.activeFocus ? 1.5 : 1
        border.color: field.activeFocus ? (field.palette.accent || "#167CC2") : (field.palette.border || "#E1E8F0")
    }
}
