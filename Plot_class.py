########################################
# Base MatPlotGraph Class Object
#
#
#
########################################

# array, plot_kind, title_string='Results', xlabel_string="",
# ylabel_string="Percentage", figsize_width=12, figsize_hight=9

import logging
import numpy as np
import re
from enum import Enum
from matplotlib import pyplot as plt
from matplotlib import patches as pat



class Base_Graph_ChartTypes(Enum):
    """
    Chart Types
    """
    BAR = 'BarChart'
    PIE = 'PieChart'
    LINE = 'LineChart'


# Defs
BASE_PLOT_BAR_DEFAULT_COLORS = ['springgreen', 'coral', 'gold', 'skyblue',
                                'indigo', 'silver', 'darkturquoise',
                                'lightsalmon']


# data_type_keyword


class Base_MatPlotGraph_Object:
    """
    Base Matplotlib based graph object
    """
    PERCENTAGE_KEYWORD = 'Percentage'

    TOTAL_HOURS_KEYWORD = 'Total Hours'

    COSTS_KEYWORD = 'Cost'

    DATE_KEYWORD = 'Date'

    #################### Inits ####################

    def __init__(self, matrix, is_flipped=False, data_type_keyword=None,
                 file_name='plot', file_dpi=400):
        """
        Inits
        """
        # the matrix
        self._matrix = matrix
        # is the matrix pivoted and need to be transposed or not.
        # Default is not pivoted
        # If matrix is pivoted then transposing
        if is_flipped is True:
            self._matrix = [list(x) for x in zip(*self._matrix)]
        # which kind of data is given:
        self._data_type_keyword = data_type_keyword

        try:
            self.__convert_matrix_to_plot_data()
            self.__is_ok = True
        except Exception as e:
            logging.warning('Could not create Graph Data: {}'.format(e.__str__()))
            self.__is_ok = False

        #### file setting #####
        # wanted file name
        self._file_name = file_name

        # wanted dpi size

        self._dpi = file_dpi

    ######### Convert Matrix To Plot Data #########

    def __convert_matrix_to_plot_data(self):
        """
        Converts Matrix to Plot Data
        :return:
        """

        # raw data for plotting according to type given
        # Takes only the list from data according to type keyword
        self._row_from_matrix = [array for array in self._matrix if array[0] == self._data_type_keyword]
        # dropping the two first values in the array as the first is row name and the second is total
        self._row_data = self._row_from_matrix[0][2:]
        # generating the total variable
        self._row_total = self._row_from_matrix[0][1]

        # Retrieves the data to be plotted according to type requested(the keyword)
        if self._data_type_keyword == Base_MatPlotGraph_Object.PERCENTAGE_KEYWORD:
            self.__convert_matrix_to_percentage()
        elif self._data_type_keyword == Base_MatPlotGraph_Object.COSTS_KEYWORD:
            self.__convert_matrix_to_costs()
        else:
            self.__convert_matrix_to_numbers()

        # Retrieves labels from matrix
        self._labels = [i.replace('\n', '/ ').
                            replace(' (Empty)', '').title().
                            replace('//', '') for i in self._matrix[0][2:]]

    def __convert_matrix_to_percentage(self):
        '''
        Converts Matrix as Percentage
        :return:
        '''
        # Removes '%' and converts to float
        self._plot_data = \
            [float(i.replace('%', ''))
             for i in self._row_data]

    def __convert_matrix_to_costs(self):
        '''
        Converts Matrix as costs
        :return:
        '''
        self._plot_data = \
            [round(val / float(self._row_total.replace('$', '')) * 100.0) for val in
             (float(elm.replace('$', '')) for elm in self._row_data)]

    def __convert_matrix_to_numbers(self):
        '''
        Converts Matrix as Percentage
        :return:
        '''
        self._plot_data = \
            [round(val / float(self._row_total) * 100.0) for val in
             (float(elm) for elm in self._row_data)]

    ################ Set Figure Data ##############

    def set_figure_data(self, fig_size, label_x='', label_y='Percentage', title=None):
        """
        Sets the Figure Data
        :return:
        """
        self._figsize = fig_size
        self._label_x = label_x
        self._label_y = label_y
        # Title naming logic
        if title == None:
            if self._data_type_keyword == Base_MatPlotGraph_Object.PERCENTAGE_KEYWORD:
                self._title = title
            else:
                self._title = self._data_type_keyword + ' in Percentage'
        else:
            self._title = title

        self.upper_limit_bar = round(max(self._plot_data) / 10 + 1.5) * 10

    ################ Create Chart : Pie ###########

    def __create_chart_pie(self):
        """
        Creates Chart: PIE
        :return:
        """
        # Plotting the data
        # label on pie are reverted to be shown with \n
        plt.pie(self._plot_data, startangle=90,
                labels=[elm.strip().replace('/ ', '\n').replace('//', '') for elm in self._labels], autopct='%d%%')
        plt.axis('equal')  # turning pei into 2d
        # making legend only dataset of 6 or less dataset points
        if len(self._labels) <= 6:
            plt.legend(self._labels, fontsize=14 - len(self._labels), loc=2)

    ################ Create line graph #############

    def __create_line_graph(self):

        # Trasforming the given the matrix in to the data needed for multi line graph

        self.__line_graph_convert_matrix_to_plot_data()

        # Ploting a line for each  date

        for i in range(len(self._labels)):
            plt.plot(self._xvalues, self._yvalues[i], linewidth=2, marker='o')
            for x, y in zip(self._xvalues, self._yvalues[i]):
                plt.annotate(y,  # this is the text
                             (x, y),
                             textcoords="offset points",  # how to position the text
                             xytext=(0, 10),  # distance from text to points (x,y)
                             ha='center')  # horizontal alignment can be left, right or center
        plt.xticks(self._xvalues, rotation=45, ha='right')

        plt.legend(self._labels, loc=0)





        plt.grid(color='grey', linestyle='-', linewidth=0.7, alpha=0.5)
        plt.title('Total Hours worked worked for each day'.title(), fontsize=24)
        plt.xlabel('Dates', fontsize=14)
        plt.ylabel('Total Hours', fontsize=14)
        plt.xlim((self._xvalues[0], self._xvalues[-1:]))
        plt.ylim(0, np.max(self._yvalues) + 10 ** (len(str(np.max(self._yvalues))) - 1))

    def __line_graph_convert_matrix_to_plot_data(self):
        """
        Converts Matrix to Plot Data for line graph
        :return:
        """
        """
         # prepring the data for plot
         # extracting the relevent information. i.e only lines with dates. droping the rest for now,
         # the dates are going to be the x axis. the numbers are going to be the y axis
         row_data = [lst for lst in self._matrix if bool(re.search("[0-9]{2}/[0-9]{2}/[0-9]{4}", lst[0])) is True]
         # fliping the matrix to get the wanted data.  relevent data for each label(line)
         row_data_tras = np.transpose(row_data)

         # extracting the y values. on for the second list onward.
         # drooing any uneeded data- all the information in the brackets
         self._yvalues = [[int(elm.split(' ')[0]) for elm in line] for line in list(row_data_tras[1:])]

         # extracting the x axis values i.e the dates. the first list in the matrix
         self._xvalues = list(row_data_tras[0])

         # extracting the labeles for each line for the row data lisr. i.e the columns.
         # the firt label is allways empyty (name of the row name column has no name)
         self._labels = [elm.replace('(Empty)', '').replace('\n', '/') for elm in self._matrix[0][1:]]
         """

        # prepring the data for plot
        # extracting the relevent information. i.e only lines with dates. droping the rest for now,
        # the dates are going to be the x axis. the numbers are going to be the y axis
        raw_data = []
        for lst in self._matrix:
            # take the frist var in a list. i.e the name of the row
            row_name = lst[0]
            # if the row name is in the pattern of a date append that row into the row data
            if bool(re.search("[0-9]{2}/[0-9]{2}/[0-9]{4}", row_name)) is True:
                raw_data.append(lst)

        # fliping the matrix to get the wanted data.  relevent data for each label(line)
        raw_data_tras = np.transpose(raw_data)

        # extracting the y values. on for the second list onward.
        # dropping any uneeded data- all the information in the brackets
        self._yvalues = []
        # iterate over the rows in the data taking only the acutal values. and dropping the row names(the dates)
        for row in list(raw_data_tras[1:]):
            # in each row iterate over the data points and take only the left most value.
            # do that by spliting the string and taking only the frist number.
            # turn it into a int so we can plot it. (can change to float but not need at the moment
            clean_row = []
            for value in row:
                clean_value = int(value.split(' ')[0])
                clean_row.append(clean_value)
            self._yvalues.append(clean_row)

        # extracting the x axis values i.e the dates. the first list in the matrix
        self._xvalues = list(raw_data_tras[0])

        # extracting the labeles for each line for the row data listt. i.e the columns.
        # the firt label is allways empyty (name of the row name column has no name)
        self._labels = [elm.replace('(Empty)', '').replace('\n', '/') for elm in self._matrix[0][1:]]
        self._labels = []
        # iterate over the columns rows (the each represents a line) in the matrix.
        # this is the first list after dropping the first entry, which is allways empty(the row name of the column row
        raw_line_names = self._matrix[0][1:]
        for line_name in raw_line_names:
            # cleaning the line name from (Empty) and \n values
            cleaned_line_name = line_name.replace('(Empty)', '').replace('\n', '/')
            self._labels.append(cleaned_line_name)

    ################ Create Chart: Bar ############

    def __create_chart_bar(self):
        """
        Creates Chart: BAR
        :return:
        """
        # defining the x and y ticks scope
        x_scope = range(len(self._labels))  # len of data
        # Assuming that it is % based so up to 5- 15 point above the max value
        y_scope = range(0, self.upper_limit_bar, 5)
        # defining the figure ab ax vars
        ax = plt.subplot()

        # main plot
        _plot = plt.bar(x_scope, self._plot_data,
                        color=BASE_PLOT_BAR_DEFAULT_COLORS)

        # Defining the axies and labeling them
        ax.set_xticks(x_scope)
        ax.set_xticklabels(self._labels)
        ax.set_yticks(y_scope)
        ax.set_yticklabels(y_scope)

        # Generating the text to be annotated on top of the bars according to type keyword
        # for %
        if self._data_type_keyword == Base_MatPlotGraph_Object.PERCENTAGE_KEYWORD:
            annotated_text = ['{}%'.format(_plot[i].get_height()) for i in x_scope]
        # for $
        elif self._data_type_keyword == Base_MatPlotGraph_Object.COSTS_KEYWORD:
            annotated_text = ['{}%\n(${})'.format(_plot[i].get_height(), self._row_data[i]) for i in x_scope]
        # for numbers
        else:
            annotated_text = ['{}%\n({})'.format(_plot[i].get_height(), self._row_data[i]) for i in x_scope]

        # Entring the numbers on top of the bars
        # (annotating the bars with the data the numbers)
        for i in x_scope:
            ax.annotate(annotated_text[i],
                        # the numbers as text to enter
                        xy=(_plot[i].get_x() + _plot[i].get_width() // 2, _plot[i].get_height()),
                        # starting point of the test before adjustment
                        # the middle of the bar
                        xytext=((i) * 1.0, _plot[i].get_height()),
                        # adjusting of the text to be on top of the bar
                        # (as the x axis increments in one the the jumps are in 1 and the y is the hight of the bar i.e the y value)
                        textcoords='data',  # starting of the xytext is the xy points
                        # text info
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        fontsize=24 - max(x_scope))

        # labeling the axies
        plt.xlabel(self._label_x, fontsize=21)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(self._label_y, fontsize=21)
        # handeling the backround and frame of the graph
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(color='grey', linestyle='-', linewidth=0.7, alpha=0.5)

        # building a legend only if there are 6 or less bars
        if len(self._labels) <= 6:
            # color - making sure the color list will never be out of range by duplicating it x times.
            # when x is the times the len of color list enters in the len of the label list + 1
            list_multiplier = len(x_scope) // len(BASE_PLOT_BAR_DEFAULT_COLORS) + 1
            # creating the adjusted color list from
            legend_colors = BASE_PLOT_BAR_DEFAULT_COLORS * list_multiplier
            # creating the legend content as a list of matplotlib's patches Objects
            legend_content = []
            # looping through x_scope which is the len of data
            for i in x_scope:
                # pairng each label with its matching color just like the bars and creating the object
                entry_in_legend = pat.Patch(color=legend_colors[i], label=self._labels[i], alpha=0.6)
                # adding the object to the content list
                legend_content.append(entry_in_legend)
            # creating the legend for thr content list
            ax.legend(handles=legend_content, loc=0)

    ################ Create Graph #################

    def create_graph_figure(self, chart_type):
        """
        Creates Graph
        :return:
        """
        if self.__is_ok is False:
            return None
        # Resetting Current Figure
        plt.close('all')
        self._figure = None
        if chart_type not in Base_Graph_ChartTypes:
            raise Exception('Unknown chart type: {}'.format(chart_type))

        # Create the Figure
        self._figure = plt.figure(figsize=(self._figsize[0], self._figsize[1]))
        # Calls relevant function for chart type
        self._chart_type = chart_type
        if self._chart_type == Base_Graph_ChartTypes.PIE:
            # Call Pie
            self.__create_chart_pie()
        if self._chart_type == Base_Graph_ChartTypes.BAR:
            # Call Bar
            self.__create_chart_bar()
        if self._chart_type == Base_Graph_ChartTypes.LINE:
            self.__create_line_graph()
        plt.title(self._title, fontsize=20)

    ################ Save Image ##################

    def save_image(self):
        """
        Saves Graph Image
        :return:
        """
        if self.__is_ok is False:
            return None
        plt.savefig('./static/img/' + self._file_name + '.png', dpi=self._dpi)

    ################ Show Figure #################

    def show_figure(self):
        """
        Shows Current Figure
        :return:
        """
        if self.__is_ok is False:
            return None
        plt.show()
        # plt.close()
