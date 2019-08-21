
# Tango icon theme for PyQt

### Build

generate a PyQt resource file

    make install
    make build

### Usage

copy the output tango.py file into your project

    from . import tango

    def main():
        app = QApplication(sys.argv)

        QIcon.setThemeName("tango")

        icon = QIcon.fromTheme("edit-copy")