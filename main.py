import os
import subprocess
import sys

def main():
    """
    Lanza el dashboard Streamlit desde main.py
    """
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
    if not os.path.exists(dashboard_path):
        print("❌ No se encontró dashboard.py en la carpeta del proyecto.")
        sys.exit(1)

    print("⚡ Lanzando ChronoLogistics Dashboard...")
    # Ejecutar streamlit run dashboard.py
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
