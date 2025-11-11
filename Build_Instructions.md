### Create virtual enviroment

Create virtual env
- python -m venv venv

Activate virtual env
- . venv/bin/activate (Linux) or ./venv/Scripts/activate (Win)

Deactivate virtual env
- deactivate (Linux)

### pip install project

In the root directory, run

- pip install -r requirements.txt

If you want to build the distributable executable (recommended to do in a
separate build environment), install the build tools from `requirements-dev.txt`:

- python -m pip install -r requirements-dev.txt

### make exe
 Run:
 - & .\venv\Scripts\pyinstaller.exe Room25.spec

Alternative (invokes PyInstaller via the venv's python - safer if activation
is blocked by PowerShell policy):

```powershell
.\venv\Scripts\python.exe -m PyInstaller Room25.spec
```