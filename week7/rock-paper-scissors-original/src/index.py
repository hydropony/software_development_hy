from rps_factory import create_game

def main():
    while True:
        print("Choose game mode"
              "\n (a) Against human"
              "\n (b) Against AI"
              "\n (c) Against improved AI"
              "\nOther choices will exit"
              )

        answer = input()
        game = create_game(answer)
        if game is None:
            break
        game.play()


if __name__ == "__main__":
    main()
