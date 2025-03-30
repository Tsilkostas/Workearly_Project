from MovieData.main import MovieDataApp
import sys

def main() -> int:
    """Main entry point with return codes"""
    print("Starting MovieData app...")
    try:
        app = MovieDataApp()
        app.fetch_and_store_movie_data()
        print("Data fetch completed successfully!")
        return 0  # Success code
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1  # Error code

if __name__ == "__main__":
    sys.exit(main())