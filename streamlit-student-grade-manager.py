import streamlit as st
import pandas as pd

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="Grade Manager", page_icon="🎓", layout="wide")

# 2. Initialize Session State
if 'students' not in st.session_state:
    st.session_state.students = []

def calculate_grade(mark):
    if mark >= 90: return "A"
    elif mark >= 80: return "B"
    elif mark >= 70: return "C"
    elif mark >= 60: return "D"
    else: return "F"

# 3. Main Header
st.title("🎓 Student Grade Manager")
st.markdown("Easily track, visualize, and manage student performance across the class.")

# 4. Sidebar for Input (Keeps the main screen clean for data visualization)
with st.sidebar:
    st.header("Add New Student")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Student Name")
        # Enforces the 0-100 rule strictly in the UI
        mark = st.number_input("Mark (0-100)", min_value=0, max_value=100, step=1)
        
        submitted = st.form_submit_button("Add to Class", width='stretch')
        
        if submitted:
            if name.strip():
                st.session_state.students.append({
                    "Name": name.strip(),
                    "Mark": mark,
                    "Grade": calculate_grade(mark)
                })
                st.success(f"Added {name.strip()} successfully!")
                
                # Fun touch: Celebrate high achievers
                if mark >= 90:
                    st.balloons()
            else:
                st.error("Please enter a valid student name.")

# 5. Dashboard Generation
if not st.session_state.students:
    st.info("👈 Add your first student in the sidebar to generate the class dashboard!")
else:
    # Convert list of dicts to a Pandas DataFrame for powerful charting and tables
    df = pd.DataFrame(st.session_state.students)
    
    # --- TOP ROW: Key Metrics ---
    st.subheader("Class Overview")
    col1, col2, col3 = st.columns(3)
    
    avg_mark = df["Mark"].mean()
    col1.metric("Class Average", f"{avg_mark:.1f}")
    col2.metric("Highest Mark", int(df["Mark"].max()))
    col3.metric("Lowest Mark", int(df["Mark"].min()))
    
    st.divider()

    # --- MIDDLE SECTION: Tabs for Organization ---
    tab1, tab2 = st.tabs(["📊 Performance Visuals", "📋 Detailed Records"])
    
    with tab1:
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("**Marks by Student**")
            # Bar chart comparing all students
            st.bar_chart(df.set_index("Name")["Mark"], color="#4CAF50")
            
        with chart_col2:
            st.markdown("**Grade Distribution**")
            # Calculates how many A's, B's, etc., and graphs them
            grade_counts = df["Grade"].value_counts().sort_index()
            st.bar_chart(grade_counts, color="#FF9800")
            
    with tab2:
        st.markdown("**Interactive Student Data**")
        # Upgraded table with visual progress bars instead of just raw numbers
        st.dataframe(
            df,
            column_config={
                "Name": st.column_config.TextColumn("Student Name"),
                "Mark": st.column_config.ProgressColumn(
                    "Mark",
                    help="Student's score out of 100",
                    format="%d",
                    min_value=0,
                    max_value=100,
                ),
                "Grade": st.column_config.TextColumn("Final Grade")
            },
            hide_index=True,
            width='stretch'
        )