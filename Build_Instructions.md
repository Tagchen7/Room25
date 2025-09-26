### Create virtual enviroment

Create virtual env
- python -m venv venv

Activate virtual env
- . venv/bin/activate (Linux) or ./venv/Scripts/activate (Win)

Deactivate virtual env
- deactivate (Linux)

### pip install project

In the root directory, run

- pip install -e . (note the dot, it stands for "current directory")
  - pip install hatchling(chosen build system) if build-system is missing