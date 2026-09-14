import QtQuick
import Quickshell.Wayland
import qs.Commons
import qs.Ui

BarWidget {
    id: root
    moduleName: "local.familiar-tasks"
    readonly property var windows: ToplevelManager.toplevels.values
    // A bounded, scrollable strip keeps every window reachable without
    // consuming the system tray. Vertical bars use one-letter buttons.
    implicitWidth: vertical ? barSize : Math.min(420, windows.length * 140)
    implicitHeight: vertical ? Math.min(280, windows.length * barSize) : barSize
    visible: windows.length > 0

    ListView {
        id: tasks
        anchors.fill: parent
        clip: true
        orientation: root.vertical ? ListView.Vertical : ListView.Horizontal
        boundsBehavior: Flickable.StopAtBounds
        model: root.windows
        spacing: 2

        delegate: WidgetButton {
            id: task
            required property var modelData
            required property int index
            readonly property string windowTitle: modelData ? (modelData.title || modelData.appId || "Window") : "Window"
            bar: root.bar
            fixedWidth: root.vertical ? root.barSize : 138
            fixedHeight: root.barSize
            width: implicitWidth
            height: implicitHeight
            labelVisible: false
            hasVisualContent: true
            tooltipText: windowTitle
            activeFocusOnTab: true
            Accessible.role: Accessible.Button
            Accessible.name: windowTitle
            Accessible.onPressAction: if (modelData) modelData.activate()
            onPressed: function(button) {
                if (button === Qt.LeftButton && modelData) modelData.activate()
            }
            Keys.onReturnPressed: if (modelData) modelData.activate()
            Keys.onSpacePressed: if (modelData) modelData.activate()
            onActiveFocusChanged: if (activeFocus) tasks.positionViewAtIndex(index, ListView.Contain)
            onWheelMoved: function(delta) {
                if (root.vertical)
                    tasks.contentY = Math.max(0, Math.min(Math.max(0, tasks.contentHeight - tasks.height), tasks.contentY - delta));
                else
                    tasks.contentX = Math.max(0, Math.min(Math.max(0, tasks.contentWidth - tasks.width), tasks.contentX - delta));
            }
            Rectangle {
                anchors.fill: parent
                color: task.foreground
                opacity: task.tooltipHovered || task.activeFocus ? 0.18 : (task.modelData && task.modelData.activated ? 0.10 : 0)
            }
            Rectangle {
                anchors.fill: parent
                color: "transparent"
                border.color: task.foreground
                border.width: task.activeFocus ? 2 : 0
            }
            Text {
                anchors.fill: parent
                anchors.margins: 10
                textFormat: Text.PlainText
                text: root.vertical ? task.windowTitle.charAt(0).toUpperCase() : task.windowTitle
                color: task.foreground
                font.family: task.fontFamily
                font.pixelSize: task.fontSize
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }
            Rectangle {
                anchors.bottom: parent.bottom
                width: parent.width
                height: 3
                color: task.foreground
                visible: task.modelData ? task.modelData.activated : false
            }
        }
    }
}
