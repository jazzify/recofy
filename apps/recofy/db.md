

# Django ORM Query Optimization Techniques

## Introduction to Database Query Optimization

Optimizing database queries is crucial for application performance. In this guide, we'll explore techniques to reduce query count and execution time in Django applications.

## Case Study: Artist and Genre Models

Let's examine a common scenario with related models:

```python
class Genre(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class Artist(BaseModel):
    name = models.CharField(max_length=255)
    popularity = models.PositiveSmallIntegerField()
    genres = models.ManyToManyField(Genre) # All artist genres
```

## Challenge: Adding Genres Dynamically

Our application needs to allow clients to dynamically add new genres when creating artists, while avoiding duplicate genres in the database.

### Approach 1: Individual Object Creation (Inefficient)

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
    # Each iteration creates a separate database query
    genre = Genre.objects.create(name=genre)
    # ... Some data processing
    genre.full_clean()
    genre.save()  # Another database hit
    genre_set.append(genre)

artist, created = Artist.objects.get_or_create(
    name="Lector Havoe",
    popularity=98,
)
artist.genres.set(genre_set)  # Multiple queries for M2M relationship
artist.full_clean()
artist.save()
```

**Performance Analysis:**
- Execution time: `33.47 ms`
- Query count: `62 queries (including 28 similar)`
- Problem: Each genre creation and save operation generates separate database queries

### Approach 2: Bulk Operations (Optimized)

```python
Genre.objects.all().delete()
Artist.objects.all().delete()

client_input_data = [
    "latin alternative", "latin pop",
    "latin rock", "mexican rock",
    "nu-cumbia", "rock en espanol", "rock urbano mexicano"
] # 7 total genres

# First, check which genres already exist (single query)
current_genres = list(Genre.objects.filter(name__in=client_input_data))
current_names = [g.name for g in current_genres]

# Prepare new genre objects without saving them individually
new_genres = [
    Genre(name=genre) for genre in client_input_data
    if genre not in current_names
]

# Create all new genres with a single query
created_genres = Genre.objects.bulk_create(new_genres)
artist_genres = created_genres + current_genres  # Combine existing and new genres

# Artist creation remains the same
artist, created = Artist.objects.get_or_create(
    name="Lector Havoe",
    popularity=98,
)
artist.genres.set(artist_genres)  # More efficient with fewer queries
artist.full_clean()
artist.save()
```

**Performance Analysis:**
- Execution time: `12.18 ms` (63% faster)
- Query count: `22 queries` (65% fewer queries)
- Without DB cleaning: `10.91 ms (11 queries)`

## Key Optimization Techniques

1. **Use `bulk_create` for multiple objects**
   - Reduces queries from N (one per object) to 1
   - Syntax: `Model.objects.bulk_create([Model(field=value), ...])`

2. **Filter existing records in a single query**
   - Use `filter(field__in=[values])` instead of multiple individual lookups

3. **Avoid unnecessary saves**
   - Only call `save()` when needed, not after every attribute change

4. **Leverage QuerySet evaluation control**
   - Convert QuerySets to lists only when needed
   - Use `values()` or `values_list()` when you only need specific fields

5. **Additional bulk operations**
   - `bulk_update()`: Update multiple objects with a single query
   - `in_bulk()`: Retrieve multiple objects by ID in one query

## Performance Comparison

| Approach | Execution Time | Query Count | Notes |
|----------|----------------|-------------|-------|
| Individual Creates | 33.47 ms | 62 queries | High overhead from multiple DB hits |
| Bulk Operations | 12.18 ms | 22 queries | 63% faster, 65% fewer queries |
| Bulk (no cleaning) | 10.91 ms | 11 queries | Best performance in production scenario |

## Conclusion

Using Django's bulk operations can dramatically reduce query count and execution time. Always consider using `bulk_create`, `bulk_update`, and efficient filtering when working with multiple objects.

For more advanced optimization, consider using Django Debug Toolbar to identify query bottlenecks and explore techniques like `select_related()` and `prefetch_related()` for related object queries.
