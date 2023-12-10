## Description
A simple project that pulls down a wikipedia page, parses it, attaches additional data from linked pages, and returns a dataset in a format friendlier to an analyst or data scientist.

### Repo Structure
- ```/``` project root contains invocation scripts, build configurations, and docker resources.
- ```/src``` is the source root for the project and contains the ```museum_parser``` package
- ```/tests``` attendant tests (using the ```pytest``` framework)
- ```/workspace``` is the local storage backing the docker container in which Jupyter is running - allowing for the persistence of notebooks and data across runs. Data from the parser job is written to ```/workspace/data```

## Quickstart
```
docker compose up
```

Running this will launch two containers:
- A python environment that will run the ```run_pkg.py``` script to completion
- A Jupyter Lab environment with access to CSVs exported by the python container and configured to use the parsing package from within notebooks.

If the docker compose is not run in detached mode, the progress of the parser can be observed.  This is useful, as The parsing process is comparatively slow (~5 min. anecdotally), due to it recusively crawling Wikipedia pages to collect enrichment data. 

## Working in a Container
Individual containers for both the parser script, and for Jupyter Lab can be built from the corresponding dockerfiles:
- ```parser.dockerfile```
- ```jupyter.dockerfile```

Alternately they can be laumched with docker compose as outlined above.

### Parser Container
The parser container runs the ```run_pkg.py``` script immediately on creation, and terminates when the script completes.  The CSV generated by this job will be written to ```/workspace/data``` which is exposed inside of the Jupyter container.

### Jupyter Container
Access the Jupyter container from the URL it provides in the standard output of the container start up process.  A sample workbook containing a simple linear regression is provided in the ```workspace/notebooks``` directory, and sample data provided in the ```workspace/data``` folder.  (This is useful if you don't want to wait for the psrser container to download a new CSV.)

The ```museum_parser``` package can be imported into a Jupyter notebook.  In general, there would be little reason to import anything beyond the core 'parser' module.

```
from museum_parser import parser
```

Access to the 'enricher' module and 'Museum' dataclass is possible if required / of interest:
```
from museum_parser.utils.museum import Museum 
from museum_parser import enricher
```

## Working Locally

NOTE: This code has been tested and run in a Python 3.10.x environment. Tests with Python 3.11.x suggested that there may be breaking changes in the way that dataclasses and regex are handled. Both Dockerfiles build on Python 3.10.x images, and as such, if you wish to build for another version of Python, you may need to adjust the Dockerfiles accordingly.

### requirements and requirements_venv
The ```requirements.txt``` provided in the projet root is used to configure the Python environment for both containers.  
The ```requirements_venv.text``` is intended for configuration of your local (virtual) environment.  (It is nearly identical to the requirements file but omits the project wheel and adds build and pytest.)

### Building and Testing
The ```museum_parser``` package can be built from the project root with the standard ```python -m build```. This will generate a wheel and a tarball in the ```/build``` directory.  Subsequently, the wheel can be installed with the following pip command: ```python -m pip install dist/museum_parser-0.0.1-py3-none-any.whl```

Likewise, the tests can be run from the project root with ```pytest```.

### Invoking the Module Directly
The script module can be installed and its methods invoked as presented in ```run_pkg.py```.  Alternately, the source can be imported directly and its methods invoked as presented in ```run_src.py```.
