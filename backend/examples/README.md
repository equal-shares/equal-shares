To run the examples in this folder (for development & research) do:

* Install Python 3.12; 
* Create and activate a virtual environment;
* Install poetry 1.7.1;
* Run:

```
cd backend
poetry config virtualenvs.create false
poetry install
pip install -e .
```

Then you should be able to run
```
python examples/run_small_examples.py
```
