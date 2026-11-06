import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: heading
    property string title: ""
    property string subtitle: ""
    property var palette: ({})
    spacing: subtitle.length > 0 ? 5 : 0

    Label {
        text: heading.title
        color: heading.palette.text || "#172536"
        font.family: "Manrope"
        font.pixelSize: 23
        font.weight: Font.Bold
        Layout.fillWidth: true
        wrapMode: Text.WordWrap
    }
    Label {
        visible: heading.subtitle.length > 0
        text: heading.subtitle
        color: heading.palette.muted || "#718096"
        font.family: "DM Sans"
        font.pixelSize: 13
        Layout.fillWidth: true
        wrapMode: Text.WordWrap
    }
}
