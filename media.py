import webbrowser


class Moive(object):
  """Movie class for all the movies that will show on the website.

  Attributes:
      moive_title: A string indicating movie's title.
      movie_storyline: A sting indicating the movie's description.
      movie_image: A string of url of the movie's post.
      movie_youtube: A string of url of movie's trailer on youtube.
  """
  def __init__(self, moive_title, movie_storyline, movie_image, movie_youtube):
    self.title = moive_title
    self.storyline = movie_storyline
    self.image = movie_image
    self.youtube = movie_youtube

  def show_trailer(self):
    webbrowser.open(self.youtube)
