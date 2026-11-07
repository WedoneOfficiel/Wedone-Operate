import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Effects
import "theme" as Theme
import "components" as Components

ApplicationWindow {
    id: root
    width: 1240
    height: 820
    minimumWidth: 980
    minimumHeight: 680
    visible: true
    title: "Wedone Operate"
    color: root.colors.bg

    property real uiScale: appBridge.uiScale
    property var progressSummary: JSON.parse(appBridge.progressJson)
    property string settingsReturnPage: "home"
    property string currentMode: appBridge.mode
    property string page: currentMode === "" ? "welcome" : currentMode === "individual" ? "practice" : "home"
    property string classroomArea: ""
    property string themeMode: appBridge.themeMode
    property bool darkTheme: themeMode === "dark" || (themeMode === "system" && appBridge.systemDark)
    property var colors: {
        var p = Theme.OperateTheme.palette(darkTheme, appBridge.highContrast)
        return {
            bg: p.background,
            surface: p.surface,
            panel: darkTheme ? "#D91B293A" : "#E8FFFFFF",
            input: p.surface,
            surfaceHover: p.surfaceAlt,
            border: p.border,
            borderHover: p.accent,
            text: p.text,
            muted: p.muted,
            textSecondary: p.muted,
            accent: p.accent,
            accentHover: p.accentHover,
            accentSoft: p.accentSoft,
            accentHoverSoft: p.accentSoft,
            accentInk: p.accentInk,
            onAccent: p.onAccent,
            glow: p.accentSoft,
            glowSecondary: p.surfaceAlt,
            shadow: p.shadow,
            glassTop: p.glassTop,
            glassBottom: p.glassBottom,
            glassHighlight: p.glassHighlight,
            success: p.success,
            warning: p.warning,
            dangerSurface: p.surfaceAlt,
            dangerHover: p.accentSoft,
            danger: p.danger
        }
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: root.darkTheme ? "#111D2C" : "#F8FBFF" }
            GradientStop { position: 0.52; color: root.colors.bg }
            GradientStop { position: 1.0; color: root.darkTheme ? "#0B1420" : "#EAF1F9" }
        }

        Rectangle {
            width: 500
            height: 500
            radius: 250
            x: parent.width - 250
            y: -220
            gradient: Gradient {
                GradientStop { position: 0.0; color: root.darkTheme ? "#554A9FE0" : "#668CCDF5" }
                GradientStop { position: 1.0; color: "transparent" }
            }
            opacity: 0.48
        }
        Rectangle {
            width: 360
            height: 360
            radius: 180
            x: -190
            y: parent.height - 210
            gradient: Gradient {
                GradientStop { position: 0.0; color: root.darkTheme ? "#333C7DB8" : "#5576A9D8" }
                GradientStop { position: 1.0; color: "transparent" }
            }
            opacity: 0.34
        }
    }

    header: ToolBar {
        implicitHeight: 78
        padding: 0
        background: Item {}
        Rectangle {
            anchors.horizontalCenter: parent.horizontalCenter
            y: 6
            width: parent.width - 36
            height: 66
            radius: 22
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: root.colors.shadow
                shadowBlur: 0.52
                shadowOpacity: 0.17
                shadowVerticalOffset: 6
            }
            gradient: Gradient {
                GradientStop { position: 0.0; color: root.colors.glassTop }
                GradientStop { position: 0.48; color: root.colors.panel }
                GradientStop { position: 1.0; color: root.darkTheme ? "#A91A293B" : "#DDFBFDFF" }
            }
            border.color: root.colors.glassHighlight
            border.width: 1
            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                anchors.topMargin: 1
                height: 1
                radius: 1
                color: root.darkTheme ? "#66FFFFFF" : "#DFFFFFFF"
            }
            RowLayout {
                anchors.centerIn: parent
                spacing: 9
                Image {
                    source: "image://branding/logo"
                    Layout.preferredWidth: 31
                    Layout.preferredHeight: 31
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    mipmap: true
                    sourceSize.width: 136
                    sourceSize.height: 136
                }
                ColumnLayout {
                    spacing: -2
                    AppLabel {
                        text: "wedone"
                        color: root.colors.text
                        font.family: "Manrope"
                        font.pixelSize: 17
                        font.weight: Font.ExtraBold
                    }
                    AppLabel {
                        text: "OPERATE"
                        color: root.colors.accent
                        font.family: "Manrope"
                        font.pixelSize: 9
                        font.weight: Font.Bold
                        font.letterSpacing: 1.25
                    }
                }
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                spacing: 9
                Item { Layout.fillWidth: true }
                Rectangle {
                    visible: root.currentMode !== ""
                    Layout.preferredWidth: modeLabel.implicitWidth + 27
                    Layout.preferredHeight: 36
                    radius: 18
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: root.colors.glassTop }
                        GradientStop { position: 1.0; color: root.colors.panel }
                    }
                    border.color: root.colors.glassHighlight
                    RowLayout {
                        anchors.centerIn: parent
                        spacing: 7
                        Rectangle {
                            Layout.preferredWidth: 7
                            Layout.preferredHeight: 7
                            radius: 4
                            color: root.colors.success
                        }
                        AppLabel {
                            id: modeLabel
                            text: root.currentMode === "individual" ? "Individuel" : "Classe"
                            color: root.colors.textSecondary
                            font.pixelSize: 11
                            font.weight: Font.DemiBold
                        }
                    }
                }
                ToolButton {
                    id: settingsButton
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 40
                    visible: root.page !== "welcome"
                    onClicked: {
                        root.settingsReturnPage = root.page
                        root.page = "settings"
                    }
                    background: Rectangle {
                        radius: 13
                        color: settingsButton.down ? root.colors.accentSoft : settingsButton.hovered ? root.colors.surfaceHover : "transparent"
                        border.color: settingsButton.hovered || settingsButton.activeFocus ? root.colors.border : "transparent"
                        border.width: 1
                        Behavior on color { ColorAnimation { duration: 130 } }
                    }
                    contentItem: AppLabel {
                        text: "⚙"
                        color: settingsButton.hovered ? root.colors.accent : root.colors.textSecondary
                        font.pixelSize: 20
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    ToolTip.visible: hovered
                    ToolTip.text: "Paramètres"
                }
            }
        }
    }

    Connections {
        target: appBridge
        function onModeChanged(mode) {
            root.currentMode = mode
            root.page = mode === "" ? "welcome" : mode === "individual" ? "practice" : "home"
            root.classroomArea = ""
        }
    }

    component AppLabel: Label {
        font.family: "DM Sans"
        font.pixelSize: 13
    }

    component AppText: Text {
        font.family: "DM Sans"
    }

    component AppTextField: Components.OperateTextField {
        palette: root.colors
        implicitHeight: 44
    }

    component AppComboBox: ComboBox {
        id: combo
        implicitHeight: 44
        font.family: "DM Sans"
        font.pixelSize: 13
        contentItem: AppText {
            leftPadding: 14
            rightPadding: 38
            text: combo.displayText
            font: combo.font
            color: combo.enabled ? root.colors.text : root.colors.muted
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
        indicator: AppText {
            x: combo.width - width - 14
            y: (combo.height - height) / 2
            text: "⌄"
            color: root.colors.muted
            font.pixelSize: 18
        }
        background: Rectangle {
            radius: 11
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: root.colors.shadow
                shadowBlur: combo.activeFocus ? 0.28 : 0.16
                shadowOpacity: combo.activeFocus ? 0.13 : 0.07
                shadowVerticalOffset: 2
            }
            gradient: Gradient {
                GradientStop { position: 0.0; color: !combo.enabled ? root.colors.surfaceHover : combo.activeFocus ? root.colors.glassTop : root.colors.input }
                GradientStop { position: 1.0; color: combo.hovered ? root.colors.surfaceHover : root.colors.panel }
            }
            border.width: combo.activeFocus ? 1.6 : 1
            border.color: combo.activeFocus ? root.colors.accent : root.colors.border
            Rectangle {
                anchors.fill: parent
                anchors.margins: 1
                radius: parent.radius - 1
                color: "transparent"
                border.width: 1
                border.color: root.colors.glassHighlight
                opacity: 0.45
            }
            Behavior on border.color { ColorAnimation { duration: 140 } }
        }
        delegate: ItemDelegate {
            required property int index
            width: combo.width
            height: 40
            highlighted: combo.highlightedIndex === index
            contentItem: AppText {
                text: combo.textAt(index)
                color: parent.highlighted ? root.colors.accentInk : root.colors.text
                font.family: "DM Sans"
                font.pixelSize: 13
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }
            background: Rectangle {
                radius: 8
                color: parent.highlighted ? root.colors.accentSoft : (parent.hovered ? root.colors.surfaceHover : "transparent")
                Behavior on color { ColorAnimation { duration: 100 } }
            }
        }
        popup: Popup {
            y: combo.height + 5
            width: combo.width
            implicitHeight: Math.min(contentItem.implicitHeight + 12, 260)
            padding: 6
            background: Rectangle {
                radius: 13
                layer.enabled: true
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: root.colors.shadow
                    shadowBlur: 0.48
                    shadowOpacity: 0.22
                    shadowVerticalOffset: 8
                }
                gradient: Gradient {
                    GradientStop { position: 0.0; color: root.colors.glassTop }
                    GradientStop { position: 1.0; color: root.colors.surface }
                }
                border.color: root.colors.border
                border.width: 1
                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 1
                    radius: parent.radius - 1
                    color: "transparent"
                    border.width: 1
                    border.color: root.colors.glassHighlight
                    opacity: 0.5
                }
            }
            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: combo.popup.visible ? combo.delegateModel : null
                currentIndex: combo.highlightedIndex
                ScrollIndicator.vertical: ScrollIndicator {}
            }
        }
    }

    component AppSpinBox: SpinBox {
        id: numberField
        implicitHeight: 44
        font.family: "DM Sans"
        font.pixelSize: 13
        contentItem: TextInput {
            z: 2
            text: numberField.textFromValue(numberField.value, numberField.locale)
            font: numberField.font
            color: numberField.enabled ? root.colors.text : root.colors.muted
            selectionColor: root.colors.accent
            selectedTextColor: "#FFFFFF"
            horizontalAlignment: TextInput.AlignHCenter
            verticalAlignment: TextInput.AlignVCenter
            readOnly: !numberField.editable
            validator: numberField.validator
            inputMethodHints: Qt.ImhFormattedNumbersOnly
            onTextEdited: numberField.value = numberField.valueFromText(text, numberField.locale)
        }
        background: Rectangle {
            radius: 10
            color: numberField.enabled ? root.colors.input : root.colors.surfaceHover
            border.color: numberField.activeFocus ? root.colors.accent : root.colors.border
            border.width: numberField.activeFocus ? 1.6 : 1
            Behavior on color { ColorAnimation { duration: 120 } }
            Behavior on border.color { ColorAnimation { duration: 120 } }
        }
        up.indicator: Rectangle {
            x: numberField.width - width
            width: 32
            height: numberField.height / 2
            color: numberField.up.pressed ? root.colors.accentSoft : (numberField.up.hovered ? root.colors.surfaceHover : "transparent")
            radius: 6
            AppText { anchors.centerIn: parent; text: "+"; color: root.colors.text; font.pixelSize: 15 }
        }
        down.indicator: Rectangle {
            x: numberField.width - width
            y: numberField.height / 2
            width: 32
            height: numberField.height / 2
            color: numberField.down.pressed ? root.colors.accentSoft : (numberField.down.hovered ? root.colors.surfaceHover : "transparent")
            radius: 6
            AppText { anchors.centerIn: parent; text: "−"; color: root.colors.text; font.pixelSize: 15 }
        }
    }

    component AppCheckBox: CheckBox {
        id: check
        spacing: 10
        implicitHeight: 40
        contentItem: AppText {
            text: check.text
            font.family: "DM Sans"
            font.pixelSize: 13
            color: root.colors.textSecondary
            verticalAlignment: Text.AlignVCenter
            leftPadding: check.indicator.width + check.spacing
        }
        indicator: Rectangle {
            implicitWidth: 20
            implicitHeight: 20
            x: 0
            y: (check.height - height) / 2
            radius: 5
            color: check.checked ? root.colors.accent : (check.enabled ? root.colors.input : root.colors.surfaceHover)
            border.color: check.activeFocus ? root.colors.accent : (check.checked ? root.colors.accent : root.colors.border)
            border.width: check.activeFocus ? 1.6 : 1
            AppText { anchors.centerIn: parent; text: check.checked ? "✓" : ""; color: "#FFFFFF"; font.pixelSize: 12; font.weight: Font.Bold }
            Behavior on color { ColorAnimation { duration: 110 } }
        }
    }

    component AppSlider: Slider {
        id: slider
        background: Rectangle {
            x: slider.leftPadding
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: slider.availableWidth
            height: 6
            radius: 3
            color: root.colors.border
            Behavior on color { ColorAnimation { duration: 120 } }
            Rectangle {
                width: slider.visualPosition * parent.width
                height: parent.height
                radius: 3
                color: root.colors.accent
            }
        }
        handle: Rectangle {
            x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: 19
            height: 19
            radius: 10
            color: slider.enabled ? root.colors.surface : root.colors.surfaceHover
            border.color: slider.activeFocus ? root.colors.accent : root.colors.accent
            border.width: slider.activeFocus ? 3 : slider.hovered ? 2.5 : 2
            Behavior on border.width { NumberAnimation { duration: 100 } }
        }
    }

    component QuietButton: Button {
        id: quiet
        implicitHeight: 42
        font.family: "DM Sans"
        font.pixelSize: 13
        contentItem: AppText {
            text: quiet.text
            color: quiet.enabled ? root.colors.textSecondary : root.colors.muted
            font.family: "DM Sans"
            font.pixelSize: 13
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        background: Rectangle {
            radius: 10
            color: !quiet.enabled ? "transparent" : quiet.down ? root.colors.accentSoft : (quiet.hovered ? root.colors.surfaceHover : "transparent")
            border.color: quiet.hovered || quiet.activeFocus ? root.colors.border : "transparent"
            border.width: quiet.hovered || quiet.activeFocus ? 1 : 0
            Behavior on color { ColorAnimation { duration: 110 } }
        }
    }

    component PrimaryButton: Components.OperateButton {
        palette: root.colors
    }

    component NavButton: Button {
        id: navControl
        property bool active: false
        property string symbol: "•"
        implicitHeight: 45
        leftPadding: 12
        rightPadding: 12
        contentItem: RowLayout {
            spacing: 12
            AppText {
                Layout.preferredWidth: 19
                text: navControl.symbol
                color: navControl.active ? root.colors.accent : (navControl.hovered ? root.colors.text : root.colors.muted)
                font.pixelSize: 15
                font.weight: navControl.active ? Font.Bold : Font.Medium
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            AppText {
                Layout.fillWidth: true
                text: navControl.text
                color: navControl.active ? root.colors.accentInk : (navControl.hovered ? root.colors.text : root.colors.muted)
                font.family: "DM Sans"
                font.pixelSize: 13
                font.weight: navControl.active ? Font.Bold : Font.Medium
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }
            Rectangle {
                visible: navControl.active
                Layout.preferredWidth: 5
                Layout.preferredHeight: 5
                radius: 3
                color: root.colors.accent
            }
        }
        background: Rectangle {
            radius: 12
            layer.enabled: navControl.active || navControl.hovered
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: root.colors.shadow
                shadowBlur: navControl.active ? 0.30 : 0.18
                shadowOpacity: navControl.active ? 0.15 : 0.08
                shadowVerticalOffset: navControl.active ? 3 : 1
            }
            gradient: Gradient {
                GradientStop { position: 0.0; color: navControl.active ? root.colors.glassTop : navControl.down ? root.colors.accentSoft : navControl.hovered ? root.colors.glassTop : "transparent" }
                GradientStop { position: 1.0; color: navControl.active ? root.colors.accentSoft : navControl.down ? root.colors.accentSoft : navControl.hovered ? root.colors.surfaceHover : "transparent" }
            }
            border.width: navControl.active ? 1.2 : navControl.hovered || navControl.activeFocus ? 1 : 0
            border.color: navControl.active ? root.colors.accent : navControl.hovered || navControl.activeFocus ? root.colors.glassHighlight : "transparent"
            Rectangle {
                anchors.fill: parent
                anchors.margins: 1
                radius: parent.radius - 1
                color: "transparent"
                border.width: navControl.active ? 1 : 0
                border.color: root.colors.glassHighlight
                opacity: 0.55
            }
            Behavior on border.color { ColorAnimation { duration: 140 } }
        }
    }

    component ModeCard: Rectangle {
        id: card
        property string heading
        property string subtitle
        property string symbol
        property string actionMode
        signal chosen(string mode)
        radius: 18
        layer.enabled: true
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: root.colors.shadow
            shadowBlur: hover.hovered ? 0.42 : 0.28
            shadowOpacity: hover.hovered ? 0.22 : 0.13
            shadowVerticalOffset: hover.hovered ? 7 : 4
        }
        gradient: Gradient {
            GradientStop { position: 0.0; color: root.colors.glassTop }
            GradientStop { position: 1.0; color: hover.hovered ? root.colors.surfaceHover : root.colors.surface }
        }
        color: hover.hovered ? root.colors.surfaceHover : root.colors.surface
        border.width: hover.hovered ? 1.5 : 1
        border.color: hover.hovered ? root.colors.accent : root.colors.border
        implicitWidth: 320
        implicitHeight: 260
        Behavior on color { ColorAnimation { duration: 140 } }
        Behavior on border.color { ColorAnimation { duration: 140 } }
        Behavior on border.width { NumberAnimation { duration: 110 } }

        HoverHandler { id: hover }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 11
            Rectangle {
                width: 54
                height: 54
                radius: 15
                color: root.colors.accentSoft
                AppText {
                    anchors.centerIn: parent
                    text: card.symbol
                    color: root.colors.accent
                    font.pixelSize: 25
                    font.weight: Font.DemiBold
                }
            }
            AppLabel {
                text: card.heading
                color: root.colors.text
                font.pixelSize: 22
                font.weight: Font.DemiBold
            }
            AppLabel {
                text: card.subtitle
                color: root.colors.muted
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
            Item { Layout.fillHeight: true }
            PrimaryButton {
                text: "Continuer"
                Layout.fillWidth: true
                onClicked: card.chosen(card.actionMode)
            }
        }
    }

    StackLayout {
        x: 30 / root.uiScale
        y: 14 / root.uiScale
        width: (parent.width - 60) / root.uiScale
        height: (parent.height - 28) / root.uiScale
        scale: root.uiScale
        transformOrigin: Item.TopLeft
        currentIndex: root.page === "welcome" ? 0 : root.page === "practice" ? 2 : root.page === "settings" ? 3 : 1

        Item {
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width, 760)
                spacing: 22

                AppLabel {
                    text: "Bienvenue."
                    color: root.colors.text
                    font.pixelSize: 38
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignHCenter
                }
                AppLabel {
                    text: "Comment souhaitez-vous utiliser Wedone Operate ?"
                    color: root.colors.muted
                    font.pixelSize: 17
                    Layout.alignment: Qt.AlignHCenter
                }
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 18
                    spacing: 18
                    ModeCard {
                        heading: "Utilisation individuelle"
                        subtitle: "Accédez directement à votre espace de pratique."
                        symbol: "↗"
                        actionMode: "individual"
                        onChosen: function(mode) { appBridge.chooseMode(mode) }
                    }
                    ModeCard {
                        heading: "Utilisation en classe"
                        subtitle: "Un espace dédié aux élèves et un autre aux professeurs."
                        symbol: "▦"
                        actionMode: "classroom"
                        onChosen: function(mode) { appBridge.chooseMode(mode) }
                    }
                }
            }
        }

        Item {
            ScrollView {
                anchors.fill: parent
                clip: true
                contentWidth: availableWidth

                ColumnLayout {
                    width: Math.min(parent.width, 1240)
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 18
                    spacing: 18

                AppLabel {
                    text: root.currentMode === "individual" ? "Votre espace de pratique" : "Espace classe"
                    color: root.colors.text
                    font.pixelSize: 36
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignLeft
                    font.family: "Manrope"
                }

                AppLabel {
                    text: root.currentMode === "individual"
                          ? "Retrouvez vos statistiques et lancez une nouvelle séance."
                          : "Accédez aux espaces élèves et professeurs pour organiser le travail de la classe."
                    color: root.colors.muted
                    font.pixelSize: 14
                    Layout.alignment: Qt.AlignLeft
                    Layout.bottomMargin: 2
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                }

                RowLayout {
                    visible: root.page === "home"
                    Layout.fillWidth: true
                    Layout.topMargin: -3
                    QuietButton {
                        text: "⇄  Changer de mode"
                        onClicked: appBridge.returnToModeChoice()
                    }
                    Item { Layout.fillWidth: true }
                }

                RowLayout {
                    visible: root.currentMode === "individual"
                    Layout.fillWidth: true
                    spacing: 14
                    Repeater {
                        model: [
                            { label: "Séances", value: root.progressSummary.sessions },
                            { label: "Réponses", value: root.progressSummary.answered },
                            { label: "Réussite", value: root.progressSummary.accuracy === null ? "—" : root.progressSummary.accuracy + "%" }
                        ]
                        delegate: Components.SurfaceCard {
                            required property var modelData
                            palette: root.colors
                            interactive: true
                            Layout.fillWidth: true
                            Layout.preferredHeight: 132
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.leftMargin: 21
                                anchors.rightMargin: 20
                                anchors.topMargin: 17
                                anchors.bottomMargin: 17
                                spacing: 0
                                RowLayout {
                                    Layout.fillWidth: true
                                    AppLabel {
                                        text: modelData.label.toUpperCase()
                                        color: root.colors.muted
                                        font.pixelSize: 10
                                        font.weight: Font.Bold
                                        font.letterSpacing: 1.0
                                        Layout.fillWidth: true
                                    }
                                    Rectangle {
                                        Layout.preferredWidth: 27
                                        Layout.preferredHeight: 27
                                        radius: 9
                                        color: root.colors.accentSoft
                                        AppLabel {
                                            anchors.centerIn: parent
                                            text: modelData.label === "Séances" ? "◷" : modelData.label === "Réponses" ? "✓" : "↗"
                                            color: root.colors.accent
                                            font.pixelSize: 15
                                            font.weight: Font.Bold
                                        }
                                    }
                                }
                                Item { Layout.fillHeight: true }
                                AppLabel {
                                    text: modelData.value
                                    color: root.colors.text
                                    font.pixelSize: 31
                                    font.weight: Font.Bold
                                    Layout.alignment: Qt.AlignLeft
                                    font.family: "Manrope"
                                }
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 3
                                    radius: 2
                                    color: root.colors.border
                                    Rectangle {
                                        width: parent.width * (modelData.label === "Réussite" && root.progressSummary.accuracy !== null ? root.progressSummary.accuracy / 100 : modelData.label === "Réponses" ? Math.min(1, root.progressSummary.answered / 100) : Math.min(1, root.progressSummary.sessions / 20))
                                        height: parent.height
                                        radius: 2
                                        color: root.colors.accent
                                    }
                                }
                            }
                        }
                    }
                }

                PrimaryButton {
                    visible: root.currentMode === "individual"
                    text: "Commencer une séance"
                    Layout.alignment: Qt.AlignLeft
                    Layout.topMargin: 2
                    width: 280
                    onClicked: root.page = "practice"
                }

                GridLayout {
                    visible: root.currentMode === "classroom"
                    Layout.fillWidth: true
                    columns: root.width >= 1050 ? 2 : 1
                    columnSpacing: 18
                    rowSpacing: 18
                    Repeater {
                        model: [
                            { title: "Espace élève", detail: "Accéder à une classe et à un profil.", icon: "◎" },
                            { title: "Espace professeur", detail: "Gérer les classes et les entraînements.", icon: "▤" }
                        ]
                        delegate: Rectangle {
                            required property var modelData
                            Layout.fillWidth: true
                            Layout.preferredWidth: 300
                            Layout.minimumWidth: 0
                            height: 190
                            radius: 18
                            layer.enabled: true
                            layer.effect: MultiEffect {
                                shadowEnabled: true
                                shadowColor: root.colors.shadow
                                shadowBlur: hoverArea.hovered ? 0.38 : 0.24
                                shadowOpacity: hoverArea.hovered ? 0.20 : 0.12
                                shadowVerticalOffset: hoverArea.hovered ? 6 : 3
                            }
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: root.colors.glassTop }
                                GradientStop { position: 1.0; color: hoverArea.hovered ? root.colors.surfaceHover : root.colors.panel }
                            }
                            border.width: hoverArea.hovered ? 1.5 : 1
                            border.color: hoverArea.hovered ? root.colors.accent : root.colors.glassHighlight
                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: 1
                                radius: parent.radius - 1
                                color: "transparent"
                                border.width: 1
                                border.color: root.colors.border
                                opacity: 0.52
                            }
                            Behavior on border.color { ColorAnimation { duration: 130 } }
                            HoverHandler { id: hoverArea }
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 22
                                spacing: 10
                                AppLabel {
                                    text: modelData.icon
                                    color: root.colors.accent
                                    font.pixelSize: 26
                                }
                                AppLabel {
                                    text: modelData.title
                                    color: root.colors.text
                                    font.pixelSize: 20
                                    font.weight: Font.DemiBold
                                }
                                AppLabel {
                                    text: modelData.detail
                                    color: root.colors.muted
                                    font.pixelSize: 13
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                                Item { Layout.fillHeight: true }
                                PrimaryButton {
                                    text: "Ouvrir"
                                    Layout.fillWidth: true
                                    onClicked: {
                                        root.classroomArea = index === 0 ? "student" : "teacher"
                                        if (index === 0) appBridge.selectStudent("")
                                        root.page = "area"
                                    }
                                }
                            }
                        }
                    }
                }

                AppLabel {
                    visible: root.page === "area"
                    text: root.classroomArea === "student" ? "Espace élève" : "Espace professeur"
                    color: root.colors.text
                    font.pixelSize: 28
                    font.weight: Font.DemiBold
                    Layout.alignment: Qt.AlignLeft
                    font.family: "Manrope"
                }

                RowLayout {
                    visible: root.page === "area" && root.currentMode === "classroom"
                    Layout.fillWidth: true
                    spacing: 8
                    QuietButton {
                        text: "Vue d'ensemble"
                        onClicked: root.page = "home"
                    }
                    QuietButton {
                        text: "Espace élève"
                        onClicked: {
                            root.classroomArea = "student"
                            appBridge.selectStudent("")
                        }
                    }
                    QuietButton {
                        text: "Espace professeur"
                        onClicked: root.classroomArea = "teacher"
                    }
                    Item { Layout.fillWidth: true }
                }

                Components.FormPanel {
                    title: "Accéder à son espace élève"
                    subtitle: "Choisissez votre classe, votre groupe et votre profil pour retrouver vos exercices."
                    palette: root.colors
                    visible: root.page === "area" && root.classroomArea === "student"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignTop
                    AppLabel { text: "Classe"; color: root.colors.textSecondary; font.pixelSize: 14; font.weight: Font.DemiBold }
                    AppComboBox {
                        id: studentClassSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "name"
                        valueRole: "id"
                        model: JSON.parse(appBridge.allClassesJson)
                        onActivated: appBridge.selectStudent("")
                    }
                    AppLabel { text: "Groupe (facultatif)"; color: root.colors.textSecondary; font.pixelSize: 14; font.weight: Font.DemiBold }
                    AppComboBox {
                        id: studentGroupSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return [{ name: "Tous les groupes", id: "" }].concat(appBridge.groupsForClass(studentClassSelect.currentValue || "")) }
                        onActivated: appBridge.selectStudent("")
                    }
                    AppLabel { text: "Élève"; color: root.colors.textSecondary; font.pixelSize: 14; font.weight: Font.DemiBold }
                    AppComboBox {
                        id: studentProfileSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "display_name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return appBridge.studentsForClass(studentClassSelect.currentValue || "", studentGroupSelect.currentValue || "") }
                        onActivated: appBridge.selectStudent(currentValue)
                    }

                    Rectangle {
                        visible: !!studentProfileSelect.currentValue
                        Layout.fillWidth: true
                        implicitHeight: studentSummary.implicitHeight + 34
                        radius: 14
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: root.colors.glassTop }
                            GradientStop { position: 1.0; color: root.colors.surfaceHover }
                        }
                        border.color: root.colors.border
                        Rectangle {
                            width: 3
                            anchors.left: parent.left
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            radius: 2
                            color: root.colors.accent
                        }
                        ColumnLayout {
                            id: studentSummary
                            anchors.fill: parent
                            anchors.margins: 15
                            spacing: 12
                            RowLayout {
                                Layout.fillWidth: true
                                AppLabel {
                                    text: "VOTRE PROGRESSION"
                                    color: root.colors.text
                                    font.pixelSize: 10
                                    font.weight: Font.Bold
                                    font.letterSpacing: 1.1
                                    Layout.fillWidth: true
                                }
                                AppLabel {
                                    text: root.progressSummary.sessions > 0 ? "ACTIF" : "NOUVEAU"
                                    color: root.colors.accent
                                    font.pixelSize: 9
                                    font.weight: Font.Bold
                                }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                Repeater {
                                    model: [
                                        { label: "Séances", value: root.progressSummary.sessions },
                                        { label: "Réponses", value: root.progressSummary.answered },
                                        { label: "Réussite", value: root.progressSummary.accuracy === null ? "—" : root.progressSummary.accuracy + "%" }
                                    ]
                                    delegate: Rectangle {
                                        required property var modelData
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 62
                                        radius: 10
                                        color: root.colors.panel
                                        border.color: root.colors.glassHighlight
                                        ColumnLayout {
                                            anchors.fill: parent
                                            anchors.leftMargin: 10
                                            anchors.rightMargin: 6
                                            anchors.topMargin: 8
                                            anchors.bottomMargin: 7
                                            spacing: 2
                                            AppLabel {
                                                text: modelData.value
                                                color: root.colors.text
                                                font.pixelSize: 18
                                                font.weight: Font.Bold
                                                font.family: "Manrope"
                                            }
                                            AppLabel {
                                                text: modelData.label
                                                color: root.colors.muted
                                                font.pixelSize: 10
                                            }
                                        }
                                    }
                                }
                            }
                            AppLabel {
                                visible: root.progressSummary.sessions === 0
                                text: "Aucun résultat enregistré pour le moment. Lancez une première séance !"
                                color: root.colors.muted
                                font.pixelSize: 11
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                    }
                    AppLabel {
                        text: "Exercices proposés par le professeur"
                        color: root.colors.text
                        font.pixelSize: 14
                        font.weight: Font.DemiBold
                        visible: !!studentClassSelect.currentValue
                    }
                    AppComboBox {
                        id: studentPlanSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "name"
                        valueRole: "id"
                        visible: !!studentClassSelect.currentValue
                        model: { appBridge.classroomRevision; return appBridge.plansForClass(studentClassSelect.currentValue || "") }
                    }
                    PrimaryButton {
                        text: "Démarrer l'exercice assigné"
                        Layout.fillWidth: true
                        visible: !!studentPlanSelect.currentValue
                        enabled: !!studentProfileSelect.currentValue
                        onClicked: {
                            appBridge.selectStudent(studentProfileSelect.currentValue)
                            appBridge.startAssignedPractice(studentPlanSelect.currentValue)
                            root.page = "practice"
                        }
                    }
                    PrimaryButton {
                        text: "Continuer"
                        Layout.fillWidth: true
                        enabled: !!studentProfileSelect.currentValue
                        onClicked: {
                            appBridge.selectStudent(studentProfileSelect.currentValue)
                            root.page = "practice"
                        }
                    }
                    QuietButton {
                        text: "S'entraîner sans profil"
                        flat: true
                        Layout.alignment: Qt.AlignHCenter
                        onClicked: {
                            appBridge.selectStudent("")
                            root.page = "practice"
                        }
                    }
                }

                GridLayout {
                    visible: root.page === "area" && root.classroomArea === "teacher" && !appBridge.teacherAuthenticated
                    Layout.fillWidth: true
                    columns: root.width >= 1050 ? 2 : 1
                    columnSpacing: 16
                    rowSpacing: 16

                    Components.FormPanel {
                        title: "Se connecter"
                        subtitle: "Retrouvez votre espace et vos classes."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        AppLabel {
                            text: "PROFIL EXISTANT"
                            color: root.colors.accent
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            font.letterSpacing: 1.2
                        }
                        AppLabel {
                            text: "Sélectionnez votre profil professeur."
                            color: root.colors.textSecondary
                            font.pixelSize: 12
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                        AppComboBox {
                            id: teacherSelect
                            Layout.fillWidth: true
                            implicitHeight: 46
                            textRole: "display_name"
                            valueRole: "id"
                            model: JSON.parse(appBridge.teachersJson)
                        }
                        AppTextField {
                            id: teacherLoginPassword
                            Layout.fillWidth: true
                            implicitHeight: 46
                            placeholderText: "Mot de passe professeur"
                            echoMode: TextInput.Password
                            onAccepted: appBridge.loginTeacher(teacherSelect.currentValue || "", text)
                        }
                        PrimaryButton {
                            text: "Se connecter  →"
                            Layout.fillWidth: true
                            implicitHeight: 48
                            enabled: !!teacherSelect.currentValue
                            onClicked: appBridge.loginTeacher(teacherSelect.currentValue, teacherLoginPassword.text)
                        }
                        AppLabel {
                            visible: teacherSelect.count === 0
                            text: "Aucun profil n'existe encore. Créez votre premier compte à côté."
                            color: root.colors.muted
                            font.pixelSize: 11
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }

                    Components.FormPanel {
                        title: "Créer un profil"
                        subtitle: "Configurez votre accès professeur en quelques instants."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        AppLabel {
                            text: "NOUVEAU PROFIL"
                            color: root.colors.accent
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            font.letterSpacing: 1.2
                        }
                        AppLabel {
                            text: "Votre nom sera utilisé pour identifier votre espace."
                            color: root.colors.textSecondary
                            font.pixelSize: 12
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                        AppTextField {
                            id: newTeacherName
                            Layout.fillWidth: true
                            implicitHeight: 46
                            placeholderText: "Votre nom"
                        }
                        AppTextField {
                            id: newTeacherPassword
                            Layout.fillWidth: true
                            implicitHeight: 46
                            placeholderText: "Mot de passe (8 caractères minimum)"
                            echoMode: TextInput.Password
                            onAccepted: appBridge.createTeacher(newTeacherName.text, text)
                        }
                        AppLabel {
                            visible: newTeacherPassword.text.length > 0 && newTeacherPassword.text.length < 8
                            text: "Encore " + (8 - newTeacherPassword.text.length) + " caractère(s) minimum."
                            color: root.colors.warning
                            font.pixelSize: 11
                        }
                        AppLabel {
                            visible: newTeacherPassword.text.length >= 8
                            text: "Longueur du mot de passe suffisante."
                            color: root.colors.success
                            font.pixelSize: 11
                        }
                        PrimaryButton {
                            text: "Créer mon profil  →"
                            Layout.fillWidth: true
                            implicitHeight: 48
                            enabled: newTeacherName.text.trim().length > 0 && newTeacherPassword.text.length >= 8
                            onClicked: appBridge.createTeacher(newTeacherName.text, newTeacherPassword.text)
                        }
                    }
                }
                AppLabel {
                    visible: root.page === "area" && root.classroomArea === "teacher" && !appBridge.teacherAuthenticated && appBridge.classroomMessage !== ""
                    text: appBridge.classroomMessage
                    color: root.colors.warning
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }

                ColumnLayout {
                    visible: root.page === "area" && root.classroomArea === "teacher" && appBridge.teacherAuthenticated
                    Layout.fillWidth: true
                    spacing: 14

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 16
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            AppLabel {
                                text: "ESPACE ENSEIGNANT"
                                color: root.colors.accent
                                font.pixelSize: 10
                                font.weight: Font.Bold
                                font.letterSpacing: 1.5
                            }
                            AppLabel {
                                text: "Votre espace de gestion"
                                color: root.colors.text
                                font.family: "Manrope"
                                font.pixelSize: 25
                                font.weight: Font.Bold
                            }
                            AppLabel {
                                text: "Classes, élèves et entraînements réunis au même endroit."
                                color: root.colors.textSecondary
                                font.pixelSize: 13
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                        Rectangle {
                            Layout.preferredWidth: 118
                            Layout.preferredHeight: 38
                            radius: 19
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: root.colors.glassTop }
                                GradientStop { position: 1.0; color: root.colors.panel }
                            }
                            border.color: root.colors.glassHighlight
                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 7
                                Rectangle {
                                    Layout.preferredWidth: 7
                                    Layout.preferredHeight: 7
                                    radius: 4
                                    color: root.colors.success
                                }
                                AppLabel {
                                    text: "Connecté"
                                    color: root.colors.textSecondary
                                    font.pixelSize: 12
                                    font.weight: Font.DemiBold
                                }
                            }
                        }
                    }

                    GridLayout {
                        Layout.fillWidth: true
                        columns: width >= 900 ? 3 : 1
                        columnSpacing: 12
                        rowSpacing: 10

                        Repeater {
                            model: [
                                { label: "CLASSES", value: JSON.parse(appBridge.classesJson).length, detail: "espaces créés" },
                                { label: "ÉLÈVES", value: teacherClassSelect.currentValue ? appBridge.teacherStudentsForClass(teacherClassSelect.currentValue, "").length : 0, detail: teacherClassSelect.currentValue ? "dans la classe sélectionnée" : "sélectionnez une classe" },
                                { label: "EXERCICES", value: teacherClassSelect.currentValue ? appBridge.teacherPlansForClass(teacherClassSelect.currentValue).length : 0, detail: "pour la classe sélectionnée" }
                            ]
                            delegate: Rectangle {
                                required property var modelData
                                Layout.fillWidth: true
                                Layout.preferredHeight: 88
                                radius: 16
                                gradient: Gradient {
                                    GradientStop { position: 0.0; color: root.colors.glassTop }
                                    GradientStop { position: 1.0; color: root.colors.panel }
                                }
                                border.color: root.colors.glassHighlight
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: 15
                                    anchors.rightMargin: 15
                                    anchors.topMargin: 11
                                    anchors.bottomMargin: 10
                                    spacing: 2
                                    AppLabel {
                                        text: modelData.label
                                        color: root.colors.muted
                                        font.pixelSize: 9
                                        font.weight: Font.Bold
                                        font.letterSpacing: 1.2
                                    }
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 8
                                        AppLabel {
                                            text: modelData.value
                                            color: root.colors.text
                                            font.family: "Manrope"
                                            font.pixelSize: 23
                                            font.weight: Font.Bold
                                        }
                                        AppLabel {
                                            text: modelData.detail
                                            color: root.colors.textSecondary
                                            font.pixelSize: 11
                                            elide: Text.ElideRight
                                            Layout.fillWidth: true
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                GridLayout {
                    visible: root.page === "area" && root.classroomArea === "teacher" && appBridge.teacherAuthenticated
                    Layout.fillWidth: true
                    columns: width >= 900 ? 2 : 1
                    columnSpacing: 18
                    rowSpacing: 18
                    Components.FormPanel {
                        title: "Mes classes"
                        subtitle: "Créez une classe et organisez votre année scolaire."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                    AppLabel {
                        visible: appBridge.classroomMessage !== ""
                        text: appBridge.classroomMessage
                        color: root.colors.accent
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    AppTextField { id: newClassName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Nom de la classe (ex. CM1 A)" }
                    AppTextField { id: newClassYear; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Année scolaire (facultatif)"; onAccepted: appBridge.createClass(newClassName.text, text) }
                    PrimaryButton {
                        text: "Créer la classe"
                        Layout.fillWidth: true
                        onClicked: appBridge.createClass(newClassName.text, newClassYear.text)
                    }
                    }
                    Components.FormPanel {
                        title: "Classes et groupes"
                        subtitle: "Sélectionnez une classe pour modifier ses informations et structurer les groupes."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                    AppComboBox {
                        id: teacherClassSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "name"
                        valueRole: "id"
                        model: JSON.parse(appBridge.classesJson)
                        onActivated: {
                            editClassName.text = currentText
                            editClassYear.text = currentIndex >= 0 ? (model[currentIndex].school_year || "") : ""
                            appBridge.selectStudent("")
                        }
                    }
                    PrimaryButton {
                        text: "Exporter le bilan de cette classe (CSV)"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue
                        fillColor: root.colors.accentSoft
                        hoverColor: root.colors.accentHoverSoft
                        textColor: root.colors.accent
                        onClicked: classReportDialog.open()
                    }
                    AppTextField {
                        id: editClassName
                        Layout.fillWidth: true
                        implicitHeight: 44
                        placeholderText: "Renommer la classe"
                    }
                    AppTextField {
                        id: editClassYear
                        Layout.fillWidth: true
                        implicitHeight: 44
                        placeholderText: "Année scolaire"
                    }
                    PrimaryButton {
                        text: "Enregistrer la classe"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue && editClassName.text.trim().length > 0
                        onClicked: appBridge.updateClass(
                            teacherClassSelect.currentValue, editClassName.text, editClassYear.text
                        )
                    }
                    AppTextField { id: newGroupName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Nom du groupe (facultatif)" }
                    PrimaryButton {
                        text: "Créer le groupe"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue
                        onClicked: appBridge.createGroup(teacherClassSelect.currentValue, newGroupName.text)
                    }
                    AppComboBox {
                        id: teacherGroupSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return [{ name: "Aucun groupe", id: "" }].concat(appBridge.teacherGroupsForClass(teacherClassSelect.currentValue || "")) }
                        onActivated: {
                            editGroupName.text = currentText
                            appBridge.selectStudent("")
                        }
                    }
                    AppTextField {
                        id: editGroupName
                        Layout.fillWidth: true
                        implicitHeight: 44
                        placeholderText: "Renommer le groupe sélectionné"
                    }
                    PrimaryButton {
                        text: "Enregistrer le groupe"
                        Layout.fillWidth: true
                        enabled: !!teacherGroupSelect.currentValue && editGroupName.text.trim().length > 0
                        onClicked: appBridge.updateGroup(teacherGroupSelect.currentValue, editGroupName.text)
                    }
                    AppTextField { id: newStudentName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Prénom ou nom affiché de l'élève"; onAccepted: if (teacherClassSelect.currentValue) appBridge.createStudent(teacherClassSelect.currentValue, text, teacherGroupSelect.currentValue || "") }
                    PrimaryButton {
                        text: "Ajouter l'élève"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue
                        onClicked: appBridge.createStudent(teacherClassSelect.currentValue, newStudentName.text, teacherGroupSelect.currentValue || "")
                    }
                    }
                    Components.FormPanel {
                        title: "Exercices"
                        subtitle: "Préparez un entraînement et attribuez-le à la classe sélectionnée."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                    AppTextField {
                        id: newExerciseName
                        Layout.fillWidth: true
                        implicitHeight: 44
                        placeholderText: "Nom de l'exercice (ex. Révisions des additions)"
                    }
                    AppComboBox {
                        id: exerciseSkillSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "label"
                        valueRole: "id"
                        model: JSON.parse(appBridge.skillsJson)
                    }
                    AppLabel { text: "Nombre de questions"; color: root.colors.textSecondary; font.pixelSize: 13 }
                    AppSpinBox { id: exerciseCountSelect; from: 5; to: 30; value: 10; editable: true; Layout.fillWidth: true }
                    AppLabel { text: "Difficulté"; color: root.colors.textSecondary; font.pixelSize: 13 }
                    AppComboBox {
                        id: exerciseDifficultySelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "label"
                        valueRole: "value"
                        model: [
                            { label: "1 · Très accessible", value: 1 },
                            { label: "2 · Accessible", value: 2 },
                            { label: "3 · Intermédiaire", value: 3 },
                            { label: "4 · Soutenue", value: 4 },
                            { label: "5 · Avancée", value: 5 }
                        ]
                    }
                    PrimaryButton {
                        text: "Assigner à cette classe"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue && !!exerciseSkillSelect.currentValue && newExerciseName.text.trim().length > 0
                        onClicked: appBridge.createExercisePlan(
                            teacherClassSelect.currentValue, newExerciseName.text,
                            exerciseSkillSelect.currentValue, exerciseCountSelect.value,
                            exerciseDifficultySelect.currentValue
                        )
                    }
                    AppComboBox {
                        id: teacherPlanSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return appBridge.teacherPlansForClass(teacherClassSelect.currentValue || "") }
                    }
                    PrimaryButton {
                        text: "Archiver l'exercice sélectionné"
                        Layout.fillWidth: true
                        enabled: !!teacherPlanSelect.currentValue
                        fillColor: root.colors.dangerSurface
                        hoverColor: root.colors.dangerHover
                        textColor: root.colors.danger
                        onClicked: appBridge.archiveExercisePlan(teacherPlanSelect.currentValue)
                    }
                    }
                    Components.FormPanel {
                        title: "Archivage"
                        subtitle: "Archivez une classe ou un groupe sans perdre l'historique associé."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        PrimaryButton {
                            text: "Archiver la classe"
                            Layout.fillWidth: true
                            enabled: !!teacherClassSelect.currentValue
                            fillColor: root.colors.dangerSurface
                            hoverColor: root.colors.dangerHover
                            textColor: root.colors.danger
                            onClicked: {
                                archiveConfirmation.archiveKind = "class"
                                archiveConfirmation.archiveId = teacherClassSelect.currentValue
                                archiveConfirmation.open()
                            }
                        }
                        PrimaryButton {
                            text: "Archiver le groupe"
                            Layout.fillWidth: true
                            enabled: !!teacherGroupSelect.currentValue
                            fillColor: root.colors.dangerSurface
                            hoverColor: root.colors.dangerHover
                            textColor: root.colors.danger
                            onClicked: {
                                archiveConfirmation.archiveKind = "group"
                                archiveConfirmation.archiveId = teacherGroupSelect.currentValue
                                archiveConfirmation.open()
                            }
                        }
                    }
                    Components.FormPanel {
                        title: "Élèves et suivi"
                        subtitle: "Sélectionnez un élève pour modifier son profil et consulter ses résultats."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                    AppComboBox {
                        id: teacherStudentSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "display_name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return appBridge.teacherStudentsForClass(teacherClassSelect.currentValue || "", teacherGroupSelect.currentValue || "") }
                        onActivated: {
                            editStudentName.text = currentText
                            appBridge.selectStudent("")
                        }
                    }
                    AppTextField {
                        id: editStudentName
                        Layout.fillWidth: true
                        implicitHeight: 44
                        placeholderText: "Renommer l'élève sélectionné"
                    }
                    PrimaryButton {
                        text: "Enregistrer l'élève"
                        Layout.fillWidth: true
                        enabled: !!teacherStudentSelect.currentValue && editStudentName.text.trim().length > 0
                        onClicked: appBridge.updateStudent(teacherStudentSelect.currentValue, editStudentName.text)
                    }
                    PrimaryButton {
                        text: "Afficher la progression de l'élève"
                        Layout.fillWidth: true
                        enabled: !!teacherStudentSelect.currentValue
                        fillColor: root.colors.accentSoft
                        hoverColor: root.colors.accentHoverSoft
                        textColor: root.colors.accent
                        onClicked: appBridge.selectStudent(teacherStudentSelect.currentValue)
                    }
                    ColumnLayout {
                        visible: !!teacherStudentSelect.currentValue
                        Layout.fillWidth: true
                        spacing: 8
                        AppLabel {
                            text: root.progressSummary.sessions === 0
                                  ? "Aucun résultat enregistré pour cet élève."
                                  : "Séances : " + root.progressSummary.sessions
                                    + " · Réponses : " + root.progressSummary.answered
                                    + " · Réussite : "
                                    + (root.progressSummary.accuracy === null ? "—" : root.progressSummary.accuracy + "%")
                            color: root.colors.muted
                            font.pixelSize: 13
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                        AppLabel {
                            visible: root.progressSummary.skills.length > 0
                            text: "Résultats par compétence"
                            color: root.colors.text
                            font.pixelSize: 14
                            font.weight: Font.DemiBold
                        }
                        Repeater {
                            model: root.progressSummary.skills
                            delegate: Rectangle {
                                required property var modelData
                                Layout.fillWidth: true
                                implicitHeight: 58
                                radius: 10
                                color: root.colors.surfaceHover
                                border.color: root.colors.border
                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: 12
                                    anchors.rightMargin: 12
                                    anchors.topMargin: 8
                                    anchors.bottomMargin: 8
                                    spacing: 12
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 5
                                        AppLabel {
                                            text: modelData.skill_id
                                            color: root.colors.text
                                            font.pixelSize: 12
                                            font.weight: Font.DemiBold
                                        }
                                        Rectangle {
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: 4
                                            radius: 2
                                            color: root.colors.border
                                            Rectangle {
                                                width: parent.width * Math.max(0, Math.min(1, modelData.accuracy / 100))
                                                height: parent.height
                                                radius: 2
                                                color: modelData.accuracy >= 80 ? root.colors.success : root.colors.accent
                                            }
                                        }
                                    }
                                    AppLabel {
                                        text: modelData.correct + "/" + modelData.answered
                                        color: root.colors.muted
                                        font.pixelSize: 11
                                    }
                                    AppLabel {
                                        text: modelData.accuracy + "%"
                                        color: root.colors.accent
                                        font.pixelSize: 13
                                        font.weight: Font.Bold
                                    }
                                }
                            }
                        }
                    }
                    PrimaryButton {
                        text: "Archiver l'élève sélectionné"
                        Layout.fillWidth: true
                        enabled: !!teacherStudentSelect.currentValue
                        fillColor: root.colors.dangerSurface
                        hoverColor: root.colors.dangerHover
                        textColor: root.colors.danger
                        onClicked: {
                            archiveConfirmation.archiveKind = "student"
                            archiveConfirmation.archiveId = teacherStudentSelect.currentValue
                            archiveConfirmation.open()
                        }
                    }
                    }
                    Components.FormPanel {
                        title: "Mon profil"
                        subtitle: "Modifiez votre nom affiché ou fermez votre session."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                    AppTextField { id: teacherDisplayName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Nouveau nom affiché"; onAccepted: appBridge.updateTeacherProfile(text) }
                    PrimaryButton {
                        text: "Enregistrer le profil"
                        Layout.fillWidth: true
                        onClicked: appBridge.updateTeacherProfile(teacherDisplayName.text)
                    }
                    QuietButton { text: "Se déconnecter"; flat: true; Layout.alignment: Qt.AlignHCenter; onClicked: appBridge.logoutTeacher() }
                    }
                }

                    }
                AppLabel {
                    visible: root.page === "area" && appBridge.classroomMessage !== ""
                    text: appBridge.classroomMessage
                    color: root.colors.accent
                    font.pixelSize: 13
                    Layout.alignment: Qt.AlignHCenter
                }

                PrimaryButton {
                    visible: root.page === "area"
                    text: "Retour à l'espace classe"
                    fillColor: root.colors.accentSoft
                    hoverColor: root.colors.accentHoverSoft
                    textColor: root.colors.accent
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        root.classroomArea = ""
                        root.page = "home"
                    }
                }

                PrimaryButton {
                    visible: root.page === "home"
                    text: "Paramètres"
                    fillColor: root.colors.accentSoft
                    hoverColor: root.colors.accentHoverSoft
                    textColor: root.colors.accent
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        root.settingsReturnPage = root.page
                        root.page = "settings"
                    }
                }

                PrimaryButton {
                    visible: root.page === "home"
                    text: "Changer de mode"
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 12
                    onClicked: appBridge.returnToModeChoice()
                }
                }
            }
        }

        Item {
            ScrollView {
                anchors.fill: parent
                clip: true
                contentWidth: availableWidth
                ColumnLayout {
                    width: Math.min(parent.width, 920)
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 24
                    spacing: 20

                AppLabel {
                    visible: appBridge.questionTotal === 0
                    text: "Nouvel entraînement"
                    color: root.colors.text
                    font.pixelSize: 32
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignLeft
                    font.family: "Manrope"
                }

                RowLayout {
                    visible: appBridge.questionTotal === 0 && root.currentMode === "individual"
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 10
                    QuietButton {
                        text: "Paramètres"
                        flat: true
                        onClicked: {
                            root.settingsReturnPage = "practice"
                            root.page = "settings"
                        }
                    }
                    QuietButton {
                        text: "Changer de mode"
                        flat: true
                        onClicked: appBridge.returnToModeChoice()
                    }
                }

                AppLabel {
                    visible: appBridge.questionTotal === 0 && appBridge.feedback !== ""
                    text: appBridge.feedback
                    color: root.colors.warning
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }

                    Components.FormPanel {
                        title: "Votre séance"
                        subtitle: "Choisissez le contenu et le niveau de votre entraînement."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                GridLayout {
                    visible: appBridge.questionTotal === 0
                    Layout.fillWidth: true
                    columns: root.width >= 1050 ? 3 : 1
                    columnSpacing: 12
                    rowSpacing: 12
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 154
                        radius: 14
                        color: root.colors.surfaceHover
                        border.color: root.colors.border
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 13
                            spacing: 8
                            RowLayout {
                                Layout.fillWidth: true
                                AppLabel { text: "01"; color: root.colors.accent; font.pixelSize: 10; font.weight: Font.Bold }
                                AppLabel { text: "CONTENU"; color: root.colors.muted; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1.0 }
                                Item { Layout.fillWidth: true }
                                AppLabel { text: "◎"; color: root.colors.accent; font.pixelSize: 15 }
                            }
                            AppLabel { text: "Compétence"; color: root.colors.text; font.pixelSize: 13; font.weight: Font.DemiBold }
                            AppComboBox {
                                id: skillSelect
                                Layout.fillWidth: true
                                implicitHeight: 44
                                textRole: "label"
                                valueRole: "id"
                                model: JSON.parse(appBridge.skillsJson)
                            }
                            AppLabel { text: "Choisissez ce que vous souhaitez travailler."; color: root.colors.muted; font.pixelSize: 10; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 154
                        radius: 14
                        color: root.colors.surfaceHover
                        border.color: root.colors.border
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 13
                            spacing: 8
                            RowLayout {
                                Layout.fillWidth: true
                                AppLabel { text: "02"; color: root.colors.accent; font.pixelSize: 10; font.weight: Font.Bold }
                                AppLabel { text: "FORMAT"; color: root.colors.muted; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1.0 }
                                Item { Layout.fillWidth: true }
                                AppLabel { text: "▤"; color: root.colors.accent; font.pixelSize: 15 }
                            }
                            AppLabel { text: "Nombre de questions"; color: root.colors.text; font.pixelSize: 13; font.weight: Font.DemiBold }
                            AppSpinBox {
                                id: countSelect
                                from: 5
                                to: 30
                                value: 10
                                editable: true
                                implicitHeight: 44
                                Layout.fillWidth: true
                            }
                            AppLabel { text: "De 5 à 30 questions par séance."; color: root.colors.muted; font.pixelSize: 10; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 154
                        radius: 14
                        color: root.colors.surfaceHover
                        border.color: root.colors.border
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 13
                            spacing: 8
                            RowLayout {
                                Layout.fillWidth: true
                                AppLabel { text: "03"; color: root.colors.accent; font.pixelSize: 10; font.weight: Font.Bold }
                                AppLabel { text: "INTENSITÉ"; color: root.colors.muted; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1.0 }
                                Item { Layout.fillWidth: true }
                                AppLabel { text: "↗"; color: root.colors.accent; font.pixelSize: 15 }
                            }
                            AppLabel { text: "Difficulté"; color: root.colors.text; font.pixelSize: 13; font.weight: Font.DemiBold }
                            AppComboBox {
                                id: difficultySelect
                                Layout.fillWidth: true
                                implicitHeight: 44
                                model: [
                                    { label: "1 · Très accessible", value: 1 },
                                    { label: "2 · Accessible", value: 2 },
                                    { label: "3 · Intermédiaire", value: 3 },
                                    { label: "4 · Soutenue", value: 4 },
                                    { label: "5 · Avancée", value: 5 }
                                ]
                                textRole: "label"
                                valueRole: "value"
                            }
                            AppLabel { text: "Ajustez le niveau à votre rythme."; color: root.colors.muted; font.pixelSize: 10; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                        }
                    }
                    PrimaryButton {
                        text: "Lancer l'entraînement  →"
                        Layout.fillWidth: true
                        Layout.columnSpan: root.width >= 1050 ? 3 : 1
                        Layout.topMargin: 4
                        implicitHeight: 52
                        onClicked: appBridge.startPractice(skillSelect.currentValue, countSelect.value, difficultySelect.currentValue)
                    }
                }

                    }
                Components.FormPanel {
                    title: "À vous de jouer"
                    subtitle: "Concentrez-vous sur une question à la fois. Vous avancez à votre rythme."
                    palette: root.colors
                    visible: appBridge.questionTotal > 0 && !appBridge.practiceFinished
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignTop
                    contentSpacing: 18

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Rectangle {
                            Layout.preferredWidth: 42
                            Layout.preferredHeight: 42
                            radius: 13
                            color: root.colors.accentSoft
                            AppLabel {
                                anchors.centerIn: parent
                                text: "✦"
                                color: root.colors.accent
                                font.pixelSize: 19
                                font.weight: Font.Bold
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2
                            AppLabel {
                                text: "Votre progression"
                                color: root.colors.text
                                font.pixelSize: 14
                                font.weight: Font.DemiBold
                            }
                            AppLabel {
                                text: "Question " + appBridge.questionNumber + " sur " + appBridge.questionTotal
                                color: root.colors.muted
                                font.pixelSize: 12
                            }
                        }
                        Rectangle {
                            Layout.preferredWidth: 62
                            Layout.preferredHeight: 30
                            radius: 15
                            color: root.colors.surfaceHover
                            AppLabel {
                                anchors.centerIn: parent
                                text: Math.round(appBridge.questionNumber / Math.max(1, appBridge.questionTotal) * 100) + "%"
                                color: root.colors.accent
                                font.pixelSize: 12
                                font.weight: Font.Bold
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 7
                        radius: 4
                        color: root.colors.border
                        clip: true
                        Rectangle {
                            width: parent.width * appBridge.questionNumber / Math.max(1, appBridge.questionTotal)
                            height: parent.height
                            radius: 4
                            color: root.colors.accent
                            Behavior on width { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.topMargin: 2
                        Layout.bottomMargin: 2
                        implicitHeight: 190
                        radius: 18
                        layer.enabled: true
                        layer.effect: MultiEffect {
                            shadowEnabled: true
                            shadowColor: root.colors.shadow
                            shadowBlur: 0.42
                            shadowOpacity: 0.16
                            shadowVerticalOffset: 6
                        }
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: root.colors.glassTop }
                            GradientStop { position: 1.0; color: root.colors.accentSoft }
                        }
                        border.color: root.colors.glassHighlight
                        clip: true
                        Rectangle {
                            width: 190; height: 190; radius: 95
                            anchors.right: parent.right; anchors.rightMargin: -62
                            anchors.top: parent.top; anchors.topMargin: -76
                            color: root.colors.accent; opacity: 0.055
                        }
                        Rectangle {
                            width: 130; height: 130; radius: 65
                            anchors.left: parent.left; anchors.leftMargin: -58
                            anchors.bottom: parent.bottom; anchors.bottomMargin: -76
                            color: root.colors.accent; opacity: 0.045
                        }
                        ColumnLayout {
                            anchors.centerIn: parent
                            spacing: 9
                            AppLabel {
                                text: "À VOUS DE JOUER"
                                color: root.colors.accent
                                font.pixelSize: 10
                                font.weight: Font.Bold
                                font.letterSpacing: 1.8
                                Layout.alignment: Qt.AlignHCenter
                            }
                            AppLabel {
                                text: appBridge.questionPrompt
                                color: root.colors.text
                                font.pixelSize: 50
                                font.weight: Font.Bold
                                font.family: "Manrope"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            AppLabel {
                                text: "Prenez votre temps et trouvez le résultat."
                                color: root.colors.textSecondary
                                font.pixelSize: 11
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                    }

                    AppLabel {
                        text: "Votre réponse"
                        color: root.colors.textSecondary
                        font.pixelSize: 13
                        font.weight: Font.DemiBold
                    }
                    AppTextField {
                        id: answerInput
                        Layout.fillWidth: true
                        implicitHeight: 60
                        enabled: !appBridge.answerSubmitted
                        placeholderText: "Écrivez votre résultat…"
                        horizontalAlignment: TextInput.AlignHCenter
                        font.pixelSize: 23
                        onAccepted: if (!appBridge.answerSubmitted) appBridge.submitAnswer(text)
                    }
                    Rectangle {
                        visible: appBridge.answerSubmitted
                        Layout.fillWidth: true
                        implicitHeight: feedbackLabel.implicitHeight + 24
                        radius: 11
                        color: appBridge.feedback === "Bonne réponse !" ? root.colors.accentSoft : root.colors.surfaceHover
                        border.color: appBridge.feedback === "Bonne réponse !" ? root.colors.success : root.colors.warning
                        AppLabel {
                            id: feedbackLabel
                            anchors.fill: parent
                            anchors.margins: 12
                            text: appBridge.feedback
                            color: appBridge.feedback === "Bonne réponse !" ? root.colors.success : root.colors.warning
                            font.pixelSize: 14
                            font.weight: Font.DemiBold
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            wrapMode: Text.WordWrap
                        }
                    }
                    PrimaryButton {
                        visible: !appBridge.answerSubmitted
                        text: "Vérifier ma réponse  →"
                        Layout.fillWidth: true
                        implicitHeight: 50
                        onClicked: appBridge.submitAnswer(answerInput.text)
                    }
                    PrimaryButton {
                        visible: appBridge.answerSubmitted
                        text: appBridge.questionNumber === appBridge.questionTotal ? "Terminer la séance  →" : "Continuer  →"
                        Layout.fillWidth: true
                        implicitHeight: 50
                        onClicked: {
                            answerInput.text = ""
                            appBridge.nextQuestion()
                        }
                    }
                    AppLabel {
                        text: "Astuce : appuyez sur Entrée pour valider votre réponse."
                        color: root.colors.muted
                        font.pixelSize: 11
                        Layout.alignment: Qt.AlignHCenter
                    }
                }

                Components.FormPanel {
                    title: "Séance terminée"
                    subtitle: "Bravo pour votre effort. Voici le récapitulatif de votre entraînement."
                    palette: root.colors
                    visible: appBridge.practiceFinished
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignTop
                    contentSpacing: 18
                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: 170
                        radius: 16
                        color: root.colors.accentSoft
                        border.color: root.colors.border
                        ColumnLayout {
                            anchors.centerIn: parent
                            spacing: 9
                            AppLabel {
                                text: "SÉANCE ACCOMPLIE"
                                color: root.colors.accent
                                font.pixelSize: 10
                                font.weight: Font.Bold
                                font.letterSpacing: 1.4
                                Layout.alignment: Qt.AlignHCenter
                            }
                            AppLabel {
                                text: appBridge.scoreText
                                color: root.colors.text
                                font.pixelSize: 26
                                font.weight: Font.Bold
                                font.family: "Manrope"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            AppLabel {
                                text: "Chaque séance vous fait progresser."
                                color: root.colors.textSecondary
                                font.pixelSize: 12
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                    }
                    PrimaryButton {
                        text: root.currentMode === "classroom" ? "Retour à l'espace élève" : "Retour à l'espace individuel"
                        Layout.fillWidth: true
                        implicitHeight: 50
                        onClicked: {
                            appBridge.abandonPractice()
                            root.page = root.currentMode === "classroom" ? "area" : "home"
                        }
                    }
                }

                QuietButton {
                    visible: !appBridge.practiceFinished
                    text: "Quitter la séance"
                    flat: true
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        appBridge.abandonPractice()
                        root.page = root.currentMode === "classroom" ? "area" : "home"
                    }
                }
            }
            }
        }

        Item {
            ScrollView {
                anchors.fill: parent
                contentWidth: availableWidth
                ColumnLayout {
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 24
                    width: Math.min(parent.width, 1040)
                    spacing: 18

                    AppLabel {
                    text: "Paramètres"
                    color: root.colors.text
                    font.pixelSize: 32
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignLeft
                    font.family: "Manrope"
                }
                    Components.FormPanel {
                        title: "Apparence"
                        subtitle: "Personnalisez l'apparence de Wedone Operate."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                AppComboBox {
                    id: themeModeSelect
                    Layout.fillWidth: true
                    implicitHeight: 46
                    textRole: "label"
                    valueRole: "value"
                    model: [
                        { label: "Automatique · suivre le système", value: "system" },
                        { label: "Clair", value: "light" },
                        { label: "Sombre", value: "dark" }
                    ]
                    currentIndex: appBridge.themeMode === "light" ? 1
                                  : appBridge.themeMode === "dark" ? 2 : 0
                    onActivated: appBridge.setThemeMode(currentValue)
                }
                    }
                    Components.FormPanel {
                        title: "Accessibilité"
                        subtitle: "Adaptez l'interface à vos préférences de confort visuel."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                AppLabel { text: "Taille de l'interface · " + Math.round(appBridge.uiScale * 100) + "%"; color: root.colors.textSecondary; font.pixelSize: 15 }
                AppSlider {
                    id: scaleSlider
                    Layout.fillWidth: true
                    from: 0.85
                    to: 1.25
                    stepSize: 0.05
                    value: appBridge.uiScale
                    onMoved: appBridge.setUiScale(value)
                }
                AppCheckBox {
                    text: "Contraste renforcé"
                    checked: appBridge.highContrast
                    onToggled: appBridge.setHighContrast(checked)
                }
                AppCheckBox {
                    text: "Réduire les animations"
                    checked: appBridge.reduceMotion
                    onToggled: appBridge.setReduceMotion(checked)
                }
                    }
                    Components.FormPanel {
                        title: "Données et sauvegardes"
                        subtitle: "Importez, exportez et restaurez vos données en toute sécurité."
                        palette: root.colors
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop

                GridLayout {
                    columns: 2
                    columnSpacing: 12
                    rowSpacing: 12
                    Repeater {
                        model: [
                            { title: "Créer une sauvegarde", detail: "Enregistrer une copie de sécurité.", action: "backup" },
                            { title: "Exporter en JSON", detail: "Récupérer une copie portable des données.", action: "export" },
                            { title: "Importer un export", detail: "Ajouter des données depuis un fichier JSON.", action: "import" },
                            { title: "Restaurer une sauvegarde", detail: "Revenir à une sauvegarde existante.", action: "restore" }
                        ]
                        delegate: Rectangle {
                            required property var modelData
                            Layout.fillWidth: true
                            Layout.minimumWidth: 0
                            implicitHeight: 132
                            radius: 13
                            color: root.colors.surfaceHover
                            border.color: root.colors.border
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 13
                                spacing: 5
                                RowLayout {
                                    Layout.fillWidth: true
                                    AppLabel {
                                        text: modelData.action === "backup" ? "◫" : modelData.action === "export" ? "↗" : modelData.action === "import" ? "↙" : "⟲"
                                        color: root.colors.accent
                                        font.pixelSize: 17
                                    }
                                    Item { Layout.fillWidth: true }
                                    AppLabel { text: "DONNÉES"; color: root.colors.muted; font.pixelSize: 9; font.weight: Font.Bold; font.letterSpacing: 0.9 }
                                }
                                AppLabel { text: modelData.title; color: root.colors.text; font.pixelSize: 12; font.weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.WordWrap }
                                AppLabel { text: modelData.detail; color: root.colors.muted; font.pixelSize: 10; Layout.fillWidth: true; wrapMode: Text.WordWrap; Layout.fillHeight: true; verticalAlignment: Text.AlignVCenter }
                                PrimaryButton {
                                    text: modelData.action === "backup" ? "Créer" : modelData.action === "export" ? "Exporter" : modelData.action === "import" ? "Importer" : "Restaurer"
                                    Layout.fillWidth: true
                                    implicitHeight: 36
                                    onClicked: {
                                        if (modelData.action === "backup") appBridge.createBackup()
                                        else if (modelData.action === "export") exportDialog.open()
                                        else if (modelData.action === "import") importDialog.open()
                                        else restoreDialog.open()
                                    }
                                }
                            }
                        }
                    }
                }
                    }
                QuietButton {
                    text: "Réinitialiser toutes les données"
                    flat: true
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: resetConfirmation.open()
                }
                AppLabel {
                    visible: appBridge.dataMessage !== ""
                    text: appBridge.dataMessage
                    color: root.colors.accent
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                PrimaryButton {
                    text: "Retour"
                    Layout.fillWidth: true
                    onClicked: root.page = root.settingsReturnPage
                }
                }
            }
        }
    }

    FileDialog {
        id: classReportDialog
        title: "Exporter le bilan de la classe"
        fileMode: FileDialog.SaveFile
        nameFilters: ["Rapport de classe (*.csv)"]
        onAccepted: appBridge.exportClassReport(
            teacherClassSelect.currentValue, selectedFile.toLocalFile()
        )
    }

    FileDialog {
        id: exportDialog
        title: "Exporter les données Phoenix"
        fileMode: FileDialog.SaveFile
        nameFilters: ["Export Phoenix (*.json)"]
        onAccepted: appBridge.exportData(selectedFile.toLocalFile())
    }

    FileDialog {
        id: importDialog
        title: "Importer un export Phoenix"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Export Phoenix (*.json)"]
        onAccepted: appBridge.importData(selectedFile.toLocalFile())
    }

    FileDialog {
        id: restoreDialog
        title: "Restaurer une sauvegarde Phoenix"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Sauvegarde SQLite (*.sqlite3 *.db)"]
        onAccepted: appBridge.restoreBackup(selectedFile.toLocalFile())
    }

    Dialog {
        id: archiveConfirmation
        property string archiveKind: ""
        property string archiveId: ""
        title: "Archiver cet élément ?"
        modal: true
        anchors.centerIn: parent
        width: Math.min(440, root.width - 40)
        padding: 22
        spacing: 16
        background: Rectangle {
            radius: 19
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: root.colors.shadow
                shadowBlur: 0.55
                shadowOpacity: 0.24
                shadowVerticalOffset: 10
            }
            gradient: Gradient {
                GradientStop { position: 0.0; color: root.colors.glassTop }
                GradientStop { position: 1.0; color: root.colors.surface }
            }
            border.color: root.colors.border
            border.width: 1
            Rectangle {
                anchors.fill: parent
                anchors.margins: 1
                radius: parent.radius - 1
                color: "transparent"
                border.color: root.colors.glassHighlight
                opacity: 0.55
            }
        }
        AppLabel {
            width: archiveConfirmation.availableWidth
            text: "L'élément ne sera plus proposé dans les listes actives. Les résultats et l'historique associés seront conservés."
            color: root.colors.textSecondary
            wrapMode: Text.WordWrap
        }
        footer: RowLayout {
            width: archiveConfirmation.availableWidth
            spacing: 9
            QuietButton {
                text: "Annuler"
                Layout.preferredWidth: 112
                onClicked: archiveConfirmation.reject()
            }
            PrimaryButton {
                text: "Archiver"
                Layout.preferredWidth: 120
                onClicked: archiveConfirmation.accept()
            }
        }
        enter: Transition {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 140 }
            NumberAnimation { property: "scale"; from: 0.97; to: 1; duration: 140; easing.type: Easing.OutCubic }
        }
        exit: Transition {
            NumberAnimation { property: "opacity"; from: 1; to: 0; duration: 100 }
        }
        onAccepted: {
            if (archiveKind === "student") appBridge.archiveStudent(archiveId)
            else if (archiveKind === "group") appBridge.archiveGroup(archiveId)
            else if (archiveKind === "class") appBridge.archiveClass(archiveId)
        }
    }

    Dialog {
        id: resetConfirmation
        title: "Réinitialiser les données ?"
        modal: true
        anchors.centerIn: parent
        width: Math.min(480, root.width - 40)
        padding: 22
        spacing: 16
        background: Rectangle {
            radius: 19
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: root.colors.shadow
                shadowBlur: 0.55
                shadowOpacity: 0.24
                shadowVerticalOffset: 10
            }
            gradient: Gradient {
                GradientStop { position: 0.0; color: root.colors.glassTop }
                GradientStop { position: 1.0; color: root.colors.surface }
            }
            border.color: root.colors.danger
            border.width: 1
            Rectangle {
                anchors.fill: parent
                anchors.margins: 1
                radius: parent.radius - 1
                color: "transparent"
                border.color: root.colors.glassHighlight
                opacity: 0.55
            }
        }
        AppLabel {
            width: resetConfirmation.availableWidth
            text: "Toutes les classes, tous les profils, les réglages et l'historique Phoenix seront supprimés. Une sauvegarde de sécurité sera créée avant l'opération."
            color: root.colors.textSecondary
            wrapMode: Text.WordWrap
        }
        footer: RowLayout {
            width: resetConfirmation.availableWidth
            spacing: 9
            QuietButton {
                text: "Annuler"
                Layout.preferredWidth: 112
                onClicked: resetConfirmation.reject()
            }
            PrimaryButton {
                text: "Tout supprimer"
                kind: "danger"
                Layout.preferredWidth: 142
                onClicked: resetConfirmation.accept()
            }
        }
        enter: Transition {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 140 }
            NumberAnimation { property: "scale"; from: 0.97; to: 1; duration: 140; easing.type: Easing.OutCubic }
        }
        exit: Transition {
            NumberAnimation { property: "opacity"; from: 1; to: 0; duration: 100 }
        }
        onAccepted: appBridge.resetData()
    }
}
