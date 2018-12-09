# What it does
This python code will take multiple files containing key value pairs and make a directed graph out of them. The ultimate goal of this is to make a dynamic dependency chart that can be used to determine what is affected by or what will be affected by a change in a node of the diagram (for example to be used when planning IT maintenence)

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

# Development environment
Python 3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:54:40) [MSC v.1900 64 bit (AMD64)] on win32