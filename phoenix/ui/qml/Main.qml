import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    id: root
    width: 1120
    height: 760
    minimumWidth: 760
    minimumHeight: 560
    visible: true
    title: "Wedone Operate"
    color: appBridge.highContrast ? "#FFFFFF" : "#F4F7FC"

    property real uiScale: appBridge.uiScale
    property var progressSummary: JSON.parse(appBridge.progressJson)
    property string settingsReturnPage: "home"
    property string currentMode: appBridge.mode
    property string page: currentMode === "" ? "welcome" : currentMode === "individual" ? "practice" : "home"
    property string classroomArea: ""

    Rectangle {
        anchors.fill: parent
        color: appBridge.highContrast ? "#FFFFFF" : "#F4F7FC"

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
            root.page = mode === "" ? "welcome" : mode === "individual" ? "practice" : "home"
            root.classroomArea = ""
        }
    }

    component PrimaryButton: Button {
        id: control
        property color fillColor: "#1769D2"
        property color hoverColor: "#0F56B5"
        property color textColor: "white"
        implicitHeight: 52
        contentItem: Text {
            text: control.text
            color: control.textColor
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
        implicitWidth: 320
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
        x: 42 / root.uiScale
        y: 42 / root.uiScale
        width: (parent.width - 84) / root.uiScale
        height: (parent.height - 84) / root.uiScale
        scale: root.uiScale
        transformOrigin: Item.TopLeft
        currentIndex: root.page === "welcome" ? 0 : root.page === "practice" ? 2 : root.page === "settings" ? 3 : 1

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
                    visible: root.currentMode === "individual"
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 12
                    Repeater {
                        model: [
                            { label: "Séances", value: root.progressSummary.sessions },
                            { label: "Réponses", value: root.progressSummary.answered },
                            { label: "Réussite", value: root.progressSummary.accuracy === null ? "—" : root.progressSummary.accuracy + "%" }
                        ]
                        delegate: Rectangle {
                            required property var modelData
                            width: 150
                            height: 88
                            radius: 16
                            color: "#FFFFFF"
                            border.color: "#E3EAF4"
                            ColumnLayout {
                                anchors.centerIn: parent
                                spacing: 4
                                Label {
                                    text: modelData.value
                                    color: "#1769D2"
                                    font.pixelSize: 23
                                    font.weight: Font.Bold
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                Label {
                                    text: modelData.label
                                    color: "#66768E"
                                    font.pixelSize: 12
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                        }
                    }
                }

                PrimaryButton {
                    visible: root.currentMode === "individual"
                    text: "Commencer une séance"
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 12
                    width: 280
                    onClicked: root.page = "practice"
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
                                        if (index === 0) appBridge.selectStudent("")
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

                ColumnLayout {
                    visible: root.page === "area" && root.classroomArea === "student"
                    Layout.fillWidth: true
                    spacing: 12
                    Label { text: "Classe"; color: "#33445D"; font.pixelSize: 14; font.weight: Font.DemiBold }
                    ComboBox {
                        id: studentClassSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "name"
                        valueRole: "id"
                        model: JSON.parse(appBridge.classesJson)
                        onActivated: appBridge.selectStudent("")
                    }
                    Label { text: "Groupe (facultatif)"; color: "#33445D"; font.pixelSize: 14; font.weight: Font.DemiBold }
                    ComboBox {
                        id: studentGroupSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return [{ name: "Tous les groupes", id: "" }].concat(appBridge.groupsForClass(studentClassSelect.currentValue || "")) }
                        onActivated: appBridge.selectStudent("")
                    }
                    Label { text: "Élève"; color: "#33445D"; font.pixelSize: 14; font.weight: Font.DemiBold }
                    ComboBox {
                        id: studentProfileSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "display_name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return appBridge.studentsForClass(studentClassSelect.currentValue || "", studentGroupSelect.currentValue || "") }
                        onActivated: appBridge.selectStudent(currentValue)
                    }

                    Label {
                        visible: !!studentProfileSelect.currentValue
                        text: root.progressSummary.sessions === 0 ? "Pas encore de résultat pour cet élève." : "Séances : " + root.progressSummary.sessions + " · Réponses : " + root.progressSummary.answered + " · Réussite : " + (root.progressSummary.accuracy === null ? "—" : root.progressSummary.accuracy + "%")
                        color: "#66768E"
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
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
                    Button {
                        text: "S'entraîner sans profil"
                        flat: true
                        Layout.alignment: Qt.AlignHCenter
                        onClicked: {
                            appBridge.selectStudent("")
                            root.page = "practice"
                        }
                    }
                }

                ColumnLayout {
                    visible: root.page === "area" && root.classroomArea === "teacher" && !appBridge.teacherAuthenticated
                    Layout.fillWidth: true
                    spacing: 10
                    Label { text: "Se connecter"; color: "#172A45"; font.pixelSize: 20; font.weight: Font.DemiBold }
                    ComboBox {
                        id: teacherSelect
                        Layout.fillWidth: true
                        implicitHeight: 46
                        textRole: "display_name"
                        valueRole: "id"
                        model: JSON.parse(appBridge.teachersJson)
                    }
                    TextField {
                        id: teacherLoginPassword
                        Layout.fillWidth: true
                        implicitHeight: 46
                        placeholderText: "Mot de passe professeur"
                        echoMode: TextInput.Password
                        onAccepted: appBridge.loginTeacher(teacherSelect.currentValue || "", text)
                    }
                    PrimaryButton {
                        text: "Se connecter"
                        Layout.fillWidth: true
                        enabled: !!teacherSelect.currentValue
                        onClicked: appBridge.loginTeacher(teacherSelect.currentValue, teacherLoginPassword.text)
                    }
                    Label { text: "Créer un profil professeur"; color: "#172A45"; font.pixelSize: 20; font.weight: Font.DemiBold; Layout.topMargin: 10 }
                    TextField { id: newTeacherName; Layout.fillWidth: true; implicitHeight: 46; placeholderText: "Votre nom" }
                    TextField {
                        id: newTeacherPassword
                        Layout.fillWidth: true
                        implicitHeight: 46
                        placeholderText: "Mot de passe (8 caractères minimum)"
                        echoMode: TextInput.Password
                        onAccepted: appBridge.createTeacher(newTeacherName.text, text)
                    }
                    PrimaryButton {
                        text: "Créer mon profil"
                        Layout.fillWidth: true
                        onClicked: appBridge.createTeacher(newTeacherName.text, newTeacherPassword.text)
                    }
                }

                ColumnLayout {
                    visible: root.page === "area" && root.classroomArea === "teacher" && appBridge.teacherAuthenticated
                    Layout.fillWidth: true
                    spacing: 10
                    Label { text: "Mes classes"; color: "#172A45"; font.pixelSize: 20; font.weight: Font.DemiBold }
                    TextField { id: newClassName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Nom de la classe (ex. CM1 A)" }
                    TextField { id: newClassYear; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Année scolaire (facultatif)"; onAccepted: appBridge.createClass(newClassName.text, text) }
                    PrimaryButton {
                        text: "Créer la classe"
                        Layout.fillWidth: true
                        onClicked: appBridge.createClass(newClassName.text, newClassYear.text)
                    }
                    Label { text: "Ajouter un élève"; color: "#172A45"; font.pixelSize: 20; font.weight: Font.DemiBold; Layout.topMargin: 10 }
                    ComboBox {
                        id: teacherClassSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "name"
                        valueRole: "id"
                        model: JSON.parse(appBridge.classesJson)
                    }
                    TextField { id: newGroupName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Nom du groupe (facultatif)" }
                    PrimaryButton {
                        text: "Créer le groupe"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue
                        onClicked: appBridge.createGroup(teacherClassSelect.currentValue, newGroupName.text)
                    }
                    ComboBox {
                        id: teacherGroupSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return [{ name: "Aucun groupe", id: "" }].concat(appBridge.groupsForClass(teacherClassSelect.currentValue || "")) }
                    }
                    TextField { id: newStudentName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Prénom ou nom affiché de l'élève"; onAccepted: if (teacherClassSelect.currentValue) appBridge.createStudent(teacherClassSelect.currentValue, text, teacherGroupSelect.currentValue || "") }
                    PrimaryButton {
                        text: "Ajouter l'élève"
                        Layout.fillWidth: true
                        enabled: !!teacherClassSelect.currentValue
                        onClicked: appBridge.createStudent(teacherClassSelect.currentValue, newStudentName.text, teacherGroupSelect.currentValue || "")
                    }
                    Label { text: "Archiver des éléments"; color: "#172A45"; font.pixelSize: 20; font.weight: Font.DemiBold; Layout.topMargin: 16 }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        PrimaryButton {
                            text: "Archiver la classe"
                            Layout.fillWidth: true
                            enabled: !!teacherClassSelect.currentValue
                            fillColor: "#FCEEEE"
                            hoverColor: "#F8DADA"
                            textColor: "#A12C2C"
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
                            fillColor: "#FCEEEE"
                            hoverColor: "#F8DADA"
                            textColor: "#A12C2C"
                            onClicked: {
                                archiveConfirmation.archiveKind = "group"
                                archiveConfirmation.archiveId = teacherGroupSelect.currentValue
                                archiveConfirmation.open()
                            }
                        }
                    }
                    ComboBox {
                        id: teacherStudentSelect
                        Layout.fillWidth: true
                        implicitHeight: 44
                        textRole: "display_name"
                        valueRole: "id"
                        model: { appBridge.classroomRevision; return appBridge.studentsForClass(teacherClassSelect.currentValue || "", teacherGroupSelect.currentValue || "") }
                    }
                    PrimaryButton {
                        text: "Archiver l'élève sélectionné"
                        Layout.fillWidth: true
                        enabled: !!teacherStudentSelect.currentValue
                        fillColor: "#FCEEEE"
                        hoverColor: "#F8DADA"
                        textColor: "#A12C2C"
                        onClicked: {
                            archiveConfirmation.archiveKind = "student"
                            archiveConfirmation.archiveId = teacherStudentSelect.currentValue
                            archiveConfirmation.open()
                        }
                    }
                    Label { text: "Modifier mon profil"; color: "#172A45"; font.pixelSize: 20; font.weight: Font.DemiBold; Layout.topMargin: 10 }
                    TextField { id: teacherDisplayName; Layout.fillWidth: true; implicitHeight: 44; placeholderText: "Nouveau nom affiché"; onAccepted: appBridge.updateTeacherProfile(text) }
                    PrimaryButton {
                        text: "Enregistrer le profil"
                        Layout.fillWidth: true
                        onClicked: appBridge.updateTeacherProfile(teacherDisplayName.text)
                    }
                    Button { text: "Se déconnecter"; flat: true; Layout.alignment: Qt.AlignHCenter; onClicked: appBridge.logoutTeacher() }
                }

                Label {
                    visible: root.page === "area" && appBridge.classroomMessage !== ""
                    text: appBridge.classroomMessage
                    color: "#1769D2"
                    font.pixelSize: 13
                    Layout.alignment: Qt.AlignHCenter
                }

                PrimaryButton {
                    visible: root.page === "area"
                    text: "Retour à l'espace classe"
                    fillColor: "#E8F0FC"
                    hoverColor: "#D8E6FA"
                    textColor: "#1769D2"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        root.classroomArea = ""
                        root.page = "home"
                    }
                }

                PrimaryButton {
                    visible: root.page === "home"
                    text: "Paramètres"
                    fillColor: "#E8F0FC"
                    hoverColor: "#D8E6FA"
                    textColor: "#1769D2"
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

        Item {
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width, 680)
                spacing: 18

                Label {
                    visible: appBridge.questionTotal === 0
                    text: "Nouvel entraînement"
                    color: "#172A45"
                    font.pixelSize: 32
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    visible: appBridge.questionTotal === 0 && root.currentMode === "individual"
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 10
                    Button {
                        text: "Paramètres"
                        flat: true
                        onClicked: {
                            root.settingsReturnPage = "practice"
                            root.page = "settings"
                        }
                    }
                    Button {
                        text: "Changer de mode"
                        flat: true
                        onClicked: appBridge.returnToModeChoice()
                    }
                }

                Label {
                    visible: appBridge.questionTotal === 0 && appBridge.feedback !== ""
                    text: appBridge.feedback
                    color: "#B45309"
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }

                ColumnLayout {
                    visible: appBridge.questionTotal === 0
                    Layout.fillWidth: true
                    spacing: 12
                    Label { text: "Compétence"; color: "#33445D"; font.pixelSize: 15; font.weight: Font.DemiBold }
                    ComboBox {
                        id: skillSelect
                        Layout.fillWidth: true
                        implicitHeight: 48
                        textRole: "label"
                        valueRole: "value"
                        model: [
                            { label: "CP · Additions jusqu'à 20", value: "cp.addition_20" },
                            { label: "CP · Soustractions jusqu'à 20", value: "cp.subtraction_20" },
                            { label: "CE1 · Additions jusqu'à 100", value: "ce1.addition_100" },
                            { label: "CE1 · Soustractions jusqu'à 100", value: "ce1.subtraction_100" },
                            { label: "CE2 · Additions jusqu'à 1 000", value: "ce2.addition_1000" },
                            { label: "CE2 · Tables de multiplication", value: "ce2.multiplication_tables" },
                            { label: "CM1 · Multiplications", value: "cm1.multiplication" },
                            { label: "CM2 · Divisions exactes", value: "cm2.division_exact" },
                            { label: "5e · Addition de nombres relatifs", value: "college.signed_addition" },
                            { label: "4e · Multiplication de nombres relatifs", value: "college.signed_multiplication" }
                        ]
                    }
                    Label { text: "Nombre de questions"; color: "#33445D"; font.pixelSize: 15; font.weight: Font.DemiBold }
                    SpinBox {
                        id: countSelect
                        from: 5
                        to: 30
                        value: 10
                        editable: true
                        implicitHeight: 48
                    }
                    Label { text: "Difficulté"; color: "#33445D"; font.pixelSize: 15; font.weight: Font.DemiBold }
                    ComboBox {
                        id: difficultySelect
                        Layout.fillWidth: true
                        implicitHeight: 48
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
                    PrimaryButton {
                        text: "Lancer l'entraînement"
                        Layout.fillWidth: true
                        Layout.topMargin: 8
                        onClicked: appBridge.startPractice(skillSelect.currentValue, countSelect.value, difficultySelect.currentValue)
                    }
                }

                ColumnLayout {
                    visible: appBridge.questionTotal > 0 && !appBridge.practiceFinished
                    Layout.fillWidth: true
                    spacing: 18
                    Label {
                        text: "Question " + appBridge.questionNumber + " / " + appBridge.questionTotal
                        color: "#66768E"
                        font.pixelSize: 15
                        Layout.alignment: Qt.AlignHCenter
                    }
                    Rectangle {
                        Layout.fillWidth: true
                        height: 8
                        radius: 4
                        color: "#E3EAF4"
                        Rectangle {
                            width: parent.width * appBridge.questionNumber / Math.max(1, appBridge.questionTotal)
                            height: parent.height
                            radius: 4
                            color: "#1769D2"
                        }
                    }
                    Label {
                        text: appBridge.questionPrompt
                        color: "#172A45"
                        font.pixelSize: 42
                        font.weight: Font.Bold
                        Layout.alignment: Qt.AlignHCenter
                        Layout.topMargin: 20
                    }
                    TextField {
                        id: answerInput
                        Layout.fillWidth: true
                        implicitHeight: 58
                        enabled: !appBridge.answerSubmitted
                        placeholderText: "Votre réponse"
                        horizontalAlignment: TextInput.AlignHCenter
                        font.pixelSize: 23
                        onAccepted: if (!appBridge.answerSubmitted) appBridge.submitAnswer(text)
                    }
                    Label {
                        visible: appBridge.answerSubmitted
                        text: appBridge.feedback
                        color: appBridge.feedback === "Bonne réponse !" ? "#16804A" : "#B45309"
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignHCenter
                    }
                    PrimaryButton {
                        visible: !appBridge.answerSubmitted
                        text: "Valider"
                        Layout.fillWidth: true
                        onClicked: appBridge.submitAnswer(answerInput.text)
                    }
                    PrimaryButton {
                        visible: appBridge.answerSubmitted
                        text: appBridge.questionNumber === appBridge.questionTotal ? "Voir le résultat" : "Question suivante"
                        Layout.fillWidth: true
                        onClicked: {
                            answerInput.text = ""
                            appBridge.nextQuestion()
                        }
                    }
                }

                ColumnLayout {
                    visible: appBridge.practiceFinished
                    Layout.fillWidth: true
                    spacing: 16
                    Label {
                        text: "Séance terminée"
                        color: "#172A45"
                        font.pixelSize: 32
                        font.weight: Font.Bold
                        Layout.alignment: Qt.AlignHCenter
                    }
                    Label {
                        text: appBridge.scoreText
                        color: "#1769D2"
                        font.pixelSize: 23
                        font.weight: Font.DemiBold
                        Layout.alignment: Qt.AlignHCenter
                    }
                    PrimaryButton {
                        text: root.currentMode === "classroom" ? "Retour à l'espace élève" : "Retour à l'espace individuel"
                        Layout.fillWidth: true
                        onClicked: {
                            appBridge.abandonPractice()
                            root.page = root.currentMode === "classroom" ? "area" : "home"
                        }
                    }
                }

                Button {
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

        Item {
            ScrollView {
                anchors.fill: parent
                contentWidth: availableWidth
                ColumnLayout {
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: Math.min(parent.width, 660)
                    spacing: 16

                    Label {
                    text: "Paramètres"
                    color: "#172A45"
                    font.pixelSize: 32
                    font.weight: Font.Bold
                    Layout.alignment: Qt.AlignHCenter
                }
                Label { text: "Accessibilité"; color: "#1769D2"; font.pixelSize: 18; font.weight: Font.DemiBold }
                Label { text: "Taille de l'interface · " + Math.round(appBridge.uiScale * 100) + "%"; color: "#33445D"; font.pixelSize: 15 }
                Slider {
                    id: scaleSlider
                    Layout.fillWidth: true
                    from: 0.85
                    to: 1.25
                    stepSize: 0.05
                    value: appBridge.uiScale
                    onMoved: appBridge.setUiScale(value)
                }
                CheckBox {
                    text: "Contraste renforcé"
                    checked: appBridge.highContrast
                    onToggled: appBridge.setHighContrast(checked)
                }
                CheckBox {
                    text: "Réduire les animations"
                    checked: appBridge.reduceMotion
                    onToggled: appBridge.setReduceMotion(checked)
                }
                Label { text: "Données"; color: "#1769D2"; font.pixelSize: 18; font.weight: Font.DemiBold; Layout.topMargin: 8 }
                GridLayout {
                    columns: 2
                    columnSpacing: 12
                    rowSpacing: 10
                    PrimaryButton {
                        text: "Créer une sauvegarde"
                        Layout.fillWidth: true
                        onClicked: appBridge.createBackup()
                    }
                    PrimaryButton {
                        text: "Exporter en JSON"
                        Layout.fillWidth: true
                        onClicked: exportDialog.open()
                    }
                    PrimaryButton {
                        text: "Importer un export"
                        Layout.fillWidth: true
                        onClicked: importDialog.open()
                    }
                    PrimaryButton {
                        text: "Restaurer une sauvegarde"
                        Layout.fillWidth: true
                        onClicked: restoreDialog.open()
                    }
                }
                Button {
                    text: "Réinitialiser toutes les données"
                    flat: true
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: resetConfirmation.open()
                }
                Label {
                    visible: appBridge.dataMessage !== ""
                    text: appBridge.dataMessage
                    color: "#1769D2"
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
        standardButtons: Dialog.Yes | Dialog.No
        anchors.centerIn: parent
        Label {
            text: "L'élément ne sera plus proposé dans les listes actives. Les résultats et l'historique associés seront conservés."
            wrapMode: Text.WordWrap
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
        standardButtons: Dialog.Yes | Dialog.No
        anchors.centerIn: parent
        Label {
            text: "Toutes les classes, tous les profils, les réglages et l'historique Phoenix seront supprimés. Une sauvegarde de sécurité sera créée avant l'opération."
            wrapMode: Text.WordWrap
        }
        onAccepted: appBridge.resetData()
    }
}
