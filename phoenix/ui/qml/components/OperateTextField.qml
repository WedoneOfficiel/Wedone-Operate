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
    color: enabled ? (palette.text || "#172536") : (palette.muted || "#718096")
    placeholderTextColor: palette.muted || "#718096"
    selectionColor: palette.accent || "#167CC2"
    selectedTextColor: "#FFFFFF"

    HoverHandler {
        id: hover
        enabled: field.enabled
    }

    background: Rectangle {
        radius: field.fieldRadius
        color: !field.enabled ? (field.palette.surfaceAlt || "#F7FAFD")
             : hover.hovered ? (field.palette.surfaceAlt || "#F7FAFD")
             : (field.palette.surface || "#FFFFFF")
        border.width: field.activeFocus ? 1.6 : hover.hovered ? 1.2 : 1
        border.color: field.activeFocus ? (field.palette.accent || "#167CC2")
                    : (field.palette.border || "#E1E8F0")
        Behavior on color { ColorAnimation { duration: 120 } }
        Behavior on border.color { ColorAnimation { duration: 120 } }
        Behavior on border.width { NumberAnimation { duration: 100 } }
    }
}
