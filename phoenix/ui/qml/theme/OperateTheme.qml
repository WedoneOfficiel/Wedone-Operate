pragma Singleton
import QtQuick

QtObject {
    id: theme

    readonly property color lightBackground: "#F4F7FB"
    readonly property color lightSurface: "#FFFFFF"
    readonly property color lightSurfaceAlt: "#F7FAFD"
    readonly property color lightBorder: "#E1E8F0"
    readonly property color lightText: "#172536"
    readonly property color lightMuted: "#718096"
    readonly property color lightBlue: "#167CC2"
    readonly property color lightBlueHover: "#1168A5"
    readonly property color lightBlueSoft: "#E8F3FC"

    readonly property color darkBackground: "#111925"
    readonly property color darkSurface: "#1A2635"
    readonly property color darkSurfaceAlt: "#202F41"
    readonly property color darkBorder: "#304257"
    readonly property color darkText: "#F1F5FA"
    readonly property color darkMuted: "#A0AEC0"
    readonly property color darkBlue: "#55A9E5"
    readonly property color darkBlueHover: "#78BDED"
    readonly property color darkBlueSoft: "#203C55"

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
            success: "#16845D",
            warning: "#99600D",
            danger: "#B73550",
            shadow: "#180D2940"
        }
    }
}
