from theapp.models import Series

books = {
  "1": {
    "title": "Demon Lord! Retry!",
    "author": "Kurone Kanzaki",
    "genre": "Fantasy, Isekai",
    "publisher": "Futabasha"
  },
  "2": {
    "title": "Fantasy Inbound",
    "author": "Joe Takeduki",
    "genre": "Action, Romance, Sci-fi, Fantasy",
    "publisher": "J-Novel Club"
  },
  "3": {
    "title": "Frieren",
    "author": "Kanehito Yamada",
    "genre": "Fantasy",
    "publisher": "Shogakukan"
  },
  "4": {
    "title": "Gekkou",
    "author": "Mamiya Natsuki",
    "genre": "Comedy, Mystery, Romance",
    "publisher": "ASCII Media Works"
  },
  "5": {
    "title": "Goblin Slayer",
    "author": "Kumo Kagyu",
    "genre": "Adventure, Dark Fantasy",
    "publisher": "SB Creative"
  },
  "6": {
    "title": "Grand Blue Dreaming",
    "author": "Kenji Inoue",
    "genre": "Comedy",
    "publisher": "Kodansha"
  },
  "7": {
    "title": "Hai to Gensou no Grimgar",
    "author": "Ao Jyumonji",
    "genre": "Action, Adventure, Drama, Fantasy",
    "publisher": "Overlap"
  },
  "8": {
    "title": "Haibara's Teenage New Game!",
    "author": "Kazuki Amamiya",
    "genre": "Comedy, Romance",
    "publisher": "Unknown"
  },
  "9": {
    "title": "Hollow Regalia",
    "author": "Gakuto Mikumo",
    "genre": "Fantasy",
    "publisher": "ASCII Media Works"
  },
  "10": {
    "title": "I Had That Same Dream Again",
    "author": "Yoru Sumino",
    "genre": "Drama, Slice of Life",
    "publisher": "Futabasha"
  }
}

for book in books:
    print(book)