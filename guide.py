import flet as ft
import requests
import threading


def main(page: ft.Page):
    page.title = "Guide"
    page.bgcolor = "#0f0c13"
    page.scroll = True
    page.update()

    pr_container = ft.Row([ft.ProgressRing(visible=False, width=60, height=60, stroke_width=2, color="#8102ed",
                                           bgcolor="#333333")], alignment="center")
    page.add(pr_container)

    def fetch_data():
        try:
            response = requests.get("http://192.168.100.195:8000/api/v1/guide")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao acessar a API: {e}")
            return []

    # Custumize conforme necessário para substituir 'vertical_alignment'
    guide_layout = ft.Column()

    page.add(ft.Row([guide_layout], alignment="center"))  # Envolver o guide_layout em uma Row centralizada

    def update_movies():
        movie_list = fetch_data()
        cards = [create_card(movie) for movie in movie_list]
        guide_layout.controls.clear()
        guide_layout.controls.extend(cards)
        pr_container.controls[0].visible = False
        page.update()

    def on_refresh_click(e):
        pr_container.controls[0].visible = True
        page.update()
        refresh_movies()

    def refresh_movies():
        threading.Thread(target=update_movies).start()

    def underscore(text):
        return text.replace(' ', '_')

    def create_card(movie):
        progress_init_movie = movie.get('progress_init_movie')
        progress_decimal = None

        if progress_init_movie:
            progress_init_movie = progress_init_movie.strip('%')
            progress_decimal = int(progress_init_movie) / 100
        pb = ft.ProgressBar(value=progress_decimal, color="#8102ed", bgcolor="#333333")

        return ft.Card(
            content=ft.Container(
                bgcolor='#1b181f',
                border_radius=ft.border_radius.all(8),
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Image(src=f'{underscore(movie['movie_channel'])}.png'),
                            title=ft.Text(
                                movie['title_init_movie'] or "Movie Not Available",
                                style=ft.TextStyle(
                                    color=ft.colors.WHITE,
                                    size=25,  # Tamanho do texto
                                )
                            ),
                            subtitle=ft.Text(
                                "Canal: {}".format(
                                    movie['movie_channel_number']
                                ),
                                style=ft.TextStyle(
                                    color=ft.colors.WHITE,
                                    size=20
                                )
                            ),
                        ),
                        ft.Text(movie['progress_init_movie'],
                                style=ft.TextStyle(
                                    color=ft.colors.WHITE,
                                    size=25,
                                )
                                ),
                        pb,
                        ft.Row(
                            wrap=True,
                            controls=[
                                ft.Text("Próximo: {}".format(movie['next_movie_info'] or "N/A")),
                                ft.Text("Próximo: {}".format(movie['next_movie_info2'] or "N/A"))
                            ],

                        ),

                    ]
                ),
                width=400,
                padding=10,
            )
        )

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.MOVIE_OUTLINED),
        title=ft.Text("Guide"),
        actions=[
            ft.IconButton(ft.icons.REFRESH, on_click=on_refresh_click),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Programa feito para mostrar a programação de filmes."),
                ]
            )

        ],
        bgcolor="#1b181f",
    )

    # Inicia a busca e exibição dos filmes ao carregar a aplicação
    refresh_movies()


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')