# Social Eagle Automation Architect - Day 4 Assignments

This repository contains the deliverables for the Day 4 tasks of the Social Eagle Automation Architect Program. It includes two separate web applications built using Python: a backend API built with FastAPI and an interactive frontend data dashboard built with Streamlit.

## Repository Structure

*   `main.py`: The FastAPI backend application.
*   `streamlit-student-grade-manager.py`: The Streamlit interactive dashboard application.
*   `requirements.txt`: Python dependencies required to run the applications.

---

## Assignment 1: FastAPI Web Server

A basic web API built with the FastAPI framework that returns JSON data and automatically generates interactive Swagger UI documentation.

### Features
*   **Root Endpoint (`/`):** Returns a simple JSON welcome message.
*   **Dynamic Routing (`/greet/{name}`):** Accepts a path parameter from the URL and returns a personalized JSON response.
*   **Interactive Docs:** Automatically hosts a Swagger UI interface at `/docs` for seamless endpoint testing.

---

## Assignment 2: Streamlit Student Grade Manager

A presentation-ready interactive web dashboard for managing and visualizing student grades, built exclusively with Streamlit.

### Features
*   **Session State Management:** Student records are stored in `st.session_state` to persist data across app interactions and reruns.
*   **Sidebar Data Entry:** Clean UI separating the input form (Name and 0-100 Mark validation) from the data visualization.
*   **Dynamic Metrics:** Automatically calculates and displays the Class Average, Highest Mark, and Lowest Mark.
*   **Visual Dashboard:** Uses `pandas` to generate dynamic bar charts for mark comparisons and grade distributions, alongside an interactive data table with visual progress bars.
*   **Automated Grading:** Implements a standard grading scale (A-F) based on the inputted mark.

---
