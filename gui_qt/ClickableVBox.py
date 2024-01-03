from PyQt5.QtWidgets import QVBoxLayout


class ClickableVBoxLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(ClickableVBoxLayout, self).__init__(parent)

    def mousePressEvent(self, event, *args, **kwargs):
        self.parentWidget().setFocus()  # Set focus to the parent widget when the layout is clicked
        super(ClickableVBoxLayout, self).mousePressEvent(event, *args, **kwargs)