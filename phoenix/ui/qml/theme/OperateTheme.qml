pragma Singleton
import QtQuick

QtObject {
    readonly property color lightBackground: "#EAF0F7"
    readonly property color lightSurface: "#F8FBFF"
    readonly property color lightSurfaceAlt: "#E7EEF7"
    readonly property color lightBorder: "#B9C9DA"
    readonly property color lightText: "#142438"
    readonly property color lightMuted: "#60748B"
    readonly property color lightBlue: "#176FC1"
    readonly property color lightBlueHover: "#0F5FA9"
    readonly property color lightBlueSoft: "#CFE5FA"
    readonly property color lightBlueInk: "#104E83"
    readonly property color darkBackground: "#091522"
    readonly property color darkSurface: "#142438"
    readonly property color darkSurfaceAlt: "#1C3048"
    readonly property color darkBorder: "#3C5874"
    readonly property color darkText: "#F1F7FF"
    readonly property color darkMuted: "#A5B8CB"
    readonly property color darkBlue: "#79C4FF"
    readonly property color darkBlueHover: "#A0D7FF"
    readonly property color darkBlueSoft: "#1A4264"
    readonly property color darkBlueInk: "#E1F3FF"

    function palette(dark, highContrast) {
        if (dark) {
            return {
                background: highContrast ? "#050B12" : darkBackground,
                surface: highContrast ? "#101D2B" : darkSurface,
                surfaceAlt: darkSurfaceAlt,
                panel: "#D91B3048", input: "#D91B3048",
                border: highContrast ? "#A0B9D1" : darkBorder,
                glassBorder: "#55FFFFFF",
                text: highContrast ? "#FFFFFF" : darkText,
                muted: highContrast ? "#D9E8F6" : darkMuted,
                accent: darkBlue, accentHover: darkBlueHover,
                accentSoft: darkBlueSoft, onAccent: "#071522",
                accentInk: darkBlueInk,
                success: "#56D6A5", warning: "#F4C56E", danger: "#FF91A3",
                shadow: "#B0000812",
                glassTop: "#55FFFFFF", glassBottom: "#B8101F30",
                glassHighlight: "#BFFFFFFF", glassEdge: "#E6FFFFFF"
            }
        }
        return {
            background: highContrast ? "#FFFFFF" : lightBackground,
            surface: "#F9FCFF", surfaceAlt: lightSurfaceAlt,
            panel: "#DDFBFDFF", input: "#E8FFFFFF",
            border: highContrast ? "#60758A" : lightBorder,
            glassBorder: "#BFFFFFFF",
            text: highContrast ? "#071522" : lightText,
            muted: highContrast ? "#344B62" : lightMuted,
            accent: lightBlue, accentHover: lightBlueHover,
            accentSoft: lightBlueSoft, onAccent: "#FFFFFF",
            accentInk: lightBlueInk,
            success: "#13845D", warning: "#A66A0B", danger: "#B52D4B",
            shadow: "#32112B48",
            glassTop: "#F8FFFFFF", glassBottom: "#B9DCE9F7",
            glassHighlight: "#FFFFFFFF", glassEdge: "#FFFFFFFF"
        }
    }
}
