# What it does
This script recursively searches for files (default .dotyaml) under a directory (defaults to current directory) and generates a composite graph from those files through GraphViz. The ultimate goal of this is to make a dynamic dependency chart that can be used to determine what is affected by or what will be affected by a change in a node of the diagram (for example to be used when planning IT maintenence).

This is done from multiple files containing key value pairs.

Possible overloads include graphing family trees, and allowing the tree to be isolated to a single person's lineage.

# Requirements  
Python v3.6  
(see contents of [requirements.txt](requirements.txt))

## Installing required libaries  
`pip install -r requirements.txt`

# Usage
`py dotyaml_to_graphs.py --source input/`

## Source file contents
Source files should be raw text files with "key : value" content, with as many lines as desired.


```
Key1 : Key2
Key2 : "Key 3"
```

See example files in the 'input' directory

# TODO
0. Don't duplicate edges when multiple files (parent and child, etc.) define the same edge.  

In no particular order,  
* Convert graphviz_graph_* in [local_functions.py](local_functions.py) to class(es).
* Should this output subgraphs to the same place we found the source?
	* Should this even output subgraphs?
* Figure out how to get an init function setup such that variables and stuff survive the init's scope destruction.
* How to return only paths that include a selected node?


# Development environment
Python 3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:54:40) [MSC v.1900 64 bit (AMD64)] on win32