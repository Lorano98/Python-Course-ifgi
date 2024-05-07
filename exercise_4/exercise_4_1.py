from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

view = QWebView()

url = "https://de.wikipedia.org/wiki/[%Name%]"

view.load(QUrl(url))
view.show()