from dgk.gui import DGKApplication, DGKInfoWindow, DGKWindow


def main():
    try:
        root = DGKApplication()
        DGKWindow(root)
        root.execute()
    except FileNotFoundError as err:
        DGKInfoWindow("Startup Error", err)


if __name__ == "__main__":
    main()
