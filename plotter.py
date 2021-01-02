import pandas as pd
from scipy import stats
import numpy as np
import streamlit as st
import plotly.graph_objs as go
from sympy import *
from sympy.matrices.expressions.slice import slice_of_slice
from plotly.subplots import make_subplots

class Plotter:
    def __init__(self, title: str, best_fit = True, line_chart=True):
        '''
        Plots the uploaded data

        dtypes supported: .csv

        It generates the upload widget by itself
        '''
        self.dataframe = None
        self.best_fit = best_fit
        self.title = title
        self.columns = None
        self.line_chart = line_chart
        
    def get_uploaded_file(self):    
        self.uploaded_file = st.file_uploader(
                    "Please Upload the file containing the data you need plotted",
                    type="csv")
        if self.uploaded_file is not None:
            self.dataframe = pd.read_csv(self.uploaded_file)
            self.uploaded_file.seek(0)
            st.table(self.dataframe)
    
    def getListofColumns(self):
        if self.dataframe is not None:
            columns = list(self.dataframe)
            self.headings = []
            for head in columns:
                self.headings.append(head.split(" ")[0])
            self.gen_dict = {k: v for v, k in enumerate(self.headings)}
            return self.headings
        else:
            return ["Upload Data to See Options"]

    def generate_graph(self, number: int, x_axis: str, y_axis: str):
        if self.dataframe is not None:
            self.columns = np.squeeze(self.dataframe.columns)
            if number == 1:
                self.slope, self.intercept, r_value, p_value, std_error = stats.linregress(
                    self.dataframe[self.columns[self.gen_dict[x_axis]]], self.dataframe[self.columns[self.gen_dict[y_axis]]])

                fig = go.Figure()
                status = "markers"
                if self.line_chart:
                    status = "lines+" + status

                fig.add_trace(go.Scatter(
                x = self.dataframe[self.columns[self.gen_dict[x_axis]]], 
                y = self.dataframe[self.columns[self.gen_dict[y_axis]]],
                mode = status, 
                name= "Recorded Data"
                ))

                line = self.slope*np.array(self.dataframe[self.columns[self.gen_dict[x_axis]]]) + self.intercept
                if self.best_fit:
                    fig.add_trace(go.Scatter(
                        x = self.dataframe[self.columns[self.gen_dict[x_axis]]], 
                        y = line,
                        mode = 'lines', 
                        line = dict(color='firebrick', width=2), 
                        name= "Line of BestFit"
                    ))

                fig.update_layout(
                    title = {
                        "text": f'{self.title}',
                        'y':0.9, 
                        'x': 0.5},
                    xaxis_title = self.columns[self.gen_dict[x_axis]], 
                    yaxis_title = self.columns[self.gen_dict[y_axis]], 
                    legend_title = "Legend"
                )
                st.plotly_chart(fig)
                return True
            if number == 2:
                self.slope_1, self.intercept_1, r_value, p_value, std_error = stats.linregress(
                    self.dataframe[self.columns[self.gen_dict[x_axis[0]]]], self.dataframe[self.columns[self.gen_dict[y_axis[0]]]])
                self.slope_2, self.intercept_2, r_value, p_value, std_error = stats.linregress(
                    self.dataframe[self.columns[self.gen_dict[x_axis[1]]]], self.dataframe[self.columns[self.gen_dict[y_axis[1]]]])
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])

                status = "markers"
                if self.line_chart:
                    status = "lines+" + status

                fig.add_trace(go.Scatter(
                x = self.dataframe[self.columns[self.gen_dict[x_axis[0]]]], 
                y = self.dataframe[self.columns[self.gen_dict[y_axis[0]]]],
                mode = status, 
                name= "Recorded Data"),
                secondary_y = False,
                )

                fig.add_trace(go.Scatter(
                x = self.dataframe[self.columns[self.gen_dict[x_axis[1]]]], 
                y = self.dataframe[self.columns[self.gen_dict[y_axis[1]]]],
                mode = status, 
                name= "Recorded Data for plot 2".title()),
                secondary_y = True,
                )

                line_1 = self.slope_1*np.array(self.dataframe[self.columns[self.gen_dict[x_axis[0]]]]) + self.intercept_1
                line_2 = self.slope_2*np.array(self.dataframe[self.columns[self.gen_dict[x_axis[1]]]]) + self.intercept_2
                if self.best_fit:
                    fig.add_trace(go.Scatter(
                        x = self.dataframe[self.columns[self.gen_dict[x_axis[0]]]], 
                        y = line_1,
                        mode = 'lines', 
                        line = dict(color='firebrick', width=2), 
                        name= "Line of BestFit"
                    ))

                    fig.add_trace(go.Scatter(
                        x = self.dataframe[self.columns[self.gen_dict[x_axis[1]]]], 
                        y = line_2,
                        mode = 'lines', 
                        line = dict(color='firebrick', width=2), 
                        name= "Line of BestFit"
                    ))

                fig.update_layout(
                    title = {
                        "text": f'{self.title}',
                        'y':0.9, 
                        'x': 0.5},
                    xaxis_title = self.columns[self.gen_dict[x_axis[0]]], 
                    legend_title = "Legend"
                )

                fig.update_yaxes(title_text = self.columns[self.gen_dict[y_axis[0]]], secondary_y=False)
                fig.update_yaxes(title_text = self.columns[self.gen_dict[y_axis[1]]], secondary_y=True)

                st.plotly_chart(fig)
                return True

        return False
    
    def gradient_calc(self, show_grad_calc = True):
        if show_grad_calc:
            A_pre = list(zip(self.dataframe[self.columns[0]], np.ones(np.array(self.dataframe[self.columns[0]]).shape)))
            A = Matrix(A_pre)
            A_T = A.T
            b = Matrix(self.dataframe[self.columns[1]])
            x_unk = Matrix([["M"], ["b"]])
            res = Matrix([[round(self.slope, 2)], [round(self.intercept, 2)]])
            st.subheader('gadient calculation'.title())
            st.write("Using Least Square Analysis to find the gradient:")
            st.markdown("<ul><li>The equation of a straight line is: </li></ul>", unsafe_allow_html=True)
            st.latex(r"y = mx + c")
            st.markdown("<ul><li>The corresponding linear equations would be: </li></ul>", unsafe_allow_html=True)
            for x in range(np.array(self.dataframe[self.columns[0]]).shape[0]):
                st.latex(fr"{np.array(self.dataframe[self.columns[1]])[x]} = {np.array(self.dataframe[self.columns[0]])[x]}M + b")
            st.markdown("<ul><li>The Corresponding Matix Equation for System of Equations is: </li></ul>", unsafe_allow_html=True)
            st.latex(latex(A) + latex(x_unk)+ "=" + latex(b))
            st.latex(r"Ax = b")
            st.latex(r"A^{T}Ax = A^{T}b")
            st.latex(r"x = (A^{T}A)^{-1}A^{T}b")
            st.latex(r"x = " + latex(res))
            st.latex(fr"\therefore gradient = {round(self.slope, 2)}")
        else:
            st.latex(fr"gradient = {round(self.slope, 4)}")

    def plot_data(self, number, x_axis, y_axis, show_calculations=False, grad = True):
        state = self.generate_graph(number, x_axis, y_axis)
        if grad:
            if state:
                self.gradient_calc(show_calculations)
        else: pass
