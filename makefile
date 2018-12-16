# If the first argument is "run"...
# WIP...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif


THIS_FILE := $(lastword $(MAKEFILE_LIST))


git_username="Charles Watkins"
git_email="charles@titandws.com"

.DEFAULT: help

help:
	@echo "make build          | build python files and make pypi package"
	@echo "make bump           | bump the package version"
	@echo "make clean          | delete temp build files"
	@echo "make init           | init git, create base directories"
	@echo "make install        | install the latest flextable from pypi in your user directory"
	@echo "make pipfile        | recreate the pipfile"
	@echo "make upload         | upload any build packages to pypi"
	@echo "make uninstall      | uninstall ddb from your user directory"
	

clean:
	@find . -type f -name "*.c" -exec rm -f {} \;
	@find . -type f -name "*.so" -exec rm -f {} \;
	@find . -type f -name "*.pyc" -exec rm -f {} \;


init:
	@echo dependencies for building...  dnf install python-devel libyaml-devel gcc make
	@if [[ ! -d 'dist' ]]; then  mkdir dist ; fi
	@if [[ ! -d '.git' ]]; then  git init; fi
	@git config --global user.email $(git_email)
	@git config --global user.name $(git_username)
	# bumpversion
	# twine
	# and other deps should be in the pipfile
	@pipenv install 
	
	@echo [bumpversion]>.bumpversion.cfg
	@echo current_version = $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'")>>.bumpversion.cfg
	@echo files = setup.py>S>.bumpversion.cfg
	@echo commit = False>>.bumpversion.cfg
	@echo tag = False>>.bumpversion.cfg

pipfile:
	pipenv install bumpversion --dev
	pipenv install twine --dev
	pipenv install flake8 --dev
	

bump:
	@pipenv run bumpversion patch --allow-dirty
	@git add -A 
	@git commit -m 'Bump Version $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'"))'
	
build: bump 
	@find dist -type f -name "*.gz" -exec rm -f {} \;
	@pipenv run python setup.py build_ext --inplace sdist 


upload:
	@pipenv run twine upload  dist/*.gz

install:
	pip install flextable --user

uninstall:
	pip uninstall flextable

