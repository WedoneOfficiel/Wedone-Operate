import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: panel
    property string title: ""
    property string subtitle: ""
    property var palette: ({})
    property int contentSpacing: 11
    default property alias content: body.data

    radius: 18
    color: palette.panel || palette.surface || "#FFFFFF"
    border.width: 1
    border.color: palette.border || "#E1E8F0"
    implicitWidth: 320
    implicitHeight: body.implicitHeight + 40

    ColumnLayout {
        id: body
        anchors.fill: parent
        anchors.margins: 20
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

    Behavior on color { ColorAnimation { duration: 140 } }
    Behavior on border.color { ColorAnimation { duration: 140 } }
}
