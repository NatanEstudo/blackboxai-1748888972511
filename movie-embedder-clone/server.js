const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Mock movie data
const movies = [
  {
    id: 1,
    title: "The Shawshank Redemption",
    category: "Drama",
    genre: "Drama",
    quality: "HD",
    language: "English",
    country: "USA",
    thumbnail: "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4"
  },
  {
    id: 2,
    title: "The Godfather",
    category: "Crime",
    genre: "Crime, Drama",
    quality: "HD",
    language: "English",
    country: "USA",
    thumbnail: "https://image.tmdb.org/t/p/w500/eEslKSwcqmiNS6va24Pbxf2UKmJ.jpg",
    videoUrl: "https://www.w3schools.com/html/movie.mp4"
  },
  {
    id: 3,
    title: "The Dark Knight",
    category: "Action",
    genre: "Action, Crime, Drama",
    quality: "HD",
    language: "English",
    country: "USA",
    thumbnail: "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4"
  },
  {
    id: 4,
    title: "Inception",
    category: "Sci-Fi",
    genre: "Action, Sci-Fi, Thriller",
    quality: "HD",
    language: "English",
    country: "USA",
    thumbnail: "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
    videoUrl: "https://www.w3schools.com/html/movie.mp4"
  },
  {
    id: 5,
    title: "Pulp Fiction",
    category: "Crime",
    genre: "Crime, Drama",
    quality: "HD",
    language: "English",
    country: "USA",
    thumbnail: "https://image.tmdb.org/t/p/w500/dM2w364MScsjFf8pfMbaWUcWrR.jpg",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4"
  }
];

// API endpoint to get all movies
app.get('/api/movies', (req, res) => {
  res.json(movies);
});

// API endpoint to get movie by id
app.get('/api/movies/:id', (req, res) => {
  const movie = movies.find(m => m.id === parseInt(req.params.id));
  if (movie) {
    res.json(movie);
  } else {
    res.status(404).json({ message: "Movie not found" });
  }
});

app.listen(port, () => {
  console.log(`Movie embedder backend listening at http://localhost:${port}`);
});
