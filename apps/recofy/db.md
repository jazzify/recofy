

## [Intro] Double-think DB Queries

Let's say we have an `Artist` model that makes music of some `Genre`s:
```python
class Genre(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class Artist(BaseModel):
    name = models.CharField(max_length=255)
    popularity = models.PositiveSmallIntegerField()
    genres = models.ManyToManyField(Genre) # All artist genres
```

For our example, the client should be able to dynamically add new genres at the artist creation point, now a little constraint here is that we shouldn't include duplicate genres in our db, that should be an easy task, our first implementation could look like this:
```python
# Clean our database to ensure all runs are the same
Genre.objects.all().delete()
Artist.objects.all().delete()

client_input_data = [
    "latin alternative", "latin pop",
    "latin rock", "mexican rock",
    "nu-cumbia", "rock en espanol", "rock urbano mexicano"
] # 7 total genres

genre_set = []
for genre in client_input_data:
    genre = Genre.objects.create(name=genre)
    # ... Some data processing
    genre.full_clean()
    genre.save()
    genre_set.append(genre)

artist, created = Artist.objects.create(
    name="Lector Havoe",
    popularity=98,
)
artist.genres.set(genre_set)
artist.full_clean()
artist.save()
```
With this particular approach, we:
1. DB Cleaning
1. Create 7 Genre records one by one
1. Create 1 Artist record and attatch to it the associated genres

The SQL overview show us the following data `33.47 ms (62 queries including 28 similar)`

Altho `31.57 ms` seems pretty good, the amount of queries performed by the sql engine is alarming, we can see that with further details with tools like Django Debug Toolbar, but we can easily see the issue is in the `for loop` where we create or update our genres and we save them one by one.

Fortunately we have an alternative with the Django ORM for creating or updating un bulk:
```python
Genre.objects.all().delete()
Artist.objects.all().delete()

client_input_data = [
    "latin alternative", "latin pop",
    "latin rock", "mexican rock",
    "nu-cumbia", "rock en espanol", "rock urbano mexicano"
] # 7 total genres

current_genres = list(Genre.objects.filter(name__in=client_input_data)) # .filter returns a Queryset<Genre>
current_names = [g.name for g in current_genres]

new_genres = [
    Genre(name=genre) for genre in client_input_data
    if genre not in current_names
]

created_genres = Genre.objects.bulk_create(new_genres) # bulk_create returns a list[Genre]
artist_genres = created_genres + current_genres # We can sum lists to merge

# Artist creation remains the same
artist, created = Artist.objects.create(
    name="Lector Havoe",
    popularity=98,
)
artist.genres.set(artist_genres) # Passing the correct set
artist.full_clean()
artist.save()
```
Surprisingly, with this approach we reduced our SQL overview to: `12.18 ms (22 queries)`

Lets take a look at what changed:
1. DB Cleaning
1. Filter Genre DB records to retrieve the models that already exist.
    - At this point we convert the `Queryset<Genre>` into a `list[Genre]`, this is because we want to merge the existing genres with the genres we are going to create.
1. A list comprehension to generate the **list** of `new_genres` with the models that does not exist in our database currently.
1. Create 7 Genres records in bulk.
1. Merge into `artist_genres` both the `current_genres` and the `created_genres`
1. Create 1 Artist record and attatch to it the associated genres


Now the overviews without DB cleaning:
- Optimized: `default 10.91 ms (11 queries)`
- Non-optimized: `31.72 ms (38 queries including 28 similar)`
