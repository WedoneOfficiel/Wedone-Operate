import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: panel
    property string title: ""
    property string subtitle: ""
    property var palette: ({})
    default property alias content: body.data

    radius: 20
    color: palette.surface || "#FFFFFF"
    border.width: 1
    border.color: palette.border || "#E1E8F0"
    implicitWidth: 320
    implicitHeight: body.implicitHeight + 40

    ColumnLayout {
        id: body
        anchors.fill: parent
        anchors.margins: 20
        spacing: 12

        Label {
            visible: panel.title.length > 0
            text: panel.title
            color: panel.palette.text || "#172536"
            font.family: "Manrope"
            font.pixelSize: 18
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
