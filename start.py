import subprocess
def run_streamlit():
    subprocess.run(["streamlit", "run", "seikatu.py"], check=True)

if __name__ == '__main__':
    run_streamlit()
