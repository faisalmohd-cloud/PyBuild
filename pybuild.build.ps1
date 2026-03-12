pyinstaller pybuild\main.py `
    --name=pybuild `
    --icon=resources\pybuild.ico `
    --noconfirm `
    --collect-all rich `
    --collect-all typer `
    --collect-all markdown_it `
    --collect-all mdurl `
    --collect-all pygments
