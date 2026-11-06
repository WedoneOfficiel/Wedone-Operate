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
    color: selected ? (palette.accentSoft || "#E8F3FC")
         : (interactive && hoverHandler.hovered ? (palette.surfaceAlt || "#F7FAFD")
         : (palette.panel || palette.surface || "#FFFFFF"))
    border.width: selected ? 1.5 : (interactive && hoverHandler.hovered ? 1.3 : 1)
    border.color: selected ? (palette.accent || "#167CC2")
                : (interactive && hoverHandler.hovered ? (palette.borderHover || palette.border || "#B9C9DA")
                : (palette.border || "#E1E8F0"))

    Item {
        id: body
        anchors.fill: parent
        anchors.margins: 18
    }

    HoverHandler {
        id: hoverHandler
        enabled: card.interactive
    }

    Behavior on color { ColorAnimation { duration: 130 } }
    Behavior on border.color { ColorAnimation { duration: 130 } }
    Behavior on border.width { NumberAnimation { duration: 100 } }
}
