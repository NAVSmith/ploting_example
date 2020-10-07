########################################
# this is the basic app controller
#
#
#
########################################

# imports
from flask import Flask, request, render_template
from run import make_graph
import matplotlib
from Plot_class import Base_MatPlotGraph_Object, Base_Graph_ChartTypes
from data_examples import EXAMPLE_1


# init the app
app = Flask(__name__)

## the body of app


# input functions

@app.route('/send', methods=['GET', 'POST'])
def user_graph_input():
    """
    read the kind of graph the user want to see
    pass it to the a function that the relevent class
    :return:
    """
    status = None
    if request.method == 'POST':
        graph_type = request.form['graph_type']
        print(graph_type)
        make_graph(graph_type)
        status = 'done'
    return render_template('index.html')





# control functions

# out put function

def insert_graph_to_page():
    """

    :return:
    """
    pass


# execute
if __name__ == "__main__":
    matplotlib.pyplot.switch_backend('Agg')
    app.run(debug=True)
