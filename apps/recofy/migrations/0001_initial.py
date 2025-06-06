# Generated by Django 5.0.6 on 2024-07-14 20:51

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("type", models.CharField(choices=[("album", "album")], max_length=5)),
                (
                    "album_type",
                    models.CharField(
                        choices=[
                            ("album", "album"),
                            ("single", "single"),
                            ("compilation", "compilation"),
                        ],
                        max_length=11,
                    ),
                ),
                ("href", models.URLField()),
                ("spotify_id", models.CharField(max_length=22, unique=True)),
                ("name", models.CharField(blank=True, max_length=255)),
                ("release_date", models.CharField(max_length=10)),
                (
                    "release_date_precision",
                    models.CharField(
                        choices=[("day", "day"), ("month", "month"), ("year", "year")],
                        max_length=5,
                    ),
                ),
                ("spotify_uri", models.CharField(max_length=37, unique=True)),
                ("external_urls", models.JSONField()),
                ("external_ids", models.JSONField()),
                ("total_tracks", models.PositiveSmallIntegerField()),
                (
                    "genres",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        default=list,
                        size=None,
                    ),
                ),
                ("label", models.CharField(max_length=255)),
                (
                    "available_markets",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=2), size=None
                    ),
                ),
                (
                    "copyrights",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.JSONField(), size=None
                    ),
                ),
                ("popularity", models.SmallIntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("external_urls", models.JSONField()),
                ("followers", models.JSONField()),
                ("href", models.URLField()),
                ("spotify_id", models.CharField(max_length=22, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("popularity", models.PositiveSmallIntegerField()),
                (
                    "type",
                    models.CharField(choices=[("artist", "artist")], max_length=6),
                ),
                ("spotify_uri", models.CharField(max_length=37, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("preview_url", models.URLField(null=True)),
                ("is_playable", models.BooleanField()),
                ("explicit", models.BooleanField()),
                ("type", models.CharField(choices=[("track", "track")], max_length=5)),
                ("spotify_id", models.CharField(max_length=22, unique=True)),
                ("href", models.URLField()),
                ("disc_number", models.PositiveSmallIntegerField()),
                ("track_number", models.PositiveSmallIntegerField()),
                ("duration_ms", models.PositiveIntegerField()),
                ("external_ids", models.JSONField()),
                ("external_urls", models.JSONField()),
                ("name", models.CharField(max_length=255)),
                ("popularity", models.PositiveSmallIntegerField()),
                ("spotify_uri", models.CharField(max_length=37, unique=True)),
                ("is_local", models.BooleanField()),
                (
                    "available_markets",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=2), size=None
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AlbumImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("height_px", models.PositiveSmallIntegerField()),
                ("width_px", models.PositiveSmallIntegerField()),
                ("url", models.URLField(unique=True)),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recofy.album"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AlbumsArtists",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recofy.album",
                        to_field="spotify_id",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recofy.artist",
                        to_field="spotify_id",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="album",
            name="artists",
            field=models.ManyToManyField(
                through="recofy.AlbumsArtists", to="recofy.artist"
            ),
        ),
        migrations.CreateModel(
            name="ArtistImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("height_px", models.PositiveSmallIntegerField()),
                ("width_px", models.PositiveSmallIntegerField()),
                ("url", models.URLField(unique=True)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recofy.artist"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="artist",
            name="genres",
            field=models.ManyToManyField(to="recofy.genre"),
        ),
        migrations.CreateModel(
            name="AlbumsTracks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recofy.album",
                        to_field="spotify_id",
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recofy.track",
                        to_field="spotify_id",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="album",
            name="tracks",
            field=models.ManyToManyField(
                through="recofy.AlbumsTracks", to="recofy.track"
            ),
        ),
        migrations.CreateModel(
            name="TracksArtists",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recofy.artist",
                        to_field="spotify_id",
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recofy.track",
                        to_field="spotify_id",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="track",
            name="artists",
            field=models.ManyToManyField(
                through="recofy.TracksArtists", to="recofy.artist"
            ),
        ),
    ]
