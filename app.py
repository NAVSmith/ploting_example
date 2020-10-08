########################################
# this is the basic app controller
#
#
#
########################################

# imports
from flask import Flask, request, render_template, redirect
from run import make_graph
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
from Plot_class import Base_MatPlotGraph_Object, Base_Graph_ChartTypes
from data_examples import EXAMPLE_1


# init the app
app = Flask(__name__)

## the body of app


# input functions

@app.route('/', methods=['GET', 'POST'])
def user_graph_input():
    """
    read the kind of graph the user want to see
    pass it to the a function that the relevent class
    :return:
    """
    matplotlib.pyplot.switch_backend('Agg')
    status = None
    if request.method == 'POST':
        graph_type = request.form['graph_type']
        print(graph_type)
        fig = make_graph(graph_type)
        # Convert plot to PNG image
        png_image = io.BytesIO()
        FigureCanvas(fig).print_png(png_image)

        # Encode PNG image to base64 string
        png_image_b64_string = "data:image/png;base64,"
        png_image_b64_string += base64.b64encode(png_image.getvalue()).decode('utf8')
        return render_template('index.html', image=png_image_b64_string)
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
