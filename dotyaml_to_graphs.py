"""usage: dotyaml_to_graphs.py 
							[-h] 
							[--extension <EXTENSION>]
                            [--graphformat <GRAPHFORMAT>]
                            [--logging_level <LOGGING_LEVEL>]
                            [--source_path <SOURCE_PATH>]
                            [--output_path <OUTPUT_PATH>]
                            [--add_graph_filename_as_cluster_node]
                            [--esep <int>]
                            [--ranksep <int>]
                            [--rankdir <DIRECTION>]

optional arguments:
  -h, --help            show this help message and exit
  --extension <EXTENSION>, -e <EXTENSION>
                        The extension of the files to load and create graphs from. Ex, '.dotyaml' [default: .dotyaml]
  --graphformat <GRAPHFORMAT>, -g <GRAPHFORMAT>
                        The output format of the graph. ex, 'png' [default: png]
  --logging_level <LOGGING_LEVEL>, -l <LOGGING_LEVEL>
                        valid options are 'Debug','Info','Warning','Error','Critical' [default: info]
  --source_path <SOURCE_PATH>, -s <SOURCE_PATH>
                        What path to use as the root for a recursive search for files matching the --extension parameter. Defaults to current working directory.
  --output_path <OUTPUT_PATH>, -o <OUTPUT_PATH>
                        What path to use as the output directory. Defaults to current working directory.
  --esep <int>
                        Area around nodes to not put edges [default: 5]
  --ranksep <int>
                        Vertical distance between rows of nodes  [default: 5]
  --rankdir <DIRECTION>
                        Which way to direct the graph.
						Valid options are 'TB', 'BT', 'LR', 'RL' [default: TB]
  --add_graph_filename_as_cluster_node
  						This switch adds a node with the same name as the filename that contained the YAML for a graph as a top level node in that file's resulting graph.
"""

try:
	import os
	import logging
	import argparse
	import docopt
	
	import graphviz

	import local_functions
except:
	raise Exception("Could not load required python libraries")

#Assign names to the arg dict for easy readability later.
args = docopt.docopt(__doc__)
graphformat = args.get('--graphformat')
logging_level = args.get('--logging_level')
extension = args.get('--extension')
source_path = args.get('--source_path')
output_path = args.get('--output_path')
edge_seperation = args.get('--esep')
rank_seperation = args.get('--ranksep')
graph_direction = args.get('--rankdir')
add_graph_filename_as_cluster_node = args.get('--add_graph_filename_as_cluster_node')

#Set logging options.
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logging_level = logging_level.upper()
loglevels = {
    'CRITICAL' : logging.CRITICAL,
    'ERROR' : logging.ERROR,
    'WARNING' : logging.WARNING,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG
}
level = loglevels[logging_level]
logger.setLevel(level)

def main():

	logger.debug(args)
	
	#mastergraph has each filegraph added to it to later be thrown into a mastergraph
	mastergraph = graphviz.Digraph(format=graphformat)
	#move attr set to somewhere better
	mastergraph.attr('node', shape='box')
	mastergraph.attr('graph', splines='polyline') #how to draw edges
	mastergraph.attr('graph', esep=f'{edge_seperation}') #area around nodes to not put edges
	mastergraph.attr('graph', ranksep=f'{rank_seperation}') #vertical distance between rows of nodes 
	mastergraph.attr('graph', rankdir=f'{graph_direction}') #vertical distance between rows of nodes 

	logger.info(f'Loading files into dictionary format and converting to individual graphs.')
	filelist = local_functions.get_files_by_extension(extension, source_path)
	for file_path in filelist:		
		
		filename = local_functions.filename_from_filepath(file_path)
		file_as_list = local_functions.filepath_to_list (file_path)
		logger.debug(f'input is {file_as_list}')
				
		fileGraph = graphviz.Digraph(format=graphformat)
		#creating a subgraph to be put in the filegraph so that when we merge many filegraphs in the mastergraph the filegraphs are kept together.
		fileSubGraph = graphviz.Digraph(format=graphformat)
		#move attr set to somewhere better
		fileSubGraph.attr('node', shape='box')
		

		fileSubGraph = local_functions.graphviz_graph_add_cluster(fileSubGraph, filename, file_as_list, add_graph_filename_as_cluster_node)
		fileSubGraph = local_functions.graphviz_graph_add_edges(fileSubGraph, filename, file_as_list, add_graph_filename_as_cluster_node)
		logger.debug(fileSubGraph)
		
		fileGraph.subgraph(fileSubGraph)
		local_functions.graphviz_graph_render(fileGraph, filename, output_path)

		logger.info(f'Adding graph to mastergraph')
		mastergraph.subgraph(fileGraph)
	local_functions.graphviz_graph_render(mastergraph, 'mastergraph', output_path)

if __name__ == "__main__":
	main()