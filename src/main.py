import webbrowser
import gui.gui as gui

def execute_main():
    webbrowser.open_new("http://127.0.0.1:5000/")
    gui.app.run()

if __name__ == "__main__":
    execute_main()