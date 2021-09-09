from python_graphs import program_graph, program_graph_graphviz
from python_graphs import program_graph_dataclasses as pgd
from copy import copy
import random
def seed_function(number):
    """
    seeding function to control randomness with random library.
    """
    random.seed(str(number))

seed_function(1)

class DFG_Analysis:
    def __init__(self):
        self.dfg_edge_lookup = [
            pgd.EdgeType.LAST_READ,
            pgd.EdgeType.LAST_WRITE,
            pgd.EdgeType.COMPUTED_FROM,
            pgd.EdgeType.RETURNS_TO
        ]
        self.dfg_edge_english_lookup = {
            pgd.EdgeType.LAST_READ : "last read",
            pgd.EdgeType.LAST_WRITE: "last wrote",
            pgd.EdgeType.COMPUTED_FROM: "computed from",
            pgd.EdgeType.RETURNS_TO: "returns to"
        }
        #TODO - Add Bias on Edge Type while sampling.
        self.class_sample_size = 2
    def generate_complete_dataflow_graph(self,program):
        """
        Function to generate complete data flow graph given a program
        args: 
             program (function|program_string) : Either the Program String/Function Object
        returns:
             deducted data flow graph from the complete program flow graph.
        """
        program_flow_graph = program_graph.get_program_graph(program)
        data_flow_graph  =copy(program_flow_graph)
        data_flow_graph.edges = [edge for edge in data_flow_graph.edges if edge.type in self.dfg_edge_lookup]
        return data_flow_graph
    def generate_edge_to_test(self, node_1 : pgd.Node, node_2 : pgd.Node, edge_type : pgd.EdgeType):
        """
        Generates edge with edge_type given two nodes(node_1,node_2)
        args:
            node_1 : python_graphs.program_graph_dataclasses.Node
            node_2 : python_graphs.program_graph_dataclasses.Node
            edge_type : python_graphs.program_graph_dataclasses.EdgeType
        """
        generated_edge = pgd.Edge(id1=node_1.id, id2=node_2.id, type=edge_type)
        return generated_edge
    def validate_edge_in_graph(self, edge_to_test : pgd.Edge, graph ) -> bool:
        """
        Validates if a Generated Graph is an edge in a given graph.
        args:
            edge_to_test  : python_graphs.program_graph_dataclasses.Edge
            graph         : python_graphs.program_graph_dataclasses.Node
        """
        return edge_to_test in graph
    def sample_true_edges(self,graph):
        """
        Samples True Edges alongside types from the given data flow graph.
        args:
            edge_to_test  : python_graphs.program_graph_dataclasses.Edge
            graph         : python_graphs.program_graph_dataclasses.Node
        """        
        #TODO : sample edges and get a promptable format.
        true_edges = []
        for chosen_edges in graph.edges:
            identifier_1, identifier_2, edge_type = graph.nodes[chosen_edges.id1].node.id,graph.nodes[chosen_edges.id2].node.id,chosen_edges.type
            if identifier_1 != identifier_2: #deduction of self-loop edges.
                edge_diction = {"idt_1":identifier_1,"idt_2":identifier_2,"edge_type": self.dfg_edge_english_lookup[edge_type]}
                true_edges.append(edge_diction)
        return true_edges

    def __call__(self,program_string):
        """
        Main call function to generate data_flow_generation
        args:
            program_string (str) : Program String of the function to be analyzed
        """      
        data_flow_graph = self.generate_complete_dataflow_graph(program_string)
        true_edges = self.sample_true_edges(data_flow_graph)
        data_flow_analysis = {"program_string":program_string,"true_edges":true_edges}
        return data_flow_analysis