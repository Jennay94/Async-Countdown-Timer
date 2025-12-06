import flet as ft
import asyncio

# Soft pink/purple theme
PRIMARY = ft.Colors.PINK_400
ACCENT = ft.Colors.PURPLE_200
BG = ft.Colors.PINK_50
CARD_BG = ft.Colors.WHITE


# --------------------------------------
#   Reusable async countdown timer widget
# --------------------------------------
class CountdownTimer(ft.Column):
    def __init__(self, page: ft.Page, label: str):
        super().__init__()
        self.page = page
        self.label = label

        # Timer state
        self.initial_value = 30
        self.remaining = self.initial_value
        self.running = False

        # Input field for start value
        self.input_value = ft.TextField(
            label="Start value (seconds)",
            value=str(self.initial_value),
            width=200,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
        )

        # Remaining time display
        self.time_text = ft.Text(
            f"{self.remaining}s",
            size=32,
            weight="bold",
            color=PRIMARY,
        )

        # Progress ring
        self.progress = ft.ProgressRing(
            value=0,
            color=PRIMARY,
            bgcolor=ACCENT,
            stroke_width=6,
        )

        # Control buttons with icons
        self.start_btn = ft.ElevatedButton(
            "Start",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_timer,
            bgcolor=PRIMARY,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        )

        self.pause_btn = ft.ElevatedButton(
            "Pause",
            icon=ft.Icons.PAUSE,
            on_click=self.pause_timer,
            bgcolor=ACCENT,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        )

        self.reset_btn = ft.ElevatedButton(
            "Reset",
            icon=ft.Icons.RESTART_ALT,
            on_click=self.reset_timer,
            bgcolor=ft.Colors.PINK_200,
            color=ft.Colors.BLACK,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        )

        # Inner card layout
        card = ft.Container(
            bgcolor=CARD_BG,
            border_radius=20,
            padding=30,
            shadow=ft.BoxShadow(
                blur_radius=16,
                spread_radius=2,
                color=ft.Colors.BLACK12,
            ),
            content=ft.Column(
                [
                    ft.Text(self.label, size=28, weight="bold", color=PRIMARY),
                    ft.Container(height=10),
                    self.input_value,
                    ft.Container(
                        content=self.progress,
                        alignment=ft.alignment.center,
                        padding=20,
                    ),
                    self.time_text,
                    ft.Container(height=20),
                    ft.Row(
                        [self.start_btn, self.pause_btn, self.reset_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        # Column (this widget) layout
        self.controls = [
            ft.Container(
                content=card,
                alignment=ft.alignment.center,
            )
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.START

    # -----------------------------
    #       Async timer logic
    # -----------------------------
    async def countdown_task(self):
        """Async countdown loop."""
        self.running = True

        while self.running and self.remaining > 0:
            await asyncio.sleep(1)
            self.remaining -= 1

            self.time_text.value = f"{self.remaining}s"
            # Avoid division by zero
            if self.initial_value > 0:
                self.progress.value = 1 - (self.remaining / self.initial_value)
            else:
                self.progress.value = 0
            self.page.update()

        self.running = False

    def start_timer(self, e):
        """Start the timer asynchronously."""
        if not self.running:
            try:
                self.initial_value = int(self.input_value.value)
            except ValueError:
                self.initial_value = 30

            self.remaining = self.initial_value
            self.running = True
            self.page.run_task(self.countdown_task)

    def pause_timer(self, e):
        """Pause the timer."""
        self.running = False

    def reset_timer(self, e):
        """Reset timer to initial start value."""
        self.running = False
        self.remaining = self.initial_value
        self.time_text.value = f"{self.remaining}s"
        self.progress.value = 0
        self.page.update()


# --------------------------------------
#                MAIN APP
# --------------------------------------
def main(page: ft.Page):
    page.title = "Async Multi Countdown Timer"
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.LIGHT

    # Create three independent timers
    timer1 = CountdownTimer(page, "Timer 1")
    timer2 = CountdownTimer(page, "Timer 2")
    timer3 = CountdownTimer(page, "Timer 3")

    # Tabs control with 3 timers
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=250,
        expand=1,
        tabs=[
            ft.Tab(
                text="Timer 1",
                icon=ft.Icons.LOOKS_ONE,
                content=timer1,
            ),
            ft.Tab(
                text="Timer 2",
                icon=ft.Icons.LOOKS_TWO,
                content=timer2,
            ),
            ft.Tab(
                text="Timer 3",
                icon=ft.Icons.LOOKS_3,
                content=timer3,
            ),
        ],
    )

    # Navigation Drawer: try switching timers via drawer as well
    def drawer_change(e):
        idx = e.control.selected_index
        if idx is not None:
            tabs.selected_index = idx
            page.update()

    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER, label="Timer 1"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER, label="Timer 2"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER, label="Timer 3"
            ),
        ],
        on_change=drawer_change,
    )

    # App bar with menu icon to open drawer
    page.appbar = ft.AppBar(
        title=ft.Text("Async Countdown Timers"),
        bgcolor=PRIMARY,
        color=ft.Colors.WHITE,
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_color=ft.Colors.WHITE,
            on_click=lambda _: page.open(drawer),
        ),
    )

    # Main content: just the Tabs
    page.add(tabs)


# Run in web browser (good for async)
ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    port=8900,
)
