PROTOTYPE
=========

This code is not thougth to be final. Efficiency, arquitechture and code structure should be improved.

## Researching about musical entities conciliation

* Target: prototype able to recognize dirty/heterogeneus (civil names, artistic names, alias) strings as entities (groups, songs, artists, releases,...).

* Content: The different packages contain executable scripts in python doing the task related with the package's name but most of them are based in private files non included in this repo. Those scripts are called main.py or main_*.py

* Collaborators: [Dani Fernández](https://github.com/DaniFdezAlvarez), [Dani Gayo](https://github.com/danigayo), [José Labra](https://github.com/labra).


The code is organized as follows:

* Package wmera: Main package. It contains the code of the entity reconciliatory and the modules involved in that process.
  * Sub-package adapters: conversion between different implementations of q-gram indexes.
  *	Sub-package controller: code to coordinate query execution with result retrieving.
  *	Sub-package graph_gen: code to generate RDF graphs through consuming an interface of a parser that yields model objects. It also contains an implementation of MERA’s graph interface using RDFLib library.
  *	Sub-package infrastructure: interface and implementations of the different q-gram indexes.
  *	Sub-package parsers: interface of parsers that generate model objects as well as implementations to generate objects of different datasources.
  *	Sub-package query_gen: code to generate serialized MERA queries in a JSON model and after parsing another JSON model.
  *	Sub-package mera_core: model objects, system interfaces, matching module and string comparison packages.
  *	Module facade:  code to consume MERA from external apps.
  *	Module factory: code to build some specific complex objects.
  *	Module utils. Different utility methods.
  *	Module word_utild: different utility methods focused in strings.
* Package apps: scripts that use somehow wmera code: research experiments, graph generation, comparison of tehcniques…
* Package test: testing code for wmera. Most of these test are integration test, and they expect to be executed in a machine running an instance of MongoDB accessible at localhost:27017.


