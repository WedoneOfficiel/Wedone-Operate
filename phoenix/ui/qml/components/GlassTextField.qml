import QtQuick
import QtQuick.Controls

TextField {
    id: field
    property var palette: ({})
    property Item backgroundSource: null
    property int fieldRadius: 13
    implicitHeight: 46
    leftPadding: 15
    rightPadding: 15
    font.family: "DM Sans"
    font.pixelSize: 13
    color: enabled ? (palette.text || "#172536") : (palette.muted || "#718096")
    placeholderTextColor: palette.muted || "#718096"
    selectionColor: palette.accent || "#287FBE"
    selectedTextColor: "#FFFFFF"
    verticalAlignment: TextInput.AlignVCenter
    HoverHandler { id: hover; enabled: field.enabled }
    background: GlassSurface {
        backgroundSource: field.backgroundSource
        palette: field.palette
        cornerRadius: field.fieldRadius
        variant: "control"
        hovered: hover.hovered
        focused: field.activeFocus
        enabled: field.enabled
        materialOpacity: field.enabled ? 0.98 : 0.75
    }
}
