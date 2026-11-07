import QtQuick

OperateMaterial {
    id: card
    property int cardRadius: 20
    property bool interactive: false
    default property alias content: body.data

    cornerRadius: card.cardRadius
    variant: "glass"
    hovered: interactive && hoverHandler.hovered
    elevated: true
    materialOpacity: 0.98
    implicitWidth: body.childrenRect.width + 40
    implicitHeight: body.childrenRect.height + 40

    Item {
        id: body
        anchors.fill: parent
        anchors.margins: 20
    }
    HoverHandler { id: hoverHandler; enabled: card.interactive }
}
