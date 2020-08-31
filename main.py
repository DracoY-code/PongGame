import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty,
                             ReferenceListProperty)
from kivy.uix.widget import Widget
from kivy.vector import Vector


class PongBall(Widget):
    """ The Ball Class. """

    # Velocity of ball
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Reference to velocity of ball
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self) -> None:
        """This method changes position of the ball.
        """
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    """ The Class for the players and their paddles. """

    # Score of the player
    score = NumericProperty(0)

    def bounce_ball(self, ball: PongBall) -> None:
        """This method is called when the ball hits the paddle.

        - ball: PongBall {The pong ball to be bounced back}
        """
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    # The ball
    ball = ObjectProperty(None)

    # The players
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel:tuple=(4, 0)) -> None:
        """This method puts the ball at its starting position.

        - vel: tuple = (4, 0) {The velocity values of the ball}
        """
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, *args) -> None:
        """This method updates the screen after an interval of time.
        """

        # Move the ball
        self.ball.move()

        # Bounce off the paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Bounce off the bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # Track score of the players
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch) -> None:
        """This method reads the touch and updates the screen.

        - touch {The touch event on the screen}
        """
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width * 2 / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    """ The Main Pong Class. """

    def build(self) -> PongGame:
        """The main build method.
        """
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    # Run the application
    PongApp().run()