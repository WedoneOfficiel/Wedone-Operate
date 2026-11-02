import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 1120
    height: 760
    minimumWidth: 760
    minimumHeight: 560
    visible: true
    title: "Wedone Operate"
    color: "#F4F7FC"

    property string currentMode: appBridge.mode
    property string page: currentMode === "" ? "welcome" : "home"
    property string classroomArea: ""

    Rectangle {
        anchors.fill: parent
        color: "#F4F7FC"

        Rectangle {
            width: 500
            height: 500
            radius: 250
            x: parent.width - 250
            y: -220
            color: "#E7F0FF"
            opacity: 0.8
        }
        Rectangle {
            width: 360
            height: 360
            radius: 180
            x: -190
            y: parent.height - 210
            color: "#E9F5FF"
            opacity: 0.8
        }
    }

    header: ToolBar {
        background: Rectangle { color: "#FFFFFF"; border.color: "#E7ECF4" }
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 28
            anchors.rightMargin: 28
            spacing: 12

            Rectangle {
                width: 34
                height: 34
                radius: 10
                color: "#1769D2"
                Text {
                    anchors.centerIn: parent
                    text: "W"
                    color: "white"
                    font.pixelSize: 19
                    font.weight: Font.Bold
                }
            }
            Label {
                text: "wedone"
                color: "#15243A"
                font.pixelSize: 19
                font.weight: Font.DemiBold
            }
            Label {
                text: "OPERATE"
                color: "#71819A"
                font.pixelSize: 10
                font.weight: Font.Bold
                Layout.leftMargin: -7
                Layout.alignment: Qt.AlignVCenter
            }
            Item { Layout.fillWidth: true }
            Label {
                visible: root.currentMode !== ""
                text: root.currentMode === "individual" ? "Espace individuel" : "Espace classe"
                color: "#64748B"
                font.pixelSize: 13
            }
        }
    }

    Connections {
        target: appBridge
        function onModeChanged(mode) {
            root.currentMode = mode
            root.page = mode === "" ? "welcome" : "home"
            root.classroomArea = ""
        }
    }

    component PrimaryButton: Button {
        id: control
        property color fillColor: "#1769D2"
        property color hoverColor: "#0F56B5"
        implicitHeight: 52
        contentItem: Text {
            text: control.text
            color: "white"
            font.pixelSize: 15
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        background: Rectangle {
            radius: 13
            color: control.down ? control.hoverColor : (control.hovered ? control.hoverColor : control.fillColor)
        }
    }

    component ModeCard: Rectangle {
        id: card
        property string heading
        property string subtitle
        property string symbol
        property string actionMode
        signal chosen(string mode)
        radius: 22
        color: "#FFFFFF"
        border.width: 1
        border.color: "#E3EAF4"
        implicitWidth: 340
        implicitHeight: 260

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 26
            spacing: 14
            Rectangle {
                width: 54
                height: 54
                radius: 16
                color: "#EAF2FF"
                Text {
                    anchors.centerIn: parent
                    text: card.symbol
                    color: "#1769D2"
                    font.pixelSize: 25
                    font.weight: Font.DemiBold
                }
            }
            Label {
                text: card.heading
                color: "#172A45"
                font.pixelSize: 22
                font.weight: Font.DemiBold
            }
            Label {
                text: card.subtitle
                color: "#66768E"
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
        anchors.fill: parent
        anchors.margins: 42
        currentIndex: root.page === "welcome" ? 0 : root.page === "home" ? 1 : 2

        Item {
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width, 760)
                spacing: 22

                Label {
                    text: "Bienvenue."
                    color: "#172A45"
                    font.pixelSize: 38
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignHCenter
                }
                Label {
                    text: "Comment souhaitez-vous utiliser Wedone Operate ?"
                    color: "#66768E"
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
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width, 720)
                spacing: 20

                Label {
                    text: root.currentMode === "individual" ? "Votre espace de pratique" : "Espace classe"
                    color: "#172A45"
                    font.pixelSize: 34
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignHCenter
                }

                Label {
                    visible: root.currentMode === "individual"
                    text: "L'espace individuel est sélectionné."
                    color: "#66768E"
                    font.pixelSize: 16
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    visible: root.currentMode === "classroom"
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 18
                    Repeater {
                        model: [
                            { title: "Espace élève", detail: "Accéder à une classe et à un profil.", icon: "◎" },
                            { title: "Espace professeur", detail: "Gérer les classes et les entraînements.", icon: "▤" }
                        ]
                        delegate: Rectangle {
                            required property var modelData
                            width: 300
                            height: 190
                            radius: 20
                            color: "#FFFFFF"
                            border.color: "#E3EAF4"
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 22
                                spacing: 10
                                Label {
                                    text: modelData.icon
                                    color: "#1769D2"
                                    font.pixelSize: 26
                                }
                                Label {
                                    text: modelData.title
                                    color: "#172A45"
                                    font.pixelSize: 20
                                    font.weight: Font.DemiBold
                                }
                                Label {
                                    text: modelData.detail
                                    color: "#66768E"
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
                                        root.page = "area"
                                    }
                                }
                            }
                        }
                    }
                }

                Label {
                    visible: root.page === "area"
                    text: root.classroomArea === "student" ? "Espace élève" : "Espace professeur"
                    color: "#172A45"
                    font.pixelSize: 28
                    font.weight: Font.DemiBold
                    Layout.alignment: Qt.AlignHCenter
                }

                PrimaryButton {
                    text: "Changer de mode"
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 12
                    onClicked: appBridge.returnToModeChoice()
                }
            }
        }

        Item {
            Label { anchors.centerIn: parent; text: "Espace"; color: "#172A45"; font.pixelSize: 28 }
        }
    }
}
