# run_server.py
import uvicorn


def main():
    uvicorn.run(
        "main:app",  # 🔁 change if your app is in another module
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n[ERROR] Backend crashed:")
        print(e)
        print("\nPress Enter to exit...")
        input()
    else:
        print("\nServer stopped. Press Enter to exit...")
        input()
