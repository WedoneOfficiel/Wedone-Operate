import QtQuick
import QtQuick.Effects

Rectangle {
    id: card
    property var palette: ({})
    property int cardRadius: 18
    property bool interactive: false
    property bool selected: false
    default property alias content: body.data
    implicitWidth: body.childrenRect.width + 36
    implicitHeight: body.childrenRect.height + 36
    radius: cardRadius
    layer.enabled: true
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowColor: card.palette.shadow || "#26000000"
        shadowBlur: card.interactive ? 0.42 : 0.28
        shadowOpacity: card.interactive ? 0.24 : 0.16
        shadowVerticalOffset: card.interactive ? 7 : 4
    }
    gradient: Gradient {
        GradientStop { position: 0.0; color: card.selected ? (card.palette.accentSoft || "#E8F3FC") : (card.palette.glassTop || "#F8FFFFFF") }
        GradientStop { position: 1.0; color: card.palette.glassBottom || (card.palette.panel || "#E8FFFFFF") }
    }
    color: selected ? (palette.accentSoft || "#E8F3FC")
         : (interactive && hoverHandler.hovered ? (palette.surfaceAlt || "#F7FAFD")
         : (palette.panel || palette.surface || "#FFFFFF"))
    border.width: selected ? 1.5 : (interactive && hoverHandler.hovered ? 1.3 : 1)
    border.color: selected ? (palette.accent || "#167CC2")
                : (interactive && hoverHandler.hovered ? (palette.borderHover || palette.border || "#B9C9DA")
                : (palette.border || "#E1E8F0"))

    Rectangle {
        anchors.fill: parent
        radius: card.radius
        color: "transparent"
        border.width: 1
        border.color: card.palette.glassHighlight || "#55FFFFFF"
        opacity: card.selected ? 0.8 : 0.48
    }

    Item {
        id: body
        anchors.fill: parent
        anchors.margins: 20
    }

    HoverHandler {
        id: hoverHandler
        enabled: card.interactive
    }

    Behavior on color { ColorAnimation { duration: 130 } }
    Behavior on border.color { ColorAnimation { duration: 130 } }
    Behavior on border.width { NumberAnimation { duration: 100 } }
}
