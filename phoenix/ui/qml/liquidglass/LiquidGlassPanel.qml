// LiquidGlassPanel.qml - Display box/card/dialog surface
// Features: header + content + optional footer with glass material

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    
    // ============================================================
    // Public Properties
    // ============================================================
    
    // Source item for background blur
    property Item backgroundSource: null
    
    // Panel content
    property string title: ""
    property string subtitle: ""
    property bool showHeader: title !== "" || subtitle !== ""
    property bool showFooter: false
    
    // Footer content (buttons, actions)
    property alias footerContent: footerContainer.data
    
    // Main content
    default property alias content: contentContainer.data
    
    // Material overrides
    property real cornerRadius: Tokens.cornerRadius * 1.5
    property real blurRadius: Tokens.effectiveBlurRadius
    property real baseOpacity: Tokens.effectiveOpacity
    property color tintColor: Tokens.tintColor
    property real highlightIntensity: Tokens.effectiveHighlightIntensity
    property real elevation: Tokens.elevation * 1.5
    
    // Padding
    property real headerPadding: 20
    property real contentPadding: 20
    property real footerPadding: 16
    
    // Accessibility
    Accessible.role: Accessible.Pane
    Accessible.name: title !== "" ? title : "Glass panel"
    
    // Default size
    implicitWidth: 320
    implicitHeight: headerSection.height + contentSection.height + 
                   (showFooter ? footerSection.height : 0)
    
    // Interactive state for subtle effects
    property bool _hovered: panelHoverHandler.hovered
    property point _pointerPos: Qt.point(width / 2, height / 2)
    
    HoverHandler {
        id: panelHoverHandler
        onPointChanged: {
            if (hovered) {
                root._pointerPos = Qt.point(point.position.x, point.position.y)
            }
        }
    }
    
    // ============================================================
    // Main Glass Surface
    // ============================================================
    
    LiquidGlassSurface {
        id: glassSurface
        anchors.fill: parent
        backgroundSource: root.backgroundSource
        cornerRadius: root.cornerRadius
        blurRadius: root.blurRadius
        baseOpacity: root.baseOpacity
        tintColor: root.tintColor
        highlightIntensity: root.highlightIntensity + (_hovered ? 0.1 : 0)
        elevation: root.elevation
        hovered: root._hovered
        pointerPosition: root._pointerPos
        
        // ============================================================
        // Panel Layout
        // ============================================================
        
        ColumnLayout {
            anchors.fill: parent
            spacing: 0
            
            // ========================================================
            // Header Section
            // ========================================================
            
            Item {
                id: headerSection
                Layout.fillWidth: true
                Layout.preferredHeight: showHeader ? headerContent.height + headerPadding * 2 : 0
                visible: showHeader
                
                ColumnLayout {
                    id: headerContent
                    anchors {
                        left: parent.left
                        right: parent.right
                        top: parent.top
                        margins: headerPadding
                    }
                    spacing: 4
                    
                    // Title
                    Text {
                        id: titleText
                        Layout.fillWidth: true
                        text: root.title
                        color: Tokens.textPrimary
                        font.pixelSize: 18
                        font.weight: Font.DemiBold
                        visible: root.title !== ""
                        elide: Text.ElideRight
                        
                        Accessible.role: Accessible.Heading
                        Accessible.name: root.title
                    }
                    
                    // Subtitle
                    Text {
                        id: subtitleText
                        Layout.fillWidth: true
                        text: root.subtitle
                        color: Tokens.textSecondary
                        font.pixelSize: 13
                        visible: root.subtitle !== ""
                        elide: Text.ElideRight
                        wrapMode: Text.WordWrap
                        maximumLineCount: 2
                    }
                }
                
                // Header separator
                Rectangle {
                    anchors {
                        left: parent.left
                        right: parent.right
                        bottom: parent.bottom
                        leftMargin: headerPadding
                        rightMargin: headerPadding
                    }
                    height: 1
                    color: Qt.rgba(1, 1, 1, 0.1)
                    visible: showHeader
                }
            }
            
            // ========================================================
            // Content Section
            // ========================================================
            
            Item {
                id: contentSection
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumHeight: 60
                
                Item {
                    id: contentContainer
                    anchors {
                        fill: parent
                        margins: contentPadding
                    }
                }
            }
            
            // ========================================================
            // Footer Section
            // ========================================================
            
            Item {
                id: footerSection
                Layout.fillWidth: true
                Layout.preferredHeight: showFooter ? footerRow.height + footerPadding * 2 : 0
                visible: showFooter
                
                // Footer separator
                Rectangle {
                    anchors {
                        left: parent.left
                        right: parent.right
                        top: parent.top
                        leftMargin: footerPadding
                        rightMargin: footerPadding
                    }
                    height: 1
                    color: Qt.rgba(1, 1, 1, 0.1)
                }
                
                Row {
                    id: footerRow
                    anchors {
                        right: parent.right
                        bottom: parent.bottom
                        margins: footerPadding
                    }
                    spacing: 12
                    layoutDirection: Qt.RightToLeft
                    
                    Item {
                        id: footerContainer
                        width: childrenRect.width
                        height: childrenRect.height
                    }
                }
            }
        }
    }
    
    // ============================================================
    // Entrance Animation
    // ============================================================
    
    property bool _animateIn: false
    
    Component.onCompleted: {
        _animateIn = true
    }
    
    opacity: _animateIn ? 1.0 : 0.0
    scale: _animateIn ? 1.0 : 0.95
    
    Behavior on opacity {
        NumberAnimation {
            duration: Tokens.durationSlow
            easing.type: Tokens.easingEnter
        }
    }
    
    Behavior on scale {
        NumberAnimation {
            duration: Tokens.durationSlow
            easing.type: Tokens.easingBounce
        }
    }
}
