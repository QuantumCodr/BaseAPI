from pathlib import Path
from cli.utils.renderer import render_directory


def run_test():

    test_dir = Path("tests/")

    render_directory(
        test_dir,
        {
            "PROJECT_NAME": "shop-api",
            "BASEAPI_VERSION": "0.1.0",
        }
    )

    print("Renderer executed successfully 🚀")


if __name__ == "__main__":
    run_test()