# prometry
A library for calculating protein geometry paramaters with searching based on criteria.

# Package structure
https://packaging.python.org/en/latest/tutorials/packaging-projects/

# Testing
https://realpython.com/pytest-python-testing/

# Create dev environment
```python3 -m venv .venv```

# Load dev environment
source .venv/bin/activate  
```pip install --upgrade pip```  
```pip install -r requirements.txt --upgrade```  

# release to pypi
Increment the version in setup.cfg in the project IMPORTANT  
```python -m build```  
```python -m twine upload --repository pypi dist/*```  
The credentials are stored in a settings file  
Check success https://pypi.org/manage/projects/  