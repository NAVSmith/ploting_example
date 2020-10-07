from Plot_class import Base_MatPlotGraph_Object, Base_Graph_ChartTypes
from data_examples import EXAMPLE_1

def make_graph(graph_type):
    graph_type = getattr(Base_Graph_ChartTypes, graph_type)
    print('prossing the data')
    my_graph = Base_MatPlotGraph_Object(EXAMPLE_1, False, 'Total Hours')
    print('making the figure')
    my_graph.set_figure_data((12, 9))
    print('plotting')
    my_graph.create_graph_figure(graph_type)
    print('saving the plot')
    my_graph.save_image()
    return my_graph._figure
