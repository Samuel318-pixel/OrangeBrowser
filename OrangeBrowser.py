from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTabWidget, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys

class FancyBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyperPolished Browser")
        self.setGeometry(100, 100, 1300, 900)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top bar com estilo
        self.top_bar = QHBoxLayout()
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("⟳")
        self.url_input = QLineEdit()
        self.go_btn = QPushButton("Go")
        self.new_tab_btn = QPushButton("+")
        for btn in [self.back_btn, self.forward_btn, self.reload_btn, self.go_btn, self.new_tab_btn]:
            btn.setStyleSheet("padding:8px; border-radius:5px; background:orange; color:white; font-weight:bold;")
        self.url_input.setStyleSheet("padding:8px; border-radius:5px; border: 1px solid gray;")
        self.top_bar.addWidget(self.back_btn)
        self.top_bar.addWidget(self.forward_btn)
        self.top_bar.addWidget(self.reload_btn)
        self.top_bar.addWidget(self.url_input, 1)
        self.top_bar.addWidget(self.go_btn)
        self.top_bar.addWidget(self.new_tab_btn)
        self.layout.addLayout(self.top_bar)

        # Abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.layout.addWidget(self.tabs)

        # Abrir primeira aba (tela inicial Google)
        self.add_new_tab("https://www.google.com", "Google")

        # Conexões
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.back_btn.clicked.connect(self.go_back)
        self.forward_btn.clicked.connect(self.go_forward)
        self.reload_btn.clicked.connect(self.reload_page)
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab("https://www.google.com", "Nova Aba"))

    def add_new_tab(self, url, title="Nova Aba"):
        webview = QWebEngineView()
        webview.setUrl(QUrl(url))
        index = self.tabs.addTab(webview, title)
        self.tabs.setCurrentIndex(index)
        webview.urlChanged.connect(lambda qurl, tab=webview: self.update_url_input(qurl, tab))
        webview.loadFinished.connect(lambda ok, tab=webview: self.update_tab_title(tab))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_webview(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        url = self.url_input.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.current_webview().setUrl(QUrl(url))

    def go_back(self):
        self.current_webview().back()

    def go_forward(self):
        self.current_webview().forward()

    def reload_page(self):
        self.current_webview().reload()

    def update_url_input(self, qurl, webview):
        if webview == self.current_webview():
            self.url_input.setText(qurl.toString())

    def update_tab_title(self, webview):
        index = self.tabs.indexOf(webview)
        if index != -1:
            self.tabs.setTabText(index, webview.page().title())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = FancyBrowser()
    browser.show()
    sys.exit(app.exec())