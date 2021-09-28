JSON Metadata Agent for Plex
============================

A metadata agent for Plex that reads from JSON files co-located with your media.


Why?
----

Not all metadata is easily accessed online via an HTML web page. There are some websites for which it is impossible to write a traditional Plex metadata agent — for example, those that:

* require username and password authentication, possibly even captcha
* hide information behind javascript
* detect the automated nature of the metadata agent, throttling or blocking scrapers
* perform poorly, crash and timeout
* frequently change their HTML structure

This agent doesn't collect any metadata itself — it simply loads metadata from JSON files found with your media into Plex.

It's designed to work alongside other tools and methods of collecting metadata, be it a custom scraper (it doesn't even have to be written in Python), browser plugin, command line tool or GUI. You could even edit the files by hand :)


Media Preperation
-----------------

At the time of writing, JSON metadata is supported *for audiobooks only*.

To define metadata for a movie, a JSON file named exactly `Info.json` must be present in the same directory as your movie file(s). For example:

```
Audiobooks
  |- Book
      |- Book.m4b
      |- Info.json
      |- Cover.jpg
```

This means you are limited to a single Book and `Info.json` file per directory.


Example JSON
------------

The structure of the `Info.json` file follows as closely as possible that of the `Music` model defined by Plex itself (although it's basically undocumented). It should look something like this:

```json
{
	"date": "Book Release Date",
	"title": "Boook Title",
	"authors": "Book Author",
	"series": "Book Series",
	"narrators": ["Narrator 1", "Narrator 2"],
	"studio": "Book Publisher",
	"rating": Rating out of 5,
	"genres": ["Genre 1", "Genre 2", "Genre 3", "Genre 4"],
	"description": "Book Description",
}
```
