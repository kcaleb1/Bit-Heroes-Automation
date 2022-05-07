from farm.fishing import go_fishing
from farm.boss import go_boss
from farm.raid import go_raid


def main():
    go_fishing(is_loop=True)
    # go_boss(is_loop=False)
    go_raid(is_loop=True)


if __name__ == '__main__':
    main()
