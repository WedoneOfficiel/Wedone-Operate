pragma Singleton
import QtQuick

QtObject {
    id: theme

    readonly property color lightBackground: "#F1F5FA"
    readonly property color lightSurface: "#FFFFFF"
    readonly property color lightSurfaceAlt: "#F6F8FC"
    readonly property color lightBorder: "#DDE5EF"
    readonly property color lightText: "#172536"
    readonly property color lightMuted: "#718096"
    readonly property color lightBlue: "#287FBE"
    readonly property color lightBlueHover: "#206DA8"
    readonly property color lightBlueSoft: "#E8F2FA"
    readonly property color lightBlueInk: "#185F91"

    readonly property color darkBackground: "#101824"
    readonly property color darkSurface: "#182536"
    readonly property color darkSurfaceAlt: "#1E2D40"
    readonly property color darkBorder: "#2D4056"
    readonly property color darkText: "#F1F5FA"
    readonly property color darkMuted: "#A0AEC0"
    readonly property color darkBlue: "#66B4EA"
    readonly property color darkBlueHover: "#85C5F0"
    readonly property color darkBlueSoft: "#203B55"
    readonly property color darkBlueInk: "#C3E6FF"

    function palette(dark, highContrast) {
        if (dark) {
            return {
                background: highContrast ? "#080D14" : darkBackground,
                surface: highContrast ? "#111B29" : darkSurface,
                surfaceAlt: darkSurfaceAlt,
                border: highContrast ? "#718096" : darkBorder,
                text: highContrast ? "#FFFFFF" : darkText,
                muted: highContrast ? "#D5DFEA" : darkMuted,
                accent: darkBlue,
                accentHover: darkBlueHover,
                accentSoft: darkBlueSoft,
                onAccent: "#071522",
                accentInk: darkBlueInk,
                success: "#4CC99A",
                warning: "#F0BF69",
                danger: "#F08A9A",
                shadow: "#55000000"
            }
        }
        return {
            background: highContrast ? "#FFFFFF" : lightBackground,
            surface: "#FFFFFF",
            surfaceAlt: lightSurfaceAlt,
            border: highContrast ? "#526477" : lightBorder,
            text: highContrast ? "#071522" : lightText,
            muted: highContrast ? "#40546A" : lightMuted,
            accent: lightBlue,
            accentHover: lightBlueHover,
            accentSoft: lightBlueSoft,
            onAccent: "#FFFFFF",
            accentInk: lightBlueInk,
            success: "#16845D",
            warning: "#99600D",
            danger: "#B73550",
            shadow: "#180D2940"
        }
    }
}
