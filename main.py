import streamlit as st
from plotter import Plotter
from PIL import Image

home_icon = Image.open("home.png")
lab_icon = Image.open("lab (1).png")
cad_icon = Image.open("cad.png")
graph_icon = Image.open("graph.png")
nav = ["Plotter", "Home", "Labs"]
Part_A = ["Question 1a", "Question 1b"]

instuctions = " 1.	Copy data into an excel sheet.\n 2.	Make sure that x-axis data is in the first column and the first cell of the column has the axis title.\n 3.	Save the sheet in .csv format.\n 4.	Name the file what you want as the Plot title.\n 5.	Upload the file.\n 6.	Change the plot preferences from the sidebar as required."

with st.beta_expander("Navigation"):
    col1, col2= st.beta_columns(2)
    with col2: 
        navi = st.selectbox("", nav)
        if navi == "Home":
            st.subheader("Hi,")
            st.write("Welcome to Your Lab progress tracker. \nLet's get you up to speed on your lab work :)")
            cms_id = st.number_input("Enter Your CMS ID", value=0)
            if cms_id != 0:
                id_entered = True
                id_ = cms_id
            else:
                id_entered = False
            if id_entered:
                st.write(f"You are logged in as: {id_}")
        if navi =='Labs':
            labs = ["Engineering Mechanics", "Electrical Engineering", "CAD"]
            lab = st.selectbox("Select Your Lab", labs)
    with col1:
        if navi == "Labs":
            if lab == "Engineering Mechanics":
                st.image(lab_icon, use_column_width=True)
            if lab == "CAD":
                st.image(cad_icon, use_column_width=True)
        elif navi == "Home":
            st.image(home_icon, use_column_width=True)
        elif navi == "Plotter":
            #st.image(graph_icon, use_column_width=True)
            st.subheader("Instructions")
            st.write(instuctions)
            pass

if navi == "Home":
    pass

if navi == "Labs":
    pass

if navi == "Plotter":
    st.title("Plot your data".title())
    st.sidebar.title("Preferences")
    l_best = st.sidebar.checkbox("Do you need to plot a line of best fit?".title())
    l_plt = st.sidebar.checkbox("Do you need a line plot?".title())
    grad = st.sidebar.checkbox("Do you need to calculate gradient of Line of best fit?".title())
    grad_calc = st.sidebar.checkbox("Do you need to show calculations for gradient of Line of best fit?".title())
    plotter = Plotter(l_best, l_plt)
    plotter.plot_data(grad_calc, grad)