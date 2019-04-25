import media
import fresh_tomatoes

# These are the movie instances
mobie_toy_story = media.Moive(
  'Toy Story',
  'A story of a boy and his toys that come to life.',
  'https://images-na.ssl-images-amazon.com/images/I/91g2fEXursL._RI_SX200_.jpg',  # noqa
  'https://www.youtube.com/watch?v=KYz2wyBy3kc')

mobie_avatar = media.Moive(
  'Avatar',
  'A marine on an alien planet.',
  'https://image.tmdb.org/t/p/w600_and_h900_bestv2/kmcqlZGaSh20zpTbuoF0Cdn07dT.jpg',  # noqa
  'https://www.youtube.com/watch?v=5PSNL1qE6VY')

mobie_jurassic = media.Moive(
  'Jurassic World: Fallen Kingdom',
  'A world with dinosaurs living in a modern society.',
  'https://image.tmdb.org/t/p/w600_and_h900_bestv2/c9XxwwhPHdaImA2f1WEfEsbhaFB.jpg',  # noqa
  'https://www.youtube.com/watch?v=vn9mMeWcgoM')

mobie_incredibles = media.Moive(
  'Incredibles 2',
  'Mr. Incredible is taking care of the problems of his three children.',
  'https://image.tmdb.org/t/p/w600_and_h900_bestv2/hL9Uz2vq93vi20oxZEBBaSs4w8U.jpg',  # noqa
  'https://www.youtube.com/watch?v=i5qOzqD9Rms')

mobie_deadpool = media.Moive(
  'Deadpool 2',
  'Wisecracking mercenary Deadpool battles the evil and powerful Cable and other bad guys to save a boy\'s life.',  # noqa
  'https://image.tmdb.org/t/p/w600_and_h900_bestv2/to0spRl1CMDvyUbOnbb4fTk3VAd.jpg',  # noqa
  'https://www.youtube.com/watch?v=D86RtevtfrA')

# Construct a list of all movies
movies = [mobie_toy_story, mobie_avatar, mobie_jurassic, mobie_incredibles, mobie_deadpool]  # noqa

# start the program.
fresh_tomatoes.open_movies_page(movies)
