import streamlit as st
import os

# -------------------- FILE SETTINGS --------------------

COURSE_FILE = "courses_data.txt"

book_categories = {
    "Programming": ["Introduction to Python", "Data Structures in C"],
    "Thermodynamics": ["Fundamentals of Thermodynamics", "Heat Transfer"],
    "Circuit Analysis": ["Basic Electrical Circuits", "Power Systems Engineering"],
    "AI": ["Mathematics for Machine Learning", "Deep Learning with Python", "Neural Networks and Deep Learning"],
    "ML": ["Python Machine Learning", "Introduction to ML Algorithms", "Hands-On Machine Learning with Scikit-Learn"],
    "Security": ["Cybersecurity Essentials", "Network Security Principles", "Ethical Hacking"],
    "Data Analysis": ["Python for Data Analysis", "Big Data Analytics", "Data Visualization with Python"],
    "Automation": ["Introduction to Robotics", "Control Systems Engineering", "Autonomous Robots and AI"],
    "Quantum Mechanics": ["Quantum Mechanics Simplified", "Advanced Classical Mechanics", "Introduction to Astrophysics"],
    "Biology Data": ["Fundamentals of Bioinformatics", "Genomic Data Science", "Computational Biology"],
}

USER_CREDENTIALS = {"admins": "123456"}


# -------------------- FILE HANDLING --------------------

def load_courses():
    if os.path.exists(COURSE_FILE):
        with open(COURSE_FILE, "r") as file:
            for line in file:
                if "|" in line:
                    course, books = line.strip().split("|")
                    book_categories[course] = books.split(",")

def save_courses():
    with open(COURSE_FILE, "w") as file:
        for course, books in book_categories.items():
            file.write(f"{course}|{','.join(books)}\n")

load_courses()


# -------------------- SESSION STATE --------------------

if "page" not in st.session_state:
    st.session_state.page = "Start"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def go_to(page_name):
    st.session_state.page = page_name


# -------------------- BUTTON CENTER FUNCTION --------------------

def center_button(label):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        return st.button(label)


# -------------------- PAGES --------------------

# START PAGE
if st.session_state.page == "Start":
    st.title("📚 Book Recommendation System")
    if center_button("Start"):
        go_to("UserSelection")


# USER SELECTION PAGE
elif st.session_state.page == "UserSelection":
    st.header("Select User Type")

    if center_button("Learner"):
        go_to("Learner")

    if center_button("Admin Login"):
        go_to("Login")

    if center_button("Back"):
        go_to("Start")


# LEARNER PAGE
elif st.session_state.page == "Learner":
    st.header("📖 Learner Page")

    course = st.selectbox("Select Your Course", list(book_categories.keys()))

    if center_button("Recommend Books"):
        books = book_categories.get(course, [])
        if books:
            st.success(f"Recommended Books for {course}:")
            for book in books:
                st.write("•", book)
        else:
            st.error("No books found.")

    if center_button("Back"):
        go_to("UserSelection")


# LOGIN PAGE
elif st.session_state.page == "Login":
    st.header("🔐 Admin Login")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if center_button("Login"):
        if USER_CREDENTIALS.get(user_id) == password:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            go_to("Admin")
        else:
            st.error("Invalid credentials")

    if center_button("Back"):
        go_to("UserSelection")


# ADMIN PAGE
elif st.session_state.page == "Admin" and st.session_state.logged_in:
    st.header("⚙ Admin Page")

    st.subheader("Add New Course")
    new_course = st.text_input("Course Name")
    new_books = st.text_input("Books (Comma separated)")

    if center_button("Add Course"):
        if new_course and new_books:
            book_categories[new_course] = [b.strip() for b in new_books.split(",")]
            save_courses()
            st.success(f"{new_course} added successfully!")
        else:
            st.error("Enter valid course and books")

    st.subheader("Delete Course")
    delete_course = st.selectbox("Select Course to Delete", list(book_categories.keys()))

    if center_button("Delete Course"):
        del book_categories[delete_course]
        save_courses()
        st.success(f"{delete_course} deleted successfully!")

    if center_button("Logout"):
        st.session_state.logged_in = False
        go_to("Start")
