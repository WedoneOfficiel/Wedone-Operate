import QtQuick
import QtQuick.Controls

TextField {
    id: field
    property var palette: ({})
    property int fieldRadius: 10
    implicitHeight: 44
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
        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: !field.enabled ? (field.palette.surfaceAlt || "#F7FAFD")
                     : field.activeFocus ? (field.palette.glassTop || "#FFFFFF")
                     : hover.hovered ? (field.palette.glassTop || "#FFFFFF")
                     : (field.palette.surface || "#FFFFFF")
            }
            GradientStop {
                position: 1.0
                color: field.activeFocus ? (field.palette.accentSoft || "#E8F3FC")
                     : !field.enabled ? (field.palette.surfaceAlt || "#F7FAFD")
                     : (field.palette.surface || "#FFFFFF")
            }
        }
        border.width: field.activeFocus ? 1.7 : hover.hovered ? 1.2 : 1
        border.color: field.activeFocus ? (field.palette.accent || "#167CC2")
                    : (field.palette.border || "#E1E8F0")
        Rectangle {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 1
            height: 1
            radius: 1
            color: field.palette.glassHighlight || "#55FFFFFF"
            opacity: field.enabled ? 0.7 : 0.25
        }
        Behavior on border.color { ColorAnimation { duration: 120 } }
        Behavior on border.width { NumberAnimation { duration: 100 } }
    }
}
