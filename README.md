wMERA
=====

* Collaborators: [Dani Fernández](https://github.com/DaniFdezAlvarez), [Dani Gayo](https://github.com/danigayo), [José Labra](https://github.com/labra).


MERA (Musical Entities Reconciliation Architecture) consist of an architecture highly configurable designed to link music-related datasuources using string comparison techniques and semantic technologies. wMERA is a prototype that implements most of MERA's features, including:
•	Graph navigation exploring alternative forms for each entity.
•	Graph navigation exploring related entities.
•	Configuration of relevancies when applying refinements to a query.
•	Configuration of minimum acceptable values for each type when scoring a result.
•	Blocking function: adaptation of q-gram indexing and TF-IDF.
•	Usage of MERA rdf graph schema
•	Set of comparison algorithms of general-purpose.
•	Set of text standardization functions.


wMERA has been developed in python 2.7 and requires the next packages:
 * rdflib
 * pymongo


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


Documentation of MERA and wMERA are still in progress. Contact with [Dani Fernández](https://github.com/DaniFdezAlvarez) for any question.
