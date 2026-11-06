import QtQuick

Rectangle {
    id: card
    property var palette: ({})
    property int cardRadius: 16
    property bool interactive: false
    property bool selected: false
    default property alias content: body.data
    implicitWidth: body.childrenRect.width + 36
    implicitHeight: body.childrenRect.height + 36
    radius: cardRadius
    color: selected ? (palette.accentSoft || "#E8F3FC") : (interactive && mouse.containsMouse ? (palette.surfaceAlt || "#F7FAFD") : (palette.surface || "#FFFFFF"))
    border.width: selected ? 1.5 : 1
    border.color: selected ? (palette.accent || "#167CC2") : (palette.border || "#E1E8F0")

    Item {
        id: body
        anchors.fill: parent
        anchors.margins: 18
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: card.interactive
        enabled: card.interactive
        z: -1
    }

    Behavior on color { ColorAnimation { duration: 130 } }
    Behavior on border.color { ColorAnimation { duration: 130 } }
}
