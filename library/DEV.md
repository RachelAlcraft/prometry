# prometry
A library for calculating protein geometry paramaters with searching based on criteria.

# Package structure
https://packaging.python.org/en/latest/tutorials/packaging-projects/

# Testing
https://realpython.com/pytest-python-testing/

# Use the .libenv, from the library dir
```python3 -m venv .libenv```
```source .libenv/bin/activate``` (deactivate to exit venv)
Then navigate to library to install
# Load dev environment
```pip install --upgrade pip```
```pip install -r requirements.txt --upgrade```  

This means that libs for the library need to be also put in the app requirements, such as build and wheel

# release to pypi
Increment the version in setup.cfg in the project IMPORTANT  
```python -m build```  
```python -m twine upload --repository pypi dist/*```  
The credentials are stored in a settings file  
Check success https://pypi.org/manage/projects/  