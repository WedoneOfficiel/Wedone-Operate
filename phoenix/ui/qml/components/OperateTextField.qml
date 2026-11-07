import QtQuick
import QtQuick.Controls

TextField {
    id: field
    property var palette: ({})
    property int fieldRadius: 12
    implicitHeight: 44
    leftPadding: 14
    rightPadding: 14
    font.family: "DM Sans"
    font.pixelSize: 13
    color: enabled ? (palette.text || "#172536") : (palette.muted || "#718096")
    placeholderTextColor: palette.muted || "#718096"
    selectionColor: palette.accent || "#287FBE"
    selectedTextColor: "#FFFFFF"
    verticalAlignment: TextInput.AlignVCenter

    HoverHandler { id: hover; enabled: field.enabled }

    background: OperateMaterial {
        palette: field.palette
        cornerRadius: field.fieldRadius
        variant: "control"
        hovered: hover.hovered
        focused: field.activeFocus
        enabled: field.enabled
        materialOpacity: field.enabled ? 1.0 : 0.82
    }
}
