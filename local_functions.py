try:
	import logging
	import os
	
	import graphviz
	
except:
	raise Exception("Could not load required python libraries")

logger = logging.getLogger("__main__")
	
def filename_from_filepath (path):
	"""given a filepath, return only the name of the file, without extensions"""
	file_fullpath = os.path.basename(path)
	path_elements = os.path.splitext(file_fullpath)
	#return only the name of the file, not an array of two elements with element 0 being filename and element 1 being the file extension.
	file_name = path_elements[0]
	return file_name

def get_files_by_extension(extension, path=None):
	"""Return a list of all files (in absolute path format) that match an extension files"""
	if isinstance(path,type(None)):
		path = os.walk(os.getcwd())
	else:
		path = os.walk(path)
	logger.info(f'Getting a list of all files in {path} that are {extension} files')
	filelist = [os.path.join(root, name)
		for root, dirs, files in path
			for name in files
				if name.endswith(extension)]
	logger.info(f'Found list of all files in {path} that are {extension} files')
	logger.debug(f'filelist = {str(filelist)}')
	return filelist

def get_file_content (file_path):
	"""Get the content of a file"""
	logger.debug(f'Opening handle for {file_path}')	
	with open(file_path) as file:
		logger.debug(f'Handle opened for {file_path}')
		try:
			logger.debug(f'Reading contents of {file_path}')
			file_content = file.read()
			logger.debug(f'Finished reading contents of {file_path}:')
			logger.debug(f'file_content: {file_content}')
		except:
			raise Exception(f'could not read file {file_path}')
		finally:
			logger.debug(f'Closing handle for {file_path}')
			file.close()
			logger.debug(f'Handle closed for {file_path}')
	return file_content

def filepath_to_list (file_path):
	"""Get the content of a file containing with a "key : value" data structure and convert it into a list python data structure"""
	data = dict()
	current_key = ""
	file_content = get_file_content(file_path)
	for line in file_content.splitlines():
		#ignore empty lines
		if line:
			split = line.split(' : ')
			if split[0] == current_key:
				data.setdefault(split[0], [])
				data[split[0]].append(split[1])
				#data[split[0]].append(split[1])
			else:
				current_key = split[0]
				data.setdefault(split[0], [])
				data[split[0]].append(split[1])
				#data[split[0]] = split[1]
	return data
	
def graphviz_graph_create_placeholder_if_empty (graph_name, dict_object):
	"""Create placeholder values to allow parent program to run, and to provide visual clue to missing information."""
	#IMHO this is 'clever' so I'ma explain it, an empty dicitonary evaluates to false (https://docs.python.org/2/library/stdtypes.html#truth-value-testing), therfore invert that test to do things less wordy than with an else
	if not dict_object:
		logging.warning(f'Graph {graph_name} has no content. Creating placeholder values.')
		dict_object = {f'{graph_name}':f'{graph_name}_placeholder!'}
	return dict_object
	
def graphviz_graph_add_edges (source_graph, graph_name, edges_as_dict, add_graph_filename_as_cluster_node):
	"""
	Add edges to a graph from a dict object, with each key being the tail(source) and the value being the head(destination). 
	Create nodes in subgraph/cluster and edges in the parent graph, unless there is no parent graph then create the edges in the topmost graph.
	This forces the defined nodes to be in the subgraph/cluster while nodes created by proxy of being part of an edge are left in the open graph space--free to bond with nodes defined elsewhere. 
	This is to allow clusters to link properly instead of having nodes show up in the wrong cluster when rendered in the parent graph--with the logic behind wherever the edge was defined first gets nodes inside it's subgraph.
	#TODO: Is there a better way to handle the double nested "for" that sets graph_name:key as the K:V if the K isn't already a V in the dict?
	"""
	not_modifying_the_source_object_because_pythons_graphviz_library_is_bad = source_graph.copy()
	source_graph_copy = not_modifying_the_source_object_because_pythons_graphviz_library_is_bad
	logger.info(f'Adding edges to graph {graph_name}')
	edges_as_dict = graphviz_graph_create_placeholder_if_empty (graph_name, edges_as_dict)
	source_graph_copy_as_str = source_graph_copy.source
	logger.debug(f'Adding "graph_name -> node" edges for top-level nodes.')
	if add_graph_filename_as_cluster_node: 
		for key, value in edges_as_dict.items():
			if f'-> {key}\n' not in source_graph_copy_as_str and f'-> "{key}"' not in source_graph_copy_as_str: #already contains key
				logger.debug(f'{graph_name} -> {key}')
				source_graph_copy.edge(graph_name,key)
	for key, value in edges_as_dict.items():
		if isinstance(value,list):
			logger.debug(f'{key}\'s value of "{value}" was detected as a list. Adding each value in the list under the key.')
			for value_instance in value:
				logger.debug(f'{key} -> {value_instance}')
				source_graph_copy.edge(key,value_instance)
		else:
			logger.debug(f'{key} -> {value}')
			source_graph_copy.edge(key,value)
	logger.info(f'Edges added to graph {graph_name}')
	logger.debug(f'{source_graph_copy}')
	return source_graph_copy

def graphviz_graph_add_cluster (source_graph, cluter_name, nodes_as_dict, add_graph_filename_as_cluster_node):
	"""
	Add ONLY nodes to a cluster inside a graph from a dict object, with each key being a node in the graph.
	Create nodes in subgraph/cluster and edges in the parent graph, unless there is no parent graph then create the edges in the topmost graph.
	This forces the defined nodes to be in the subgraph/cluster while nodes created by proxy of being part of an edge are left in the open graph space--free to bond with nodes defined elsewhere. 
	This is to allow clusters to link properly instead of having nodes show up in the wrong cluster when rendered in the parent graph--with the logic behind wherever the edge was defined first gets nodes inside it's subgraph.
	#TODO: make this a recursive function and flip-flop between grey95 and grey70 for color.
	#TODO: move setting graph attributes to its own function.
	"""
	not_modifying_the_source_object_because_pythons_graphviz_library_is_bad = source_graph.copy()
	source_graph_copy = not_modifying_the_source_object_because_pythons_graphviz_library_is_bad
	logger.info(f'Creating cluster graph {cluter_name}')
	nodes_as_dict = graphviz_graph_create_placeholder_if_empty(cluter_name, nodes_as_dict)
	with source_graph_copy.subgraph(name=f'cluster_{cluter_name}') as cluster_graph:
		cluster_graph.attr('graph', label=f'{cluter_name}')
		cluster_graph.attr('graph', style='filled')
		cluster_graph.attr('graph', color='grey95')		
		
		logger.debug(f'Adding nodes to cluster graph {cluter_name}')
		try:
			if add_graph_filename_as_cluster_node:
				cluster_graph.node(cluter_name)
			for key, value in nodes_as_dict.items():
				logger.debug(f'Add node {key}')
				cluster_graph.node(key)
		except:
			raise Exception('Could not add nodes to graph.')
		logger.debug(f'Nodes added to cluster graph {cluter_name}')	
	logger.info(f'Cluster graph {cluter_name} created')
	logger.debug(f'{source_graph_copy}')
	return source_graph_copy

def graphviz_graph_render(graph, graph_name, output_path):
	"""
	Renders graph from a graph object.
	If output_path is not specified then the graph will be created in the current directory.
	#TODO Show some kind of progress or 'still rendering' message--possibly by getting the render to occur in a seperate thread
	#TODO add render time to logger. Not as easy as it sounds cause the logging is being a snoody little thing and not wanting to print out {timer_end - timer_start} for whatever reason.
	"""
	logger.info(f'Rendering graph {graph_name}...')
	if output_path is not None:
		logger.debug(f'output_path is None')
		filepath = os.path.join(output_path, graph_name)
		graph.render(filename=filepath)
	elif output_path is None:
		logger.debug(f'output_path is {output_path}')
		graph.render(filename=graph_name)	
	logger.info(f'Graph {graph_name} rendered.')