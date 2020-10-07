from Plot_class import Base_MatPlotGraph_Object, Base_Graph_ChartTypes
from data_examples import EXAMPLE_1


my_graph = Base_MatPlotGraph_Object(EXAMPLE_1, False, 'Total Hours')
my_graph.set_figure_data((12, 9))
my_graph.create_graph_figure(Base_Graph_ChartTypes.PIE)
my_graph.save_image()
