import asyncio
import flet as ft
from src.apps.base_app import BaseApp

#2 frame ascii gif - harder than it looks !
class FokiApp(BaseApp):
    FRAMES = [
        r"""
             _                       _
          (\/ )        _  _         ( \/)
           \  |       ( \/ )        |  /
            ) |        \  /         | (
           /  \         \/         /   \
         ,-    \       /  \       /    -,
        /6 6    \     / _  \     /     a a
     &/(_x_ ),_/`)   / 6 6  \   (`\_,( _x_)-/}
              `  `-'>(_x_)< `-' `
   __________________________________________
""",
        r"""
                 _                       _
              (\/ )        _  _         ( \/)
               \  |      ( \/ )         |  /
                ) |       \  /          | (
               /  \        \/          /   \
             ,-    \      /  \        /    -,
            /- -    \    / _  \      /     6 6
         &/(_x_ ),_/`)  / a a  \    (`\_,( _x_)-/}
                  `  `-'>(_x_)< `-' `
       __________________________________________
""",
    ]

    def __init__(self, phone):
        super().__init__(phone)
        self.index = 0
        self.text = None
        self.width = 0
        self.height = 0

    def _font_size(self, ascii_art):
        lines = ascii_art.strip("\n").split("\n")
        rows = len(lines)
        cols = max(len(line) for line in lines)

        return min(
            (self.width / cols) / 0.6,
            self.height / rows,
        )


    #uses ticks
    def _tick(self):
        self.index = (self.index + 1) % len(self.FRAMES)
        art = self.FRAMES[self.index]
        self.text.value = art
        self.text.size = self._font_size(art)
        self.text.update()

    async def _animate(self):
        while True:
            await asyncio.sleep(0.5) #animation frame delay
            self._tick()

    def build(self, width, height):
        #just screen compatibility
        self.width = width
        self.height = height


        self.text = ft.Text(
            value=self.FRAMES[0],
            font_family="monospace",
            color="black",
            size=self._font_size(self.FRAMES[0]),
            no_wrap=True,
            text_align=ft.TextAlign.CENTER,
        )

#outer page
        self.phone.page.run_task(self._animate)

        return ft.Container(
            width=width,
            height=height,
            alignment=ft.Alignment.CENTER,
            content=self.text,
        )

    # no keys needed here
    # def on_key(self, key):
    #     print(f"Pressed key: {key}")
