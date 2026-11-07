import QtQuick

Item {
    id: glass
    default property alias content: contentLayer.data

    property Item backdropItem
    property color tint: "#DDFBFDFF"
    property real cornerRadius: 18
    property real refraction: 4.0
    property real blurAmount: 1.0
    property real materialOpacity: 0.96
    property real borderOpacity: 0.72
    property bool reduceMotion: false
    property real pointerLift: 0
    readonly property bool shaderAvailable: platformEffects.shaderAvailable
    readonly property bool darkTint: tint.hsvValue < 0.5

    clip: true

    Behavior on pointerLift {
        enabled: !glass.reduceMotion
        NumberAnimation { duration: 220; easing.type: Easing.OutCubic }
    }

    ShaderEffectSource {
        id: backdropCapture
        anchors.fill: parent
        visible: false
        live: true
        recursive: false
        hideSource: false
        sourceItem: glass.backdropItem
        sourceRect: {
            if (!glass.backdropItem)
                return Qt.rect(0, 0, Math.max(1, glass.width), Math.max(1, glass.height))
            const origin = glass.mapToItem(glass.backdropItem, 0, 0)
            return Qt.rect(origin.x, origin.y, Math.max(1, glass.width), Math.max(1, glass.height))
        }
        textureSize: Qt.size(Math.max(1, Math.round(glass.width)), Math.max(1, Math.round(glass.height)))
    }

    ShaderEffect {
        anchors.fill: parent
        visible: glass.shaderAvailable && glass.backdropItem !== null
        property variant source: backdropCapture
        property vector2d texelSize: Qt.vector2d(1.0 / Math.max(1.0, width), 1.0 / Math.max(1.0, height))
        property vector2d itemSize: Qt.vector2d(Math.max(1.0, width), Math.max(1.0, height))
        property real radius: glass.cornerRadius
        property real refract: glass.refraction + glass.pointerLift * 1.4
        property real blur: glass.blurAmount
        property color glassTint: glass.tint
        property real opacityFactor: glass.materialOpacity
        fragmentShader: Qt.resolvedUrl("../shaders/glass.frag.qsb")
    }

    Rectangle {
        anchors.fill: parent
        visible: !glass.shaderAvailable || glass.backdropItem === null
        radius: glass.cornerRadius
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.lighter(glass.tint, 1.08) }
            GradientStop { position: 0.52; color: glass.tint }
            GradientStop { position: 1.0; color: Qt.darker(glass.tint, 1.06) }
        }
    }

    // Independent optical rim: no layout geometry is changed by the effect.
    Rectangle {
        anchors.fill: parent
        radius: glass.cornerRadius
        color: "transparent"
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, glass.borderOpacity)
        opacity: 0.92
    }

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 1.5
        height: Math.max(1, Math.min(2.2, glass.height * 0.035))
        radius: height / 2
        color: "#BFFFFFFF"
        opacity: glass.borderOpacity * 0.62
    }

    Item {
        id: contentLayer
        anchors.fill: parent
    }

    HoverHandler {
        enabled: !glass.reduceMotion
        onHoveredChanged: glass.pointerLift = hovered ? 1 : 0
    }
}
