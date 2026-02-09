# -*- coding: utf-8 -*-
import os
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle

EMOJIS = [
    "??", "?", "??", "??",
    "??", "??", "??", "??"
]

QUESTIONS = [
    "Will you be my Valentine? ??",
    "Are you sureee? ??",
    "Like... really really sure? ??",
    "Okay last chance ??",
    "Yayyy ????",
]

BOOK_PAGES = [
    {
        "image": "p1.jpg",
        "text": (
            "I still remember the very first time we talked. It didn't feel extraordinary at that moment, "
            "yet something about it stayed with me in a quiet way. Your words felt natural, effortless, "
            "as if they belonged there all along. That simple beginning slowly turned into something "
            "meaningful without making any noise. Looking back now, I realize that moment gently marked "
            "the start of a story I never knew I would care so deeply about."
        ),
    },
    {
        "image": "p2.jpg",
        "text": (
            "With time, you became comfort - the kind that doesn't need explanation. "
            "Your presence made ordinary moments feel lighter and calmer. Even when nothing special "
            "was happening, having you around felt enough. Somewhere between small conversations "
            "and quiet pauses, you became a constant thought. Not loud, not demanding - just there, "
            "steadily making everything feel a little better."
        ),
    },
    {
        "image": "p3.jpg",
        "text": (
            "There were moments when everything felt calm simply because you existed in my world. "
            "Your laughter had its own warmth, and your silence never felt empty. "
            "You didn't change things suddenly or dramatically - you changed them slowly, "
            "softly, and in a way that stayed. Without realizing it, you became someone "
            "who mattered more than words could explain."
        ),
    },
    {
        "image": "p4.jpg",
        "text": (
            "Some people pass through our lives as memories. Others stay as lessons. "
            "But you became something different - a feeling I carry with me. "
            "You became the chapter I never want to skip, the part of the story "
            "that feels real and irreplaceable. With you, even silence feels meaningful, "
            "and time feels kinder."
        ),
    },
    {
        "image": "p2.jpg",
        "text": (
            "If love had a place, it would feel like this - calm, honest, and safe. "
            "Not perfect, but real in the most beautiful way. Being here feels like home, "
            "not because everything is easy, but because it's genuine. And if life ever "
            "gave me the chance to choose again, I wouldn't hesitate. "
            "I would still choose you - every time. ??"
        ),
    },
]

COMPLIMENTS = [
    "You are magic",
    "So sweet",
    "Cutie",
    "You make me smile",
    "My favorite",
    "Always you",
    "Lovely",
    "Heart stealer",
]


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PICS_DIR = os.path.join(ASSETS_DIR, "pics")
MUSIC_PATH = os.path.join(ASSETS_DIR, "music", "song.mp3")


class Background(FloatLayout):
    def __init__(self, color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class FloatingEmoji(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = random.choice(EMOJIS)
        self.font_size = random.randint(22, 30)
        self.size_hint = (None, None)
        self.texture_update()
        self.size = self.texture_size
        self.x = random.randint(0, int(Window.width - self.width))
        self.y = Window.height
        Clock.schedule_interval(self._move, 1 / 30.0)

    def _move(self, dt):
        self.y -= random.randint(1, 3)
        if self.y < -50:
            self.parent.remove_widget(self)
            return False
        return True


class BurstEmoji(Label):
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.text = random.choice(EMOJIS)
        self.font_size = 26
        self.size_hint = (None, None)
        self.texture_update()
        self.size = self.texture_size
        self.x = x
        self.y = y
        self.dx = random.randint(-4, 4)
        self.dy = random.randint(3, 7)
        Clock.schedule_interval(self._move, 1 / 60.0)

    def _move(self, dt):
        self.x += self.dx
        self.y += self.dy
        self.dy -= 0.25
        if self.y < -50 or self.y > Window.height + 50:
            self.parent.remove_widget(self)
            return False
        return True


class RainEmoji(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = random.choice(EMOJIS)
        self.font_size = random.randint(20, 30)
        self.size_hint = (None, None)
        self.texture_update()
        self.size = self.texture_size
        self.x = random.randint(0, int(Window.width - self.width))
        self.y = Window.height + random.randint(20, 200)
        self.speed = random.randint(2, 6)

    def fall(self):
        self.y -= self.speed


class EmojiRainOverlay(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.emojis = []
        self.spawn_ev = Clock.schedule_interval(self._spawn, 0.18)
        self.tick_ev = Clock.schedule_interval(self._tick, 1 / 30.0)

    def _spawn(self, dt):
        e = RainEmoji()
        self.emojis.append(e)
        self.add_widget(e)

    def _tick(self, dt):
        for e in self.emojis[:]:
            e.fall()
            if e.y < -60:
                self.emojis.remove(e)
                self.remove_widget(e)

    def stop(self):
        if self.spawn_ev:
            self.spawn_ev.cancel()
            self.spawn_ev = None
        if self.tick_ev:
            self.tick_ev.cancel()
            self.tick_ev = None
        self.clear_widgets()
        self.emojis.clear()


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = Background(color=(1, 0.88, 0.91, 1))
        self.add_widget(root)

        self.title = Label(text="A tiny question...", size_hint=(1, None), height=40, pos_hint={"x": 0, "top": 0.98},
                           font_size=22, color=(0.48, 0.12, 0.24, 1))
        root.add_widget(self.title)

        self.subtitle = Label(text="Made with a little courage and a lot of heart", size_hint=(1, None), height=24,
                              pos_hint={"x": 0, "top": 0.92}, font_size=13, color=(0.58, 0.26, 0.36, 1))
        root.add_widget(self.subtitle)

        self.pics = [
            os.path.join(PICS_DIR, "p1.jpg"),
            os.path.join(PICS_DIR, "p2.jpg"),
            os.path.join(PICS_DIR, "p3.jpg"),
            os.path.join(PICS_DIR, "p4.jpg"),
        ]
        self.pic_index = 0
        self.pic = Image(source=self.pics[0], size_hint=(None, None), size=(240, 240),
                         pos_hint={"center_x": 0.5, "center_y": 0.62})
        root.add_widget(self.pic)

        self.q_index = 0
        self.btn = Button(text=QUESTIONS[0], size_hint=(None, None), size=(340, 60),
                          pos_hint={"center_x": 0.5, "center_y": 0.26},
                          background_color=(1, 0.3, 0.43, 1), color=(1, 1, 1, 1))
        self.btn.bind(on_press=self.on_click)
        root.add_widget(self.btn)

        self.no_btn = Button(text="Not yet", size_hint=(None, None), size=(140, 40),
                             pos_hint={"center_x": 0.5, "center_y": 0.16},
                             background_color=(1, 1, 1, 1), color=(0.48, 0.12, 0.24, 1))
        self.no_btn.bind(on_press=self.move_no_btn)
        root.add_widget(self.no_btn)

        self.mute_btn = ToggleButton(text="Mute", size_hint=(None, None), size=(80, 30),
                                     pos_hint={"right": 0.98, "top": 0.98})
        self.mute_btn.bind(on_press=self.toggle_mute)
        root.add_widget(self.mute_btn)

        self.rain_btn = ToggleButton(text="Rain", size_hint=(None, None), size=(80, 30),
                                     pos_hint={"right": 0.98, "top": 0.92})
        self.rain_btn.bind(on_press=self.toggle_rain)
        root.add_widget(self.rain_btn)

        self.rain = None
        self.pulse = Animation(size=(350, 66), duration=0.6) + Animation(size=(340, 60), duration=0.6)
        self.pulse.repeat = True
        self.pulse.start(self.btn)

        Clock.schedule_interval(self.animate_pic_change, 3.0)
        Clock.schedule_interval(self.spawn_emoji, 0.6)

    def animate_pic_change(self, dt):
        self.pic_index = (self.pic_index + 1) % len(self.pics)
        self.pic.source = self.pics[self.pic_index]

    def spawn_emoji(self, dt):
        self.add_widget(FloatingEmoji())

    def move_no_btn(self, *args):
        x = random.uniform(0.1, 0.7)
        y = random.uniform(0.10, 0.20)
        self.no_btn.pos_hint = {"x": x, "y": y}

    def on_click(self, *args):
        for _ in range(6):
            self.add_widget(BurstEmoji(self.btn.center_x, self.btn.center_y))
        if self.q_index < len(QUESTIONS) - 1:
            self.q_index += 1
            self.btn.text = QUESTIONS[self.q_index]
        else:
            self.manager.current = "book"

    def toggle_rain(self, *args):
        if self.rain_btn.state == "down":
            if not self.rain:
                self.rain = EmojiRainOverlay()
                self.add_widget(self.rain)
        else:
            if self.rain:
                self.rain.stop()
                self.remove_widget(self.rain)
                self.rain = None

    def toggle_mute(self, *args):
        App.get_running_app().set_muted(self.mute_btn.state == "down")


class BookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = Background(color=(0.16, 0.16, 0.16, 1))
        self.add_widget(root)

        self.title = Label(text="Tap photo to zoom", size_hint=(1, None), height=24,
                           pos_hint={"x": 0, "top": 0.98}, font_size=14, color=(0.8, 0.7, 0.7, 1))
        root.add_widget(self.title)

        self.card = FloatLayout(size_hint=(None, None), size=(0.85 * Window.width, 0.75 * Window.height),
                                pos_hint={"center_x": 0.5, "center_y": 0.52})
        with self.card.canvas.before:
            Color(1, 0.97, 0.94, 1)
            self.card_bg = RoundedRectangle(pos=self.card.pos, size=self.card.size, radius=[20])
        self.card.bind(pos=self._update_card, size=self._update_card)
        root.add_widget(self.card)

        self.image = Image(size_hint=(None, None), size=(self.card.width * 0.88, self.card.height * 0.45),
                           pos_hint={"center_x": 0.5, "top": 0.96})
        self.card.add_widget(self.image)
        self.image.bind(on_touch_down=self.on_image_touch)
        self.image_zoomed = False

        self.text = Label(text="", size_hint=(None, None), size=(self.card.width * 0.88, self.card.height * 0.40),
                          pos_hint={"center_x": 0.5, "y": 0.05}, color=(0.2, 0.2, 0.2, 1),
                          text_size=(self.card.width * 0.88, None), halign="left", valign="top")
        self.text.bind(texture_size=self._update_text_height)
        self.card.add_widget(self.text)

        self.progress = Label(text="", size_hint=(1, None), height=20,
                              pos_hint={"x": 0, "y": 0.08}, font_size=12, color=(0.8, 0.7, 0.7, 1))
        root.add_widget(self.progress)

        self.btn_prev = Button(text="Back", size_hint=(None, None), size=(120, 44),
                               pos_hint={"x": 0.08, "y": 0.02}, background_color=(1, 1, 1, 1), color=(0.3, 0.3, 0.3, 1))
        self.btn_prev.bind(on_press=self.prev_page)
        root.add_widget(self.btn_prev)

        self.btn_next = Button(text="Next ?", size_hint=(None, None), size=(120, 44),
                               pos_hint={"right": 0.92, "y": 0.02}, background_color=(1, 0.3, 0.43, 1), color=(1, 1, 1, 1))
        self.btn_next.bind(on_press=self.flip)
        root.add_widget(self.btn_next)

        self.mute_btn = ToggleButton(text="Mute", size_hint=(None, None), size=(80, 30),
                                     pos_hint={"right": 0.98, "top": 0.98})
        self.mute_btn.bind(on_press=self.toggle_mute)
        root.add_widget(self.mute_btn)

        self.rain_btn = ToggleButton(text="Rain", size_hint=(None, None), size=(80, 30),
                                     pos_hint={"right": 0.98, "top": 0.92})
        self.rain_btn.bind(on_press=self.toggle_rain)
        root.add_widget(self.rain_btn)

        self.rain = None
        self.index = 0
        self.load_page()

    def _update_card(self, *args):
        self.card_bg.pos = self.card.pos
        self.card_bg.size = self.card.size

    def _update_text_height(self, *args):
        self.text.height = max(self.text.texture_size[1], self.card.height * 0.40)

    def load_page(self):
        page = BOOK_PAGES[self.index]
        self.image.source = os.path.join(PICS_DIR, page["image"])
        self.text.text = page["text"]
        self.progress.text = "Page {} of {}".format(self.index + 1, len(BOOK_PAGES))
        self.btn_prev.disabled = self.index == 0
        if self.index >= len(BOOK_PAGES) - 1:
            self.btn_next.text = "Continue ?"
        else:
            self.btn_next.text = "Next ?"

    def on_image_touch(self, instance, touch):
        if not self.image.collide_point(*touch.pos):
            return False
        if self.image_zoomed:
            Animation(size=(self.card.width * 0.88, self.card.height * 0.45), duration=0.2).start(self.image)
            self.image_zoomed = False
        else:
            Animation(size=(self.card.width * 0.94, self.card.height * 0.55), duration=0.2).start(self.image)
            self.image_zoomed = True
        for _ in range(6):
            self.add_widget(BurstEmoji(touch.x, touch.y))
        return True

    def flip(self, *args):
        if self.index >= len(BOOK_PAGES) - 1:
            self.manager.current = "game"
            return
        self.next_page()

    def next_page(self, *args):
        self.index += 1
        self.load_page()

    def prev_page(self, *args):
        if self.index <= 0:
            return
        self.index -= 1
        self.load_page()

    def toggle_rain(self, *args):
        if self.rain_btn.state == "down":
            if not self.rain:
                self.rain = EmojiRainOverlay()
                self.add_widget(self.rain)
        else:
            if self.rain:
                self.rain.stop()
                self.remove_widget(self.rain)
                self.rain = None

    def toggle_mute(self, *args):
        App.get_running_app().set_muted(self.mute_btn.state == "down")


class FallingHeart(Label):
    def __init__(self, kind="heart", **kwargs):
        super().__init__(**kwargs)
        self.kind = kind
        if kind == "gold":
            self.text = "??"
            self.font_size = 32
        elif kind == "bomb":
            self.text = "??"
            self.font_size = 30
        else:
            self.text = random.choice(["??", "??", "??", "??", "??"])
            self.font_size = 30
        self.size_hint = (None, None)
        self.texture_update()
        self.size = self.texture_size
        self.speed = random.randint(3, 7)

    def fall(self):
        self.y -= self.speed


class FloatingText(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = random.choice(COMPLIMENTS)
        self.font_size = 14
        self.color = (0.94, 0.65, 0.72, 1)
        self.size_hint = (None, None)
        self.texture_update()
        self.size = self.texture_size
        self.x = random.randint(0, int(Window.width - self.width))
        self.y = Window.height + random.randint(0, 200)
        self.speed = random.randint(1, 3)

    def float_up(self):
        self.y -= self.speed


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = Background(color=(1, 0.93, 0.95, 1))
        self.add_widget(root)

        self.title = Label(text="Catch hearts! Max score: 100", size_hint=(1, None), height=30,
                           pos_hint={"x": 0, "top": 0.98}, font_size=18, color=(0.48, 0.12, 0.24, 1))
        root.add_widget(self.title)

        self.counter = Label(text="Score: 0", size_hint=(None, None), size=(160, 24),
                             pos_hint={"x": 0.05, "top": 0.92}, color=(0.48, 0.12, 0.24, 1))
        root.add_widget(self.counter)

        self.timer_label = Label(text="Time: 20", size_hint=(None, None), size=(100, 24),
                                 pos_hint={"right": 0.95, "top": 0.92}, color=(0.48, 0.12, 0.24, 1))
        root.add_widget(self.timer_label)

        self.start_btn = Button(text="Start", size_hint=(None, None), size=(140, 44),
                                pos_hint={"center_x": 0.5, "y": 0.02})
        self.start_btn.bind(on_press=self.start_game)
        root.add_widget(self.start_btn)

        self.next_btn = Button(text="Next ?", size_hint=(None, None), size=(140, 44),
                               pos_hint={"right": 0.95, "y": 0.02})
        self.next_btn.bind(on_press=self.open_next)
        self.next_btn.opacity = 0
        self.next_btn.disabled = True
        root.add_widget(self.next_btn)

        self.tray = Label(text="==========", size_hint=(None, None))
        self.tray.font_size = 22
        self.tray.texture_update()
        self.tray.size = self.tray.texture_size
        self.tray.y = 80
        self.tray.center_x = Window.width / 2
        root.add_widget(self.tray)

        self.hearts = []
        self.texts = []
        self.score = 0
        self.time_left = 20

        self.spawn_ev = None
        self.fall_ev = None
        self.clock_ev = None
        self.text_ev = None

    def start_game(self, *args):
        self.score = 0
        self.time_left = 20
        self.update_hud()
        self.start_btn.disabled = True
        self.next_btn.opacity = 0
        self.next_btn.disabled = True

        self.spawn_ev = Clock.schedule_interval(self.spawn_heart, 0.5)
        self.fall_ev = Clock.schedule_interval(self.tick, 1 / 30.0)
        self.clock_ev = Clock.schedule_interval(self.countdown, 1.0)
        self.text_ev = Clock.schedule_interval(self.spawn_text, 0.6)

    def spawn_heart(self, dt):
        x = random.randint(30, int(Window.width - 30))
        roll = random.random()
        if roll < 0.12:
            kind = "gold"
        elif roll < 0.22:
            kind = "bomb"
        else:
            kind = "heart"
        h = FallingHeart(kind=kind)
        h.x = x
        h.y = Window.height
        self.hearts.append(h)
        self.add_widget(h)

    def tick(self, dt):
        for h in self.hearts[:]:
            h.fall()
            if h.y <= self.tray.y + 10 and h.y >= self.tray.y - 10:
                if h.x + h.width >= self.tray.x and h.x <= self.tray.x + self.tray.width:
                    self.remove_widget(h)
                    self.hearts.remove(h)
                    if h.kind == "gold":
                        self.score += 3
                    elif h.kind == "bomb":
                        self.score = max(0, self.score - 2)
                    else:
                        self.score += 1
                    self.score = min(100, self.score)
                    self.update_hud()
                    continue
            if h.y < -40:
                self.remove_widget(h)
                self.hearts.remove(h)

        for t in self.texts[:]:
            t.float_up()
            if t.y < -40:
                self.remove_widget(t)
                self.texts.remove(t)

    def countdown(self, dt):
        self.time_left -= 1
        self.update_hud()
        if self.time_left <= 0 or self.score >= 100:
            self.end_game()

    def update_hud(self):
        self.counter.text = "Score: {}".format(self.score)
        self.timer_label.text = "Time: {}".format(self.time_left)

    def end_game(self):
        if self.spawn_ev:
            self.spawn_ev.cancel()
        if self.fall_ev:
            self.fall_ev.cancel()
        if self.clock_ev:
            self.clock_ev.cancel()
        if self.text_ev:
            self.text_ev.cancel()
        self.spawn_ev = self.fall_ev = self.clock_ev = self.text_ev = None
        for h in self.hearts:
            self.remove_widget(h)
        self.hearts.clear()
        for t in self.texts:
            self.remove_widget(t)
        self.texts.clear()
        self.start_btn.disabled = False
        self.next_btn.opacity = 1
        self.next_btn.disabled = False

    def spawn_text(self, dt):
        t = FloatingText()
        self.texts.append(t)
        self.add_widget(t)

    def on_touch_move(self, touch):
        if touch.y < self.tray.y + 80:
            self.tray.center_x = touch.x
        return super().on_touch_move(touch)

    def on_touch_down(self, touch):
        if touch.y < self.tray.y + 80:
            self.tray.center_x = touch.x
        return super().on_touch_down(touch)

    def open_next(self, *args):
        self.manager.current = "gallery"


class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = Background(color=(1, 0.96, 0.96, 1))
        self.add_widget(root)

        self.title = Label(text="Our Gallery", size_hint=(1, None), height=30,
                           pos_hint={"x": 0, "top": 0.98}, font_size=18, color=(0.48, 0.12, 0.24, 1))
        root.add_widget(self.title)

        self.frame = FloatLayout(size_hint=(None, None), size=(0.85 * Window.width, 0.65 * Window.height),
                                 pos_hint={"center_x": 0.5, "center_y": 0.55})
        with self.frame.canvas.before:
            Color(1, 1, 1, 1)
            self.frame_bg = RoundedRectangle(pos=self.frame.pos, size=self.frame.size, radius=[18])
        self.frame.bind(pos=self._update_frame, size=self._update_frame)
        root.add_widget(self.frame)

        self.image = Image(size_hint=(None, None), size=(self.frame.width * 0.9, self.frame.height * 0.88),
                           pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.frame.add_widget(self.image)

        self.caption = Label(text="", size_hint=(1, None), height=24,
                             pos_hint={"x": 0, "y": 0.18}, color=(0.48, 0.12, 0.24, 1))
        root.add_widget(self.caption)

        self.dots = Label(text="", size_hint=(1, None), height=20,
                          pos_hint={"x": 0, "y": 0.14}, color=(0.76, 0.47, 0.55, 1))
        root.add_widget(self.dots)

        self.prev_btn = Button(text="Back", size_hint=(None, None), size=(120, 44),
                               pos_hint={"x": 0.08, "y": 0.02}, background_color=(1, 1, 1, 1), color=(0.48, 0.12, 0.24, 1))
        self.prev_btn.bind(on_press=self.prev)
        root.add_widget(self.prev_btn)

        self.next_btn = Button(text="Next", size_hint=(None, None), size=(120, 44),
                               pos_hint={"right": 0.92, "y": 0.02}, background_color=(1, 0.3, 0.43, 1), color=(1, 1, 1, 1))
        self.next_btn.bind(on_press=self.next)
        root.add_widget(self.next_btn)

        self.final_btn = Button(text="Final ?", size_hint=(None, None), size=(140, 44),
                                pos_hint={"center_x": 0.5, "y": 0.02}, background_color=(0.48, 0.12, 0.24, 1), color=(1, 1, 1, 1))
        self.final_btn.bind(on_press=self.open_final)
        root.add_widget(self.final_btn)

        self.pics = self._load_pics()
        self.index = 0
        self.load_image()

    def _update_frame(self, *args):
        self.frame_bg.pos = self.frame.pos
        self.frame_bg.size = self.frame.size

    def _load_pics(self):
        pics = []
        for f in sorted(os.listdir(PICS_DIR)):
            ext = os.path.splitext(f)[1].lower()
            if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                pics.append(os.path.join(PICS_DIR, f))
        if not pics:
            pics = [os.path.join(PICS_DIR, "p1.jpg")]
        return pics

    def load_image(self):
        self.image.source = self.pics[self.index]
        self.caption.text = "Photo {} of {}".format(self.index + 1, len(self.pics))
        dots = ["?" if i == self.index else "?" for i in range(len(self.pics))]
        self.dots.text = "  ".join(dots)

    def prev(self, *args):
        self.index = (self.index - 1) % len(self.pics)
        self.load_image()

    def next(self, *args):
        self.index = (self.index + 1) % len(self.pics)
        self.load_image()

    def open_final(self, *args):
        self.manager.current = "final"


class FullScreenEmojiBurst(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(120):
            e = Label(text=random.choice(EMOJIS), font_size=28, size_hint=(None, None))
            e.texture_update()
            e.size = e.texture_size
            e.x = random.randint(0, int(Window.width - e.width))
            e.y = random.randint(0, int(Window.height - e.height))
            self.add_widget(e)


class FinalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = Background(color=(0.17, 0.04, 0.11, 1))
        self.add_widget(root)

        self.title = Label(text="One last thing...", size_hint=(1, None), height=40,
                           pos_hint={"x": 0, "top": 0.98}, font_size=20, color=(0.97, 0.85, 0.88, 1))
        root.add_widget(self.title)

        self.card = FloatLayout(size_hint=(None, None), size=(0.78 * Window.width, 0.45 * Window.height),
                                pos_hint={"center_x": 0.5, "center_y": 0.55})
        with self.card.canvas.before:
            Color(1, 0.94, 0.96, 1)
            self.card_bg = RoundedRectangle(pos=self.card.pos, size=self.card.size, radius=[18])
        self.card.bind(pos=self._update_card, size=self._update_card)
        root.add_widget(self.card)

        self.heart = Label(text="??", size_hint=(1, None), height=50,
                           pos_hint={"x": 0, "top": 0.95}, font_size=28)
        self.card.add_widget(self.heart)

        self.question = Label(text="Will you be my Valentine?", size_hint=(1, None), height=60,
                              pos_hint={"x": 0, "top": 0.75}, font_size=18, color=(0.48, 0.12, 0.24, 1))
        self.card.add_widget(self.question)

        self.yes_btn = Button(text="Yes!", size_hint=(None, None), size=(110, 44),
                              pos_hint={"center_x": 0.35, "y": 0.15}, background_color=(1, 0.3, 0.43, 1), color=(1, 1, 1, 1))
        self.yes_btn.bind(on_press=self.celebrate)
        self.card.add_widget(self.yes_btn)

        self.no_btn = Button(text="Not yet", size_hint=(None, None), size=(110, 44),
                             pos_hint={"center_x": 0.65, "y": 0.15}, background_color=(1, 1, 1, 1), color=(0.48, 0.12, 0.24, 1))
        self.no_btn.bind(on_press=self.dodge)
        self.card.add_widget(self.no_btn)

        self.msg = Label(text="", size_hint=(1, None), height=30,
                         pos_hint={"x": 0, "y": 0.2}, font_size=14, color=(0.97, 0.85, 0.88, 1))
        root.add_widget(self.msg)

        Clock.schedule_interval(self.drop_emoji, 0.4)

    def _update_card(self, *args):
        self.card_bg.pos = self.card.pos
        self.card_bg.size = self.card.size

    def dodge(self, *args):
        x = random.uniform(0.1, 0.7)
        y = random.uniform(0.05, 0.22)
        self.no_btn.pos_hint = {"x": x, "y": y}

    def celebrate(self, *args):
        self.msg.text = "Yayyyy! ??"
        burst = FullScreenEmojiBurst()
        self.add_widget(burst)
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 3.0)

    def drop_emoji(self, dt):
        e = Label(text=random.choice(EMOJIS), font_size=22, size_hint=(None, None))
        e.texture_update()
        e.size = e.texture_size
        e.x = random.randint(0, int(Window.width - e.width))
        e.y = Window.height
        self.add_widget(e)
        Animation(y=-50, duration=1.2).start(e)
        Clock.schedule_once(lambda _dt: self.remove_widget(e), 1.25)


class ValentineApp(App):
    def build(self):
        self.sound = SoundLoader.load(MUSIC_PATH)
        if self.sound:
            self.sound.loop = True
            self.sound.volume = 0.4
            self.sound.play()

        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(BookScreen(name="book"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GalleryScreen(name="gallery"))
        sm.add_widget(FinalScreen(name="final"))
        sm.current = "start"
        return sm

    def set_muted(self, muted):
        if not self.sound:
            return
        self.sound.volume = 0.0 if muted else 0.4


if __name__ == "__main__":
    ValentineApp().run()
