import streamlit as st
from plotter import Plotter
from PIL import Image

home_icon = Image.open("home.png")
lab_icon = Image.open("lab (1).png")
cad_icon = Image.open("cad.png")
graph_icon = Image.open("graph.png")
nav = ["Plotter", "Home", "Labs"]
Part_A = ["Question 1a", "Question 1b"]

instuctions = " 1.	Copy data into an excel sheet.\n 2.	Save the sheet in .csv format.\n 3.	Upload the file.\n 4. Change the plot preferences from the sidebar as required."

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
    title = st.sidebar.text_input("Enter the title of the graph")
    plotter = Plotter(title, l_best, l_plt)
    plotter.get_uploaded_file()
    choices = plotter.getListofColumns()
    x_axis = st.sidebar.selectbox("X-axis", choices)
    y_axis = st.sidebar.selectbox("Y axis", choices)
    number = st.sidebar.number_input("How many plots in one graph?", 1, 2)
    if number == 2:
        y_axis_1 = st.sidebar.selectbox("Y axis_2", choices)
        x_axis = (x_axis, x_axis)
        y_axis = (y_axis, y_axis_1)
    plotter.plot_data( show_calculations=grad_calc, grad= grad, number=number, x_axis=x_axis, y_axis=y_axis)

