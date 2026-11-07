import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

GlassSurface {
    property Item backdropItem: null
    backgroundSource: backdropItem
    id: panel
    property string title: ""
    property string subtitle: ""
    property int contentSpacing: 12
    default property alias content: body.data

    cornerRadius: 20
    variant: "glass"
    elevated: true
    materialOpacity: 0.99
    implicitWidth: 320
    implicitHeight: body.implicitHeight + 44

    ColumnLayout {
        id: body
        anchors.fill: parent
        anchors.margins: 22
        spacing: panel.contentSpacing

        Label {
            visible: panel.title.length > 0
            text: panel.title
            color: panel.palette.text || "#172536"
            font.family: "Manrope"
            font.pixelSize: 17
            font.weight: Font.Bold
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
        }
        Label {
            visible: panel.subtitle.length > 0
            text: panel.subtitle
            color: panel.palette.muted || "#718096"
            font.family: "DM Sans"
            font.pixelSize: 12
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
        }
    }
}
