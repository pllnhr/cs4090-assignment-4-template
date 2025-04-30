import streamlit as st
import subprocess
import os

st.title("Pytest To-Do App Tester")

st.markdown("Select and run tests")

commands = {
    "Run All Tests": "pytest --disable-warnings tests/",
    "Run Coverage Report": "pytest --cov=src tests/",
    "Run Basic Tests": "pytest tests/test_basic.py",
    "Run Advanced Tests (Parameritzed for filter testing)": "pytest tests/test_advanced.py",
    "Run TDD Tests": "pytest tests/test_tdd.py",
    "Run BDD Tests": "pytest tests/test_bdd.py",
    "Generate HTML Report": "pytest --html=report.html --self-contained-html tests/"
}

for label, cmd in commands.items():
    if st.button(label):
        with st.spinner(f"Running: {label}"):
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                st.text_area("Test Output", result.stdout + "\n" + result.stderr, height=300)

                if "HTML" in label and os.path.exists("report.html"):
                    with open("report.html", "r", encoding="utf-8") as f:
                        html_report = f.read()
                    st.components.v1.html(html_report, height=600, scrolling=True)

            except Exception as e:
                st.error(f"Error running {label}: {e}")
