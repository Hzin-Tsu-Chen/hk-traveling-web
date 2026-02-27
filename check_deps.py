try:
    import fastapi
    import uvicorn
    import jinja2
    import multipart
    print("All dependencies are present.")
except ImportError as e:
    print(f"Missing dependency: {e}")
