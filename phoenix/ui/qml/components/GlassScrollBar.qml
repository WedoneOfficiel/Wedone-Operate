import QtQuick
import QtQuick.Controls

ScrollBar {
    id: bar
    property var palette: ({})
    implicitWidth: orientation === Qt.Vertical ? 9 : 0
    implicitHeight: orientation === Qt.Horizontal ? 9 : 0
    padding: 2
    minimumSize: 0.08
    background: Item {}
    contentItem: Rectangle {
        implicitWidth: bar.orientation === Qt.Vertical ? 5 : 24
        implicitHeight: bar.orientation === Qt.Horizontal ? 5 : 24
        radius: 4
        color: bar.pressed ? (bar.palette.accent || "#287FBE")
             : bar.hovered ? (bar.palette.accentHover || "#206DA8")
             : (bar.palette.muted || "#718096")
        opacity: bar.active || bar.pressed || bar.hovered ? 0.72 : 0.24
        Behavior on opacity { NumberAnimation { duration: 150 } }
    }
}
