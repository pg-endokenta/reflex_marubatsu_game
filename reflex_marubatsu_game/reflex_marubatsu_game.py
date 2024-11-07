import reflex as rx

PLAYER_A = "🙆"
PLAYER_B = "🙅"
COLOR_A = "lightblue"
COLOR_B = "lightgreen"
DEFAULT_COLOR = "CadetBlue"

class MarubatsuState(rx.State):
    board = [""] * 9
    board_colors = [DEFAULT_COLOR] * 9
    current_player = PLAYER_A
    winner = ""
    draw = False

    def make_move(self, index):
        if self.board[index] == "" and self.winner == "":
            self.board[index] = self.current_player
            if self.current_player == PLAYER_A:
                self.board_colors[index] = COLOR_A
            elif self.current_player == PLAYER_B:
                self.board_colors[index] = COLOR_B

            # 勝敗判定
            if self.check_winner():
                self.winner = self.current_player
            # 引き分け判定
            elif "" not in self.board:
                self.draw = True
            # 次のプレイヤーに切り替え
            else:
                self.switch_player()


    def switch_player(self):
        self.current_player = PLAYER_B if self.current_player == PLAYER_A else PLAYER_A

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 横
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 縦
            [0, 4, 8], [2, 4, 6]             # 斜め
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                return True
        return False

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = PLAYER_A
        self.winner = ""
        self.draw = False
        self.board_colors = [DEFAULT_COLOR] * 9

def index():
    return rx.center(
        rx.vstack(
            rx.heading("マルバツゲーム", font_size="2em", color=DEFAULT_COLOR),
            rx.grid(
                *[
                    rx.button(
                        MarubatsuState.board[i],
                        on_click=lambda i=i: MarubatsuState.make_move(i),
                        width="60px",
                        height="60px",
                        font_size="2em",
                        background_color=MarubatsuState.board_colors[i]
                    )
                    for i in range(9)
                ],
                grid_template_columns="repeat(3, 1fr)",
                gap="10px",
            ),

            rx.cond(
                MarubatsuState.winner != "",
                rx.text(f"{MarubatsuState.winner}の勝ち", font_size="2em", color=rx.cond(MarubatsuState.winner == PLAYER_A, COLOR_A, COLOR_B)),
                rx.cond(
                    MarubatsuState.draw,
                    rx.text("引き分けです！", font_size="2em"),
                    rx.text(f"{MarubatsuState.current_player}の番です", font_size="2em", color=rx.cond(MarubatsuState.current_player == PLAYER_A, COLOR_A, COLOR_B)),
                ),
            ),
            rx.button("リセット", on_click=MarubatsuState.reset_game, background_color=DEFAULT_COLOR),
            spacing="20px",
        ),
    padding_top="50px",
    ),

app = rx.App()
app.add_page(index)
