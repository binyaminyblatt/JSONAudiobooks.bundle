try:
    import plexhints  # noqa: F401
except ImportError:
    pass
else:  # the code is running outside of Plex
    from plexhints import plexhints_setup, update_sys_path
    plexhints_setup()  # reads the plugin plist file and determine if plexhints should use elevated policy or not
    update_sys_path()  # when running outside plex, append the path
    from plexhints.agent_kit import Agent  # agent kit
    from plexhints.core_kit import Core  # core kit
    from plexhints.locale_kit import Locale  # locale kit
    from plexhints.object_kit import MetadataSearchResult  # object kit
    from plexhints.parse_kit import JSON  # parse kit
    from plexhints.template_kit import _DatetimeTemplate as Datetime # utils kit
    from plexhints.proxy_kit import Proxy  # worker manager runner kit
    from plexhints.network_kit import HTTP  # worker kit
    from plexhints.constant_kit import CACHE_1WEEK  # worker manager kit
    from plexhints.log_kit import Log
    from plexhints.prefs_kit import Prefs  # prefs kit
import os
import re
import urllib

# Define plugin version
VERSION_NO = '0.0.1' # version

def move_articles_to_end(title):
    # Define articles to move
    articles = ["The", "A", "An"]
    words = title.split()

    # Check if the title starts with an article
    if words[0] in articles:
        # Move the article to the end, with a comma
        return " ".join(words[1:]) + ", " + words[0]
    return title

def simplify_title(self):
    """
        Remove extra description text from the title
    """
    # If the title ends with a series part, remove it
    # works for "Book 1" and "Book One"
    album_title = re.sub(r", book [\w\s-]+\s*$", "", self.title, flags=re.IGNORECASE)
    # If the title ends with "unabridged"/"abridged", with or without parenthesis
    # remove them; case insensitive
    album_title = re.sub(r" *\(?(un)?abridged\)?$", "", album_title, flags=re.IGNORECASE)
    # Trim any leading/trailing spaces just in case
    album_title = album_title.strip()

    return album_title

def Start():
    HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['User-agent'] = (
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0;'
        'SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729;'
        'Media Center PC 6.0'
    )
    HTTP.Headers['Accept-Encoding'] = 'gzip'

class JSONAudiobooksAgent(Agent.Artist):
    name = 'JSON Audiobooks Metadata'
    languages = [Locale.Language.English]
    primary_provider = True
    persist_stored_files = False
    accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.audnexus', 'com.plexapp.agents.audiobooks']
    contributes_to = ['com.plexapp.agents.audnexus', 'com.plexapp.agents.audiobooks']
    def search(self, results, media, lang):
        return
        
    def update(self, metadata, media, lang):
        return

class JSONAudiobooksAgent(Agent.Album):
    name = 'JSON Audiobooks Metadata'
    languages = [Locale.Language.English]
    primary_provider = True
    persist_stored_files = False
    accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.audnexus', 'com.plexapp.agents.audiobooks']
    contributes_to = ['com.plexapp.agents.audnexus', 'com.plexapp.agents.audiobooks']

    def search(self, results, media, lang):
        json_files = [
            'audiobook.json', 'Audiobook.json', 'audiobook_data.json', 'audiobookdata.json',
            'info.json', 'Info.json', 'data.json', 'Data.json'
        ]
        for filename in json_files:
            path = os.path.join(os.path.dirname(urllib.unquote_plus(media.filename)), filename)
            if os.path.exists(path):
                Log.Info('Found file ' + path)
                info = JSON.ObjectFromString(Core.storage.load(path))
                results.Append(MetadataSearchResult(id=path, name=info.get('title', media.album), score=100, lang=info.get('language', lang)))
                return

    def update(self, metadata, media, lang):
        path = metadata.id
        
        info = JSON.ObjectFromString(Core.storage.load(path))

        try: 
            metadata.originally_available_at = Datetime.ParseDate(info['date'])
            Log.Info('Updating metadata Dates')
        except:
            Log.Debug('Couldnt add date to album.')
        
        try: 
            metadata.title = info['title']
            Log.Info('Updating metadata Title')
        except:
            Log.Debug('Couldnt add title to album.')
            
        try: 
            metadata.artist = info['authors']
            authors = info['authors']
            if isinstance(authors, list):
                metadata.artist = authors[0]
            else:
                metadata.artist = authors            
            Log.Info('Updating metadata Authors')
        except:
            Log.Debug('Couldnt add authors to album.')
            
        try: 
            metadata.moods.clear()
            series = info['series']
            if isinstance(series, list):
                for s in series:
                    metadata.moods.add("Series: " + s)
            else:
                metadata.moods.add("Series: " + series)
            Log.Info('Updating metadata Series')
        except:
            Log.Debug('Couldnt add series to album.')

        try: 
            metadata.tags.clear()
            tags = info['tags']
            if isinstance(tags, list):
                for s in tags:
                    metadata.tags.add(s)
            else:
                metadata.tags.add(tags)
            Log.Info('Updating metadata Tags')
        except:
            Log.Debug('Couldnt add tags to album.')
        
        # add author to moods list
        contributor_regex = '.+?(?= -)'
        if not metadata.moods:
            # Loop through authors to check if it has contributor wording
            if isinstance(authors, list):
                for author in authors:
                    if not re.match(contributor_regex, author['name']):
                        metadata.moods.add(author['name'].strip())
            else:
                metadata.moods.add(authors['name'].strip())

        try:
            metadata.styles.clear()
            for g in info['narrators']:
                metadata.styles.add(g)
            Log.Info('Updating metadata Narrators')
        except:
            Log.Debug('Couldnt add narrators to album.')
        
        
        try:
            metadata.collections.clear()
            for g in info['collections']:
                metadata.collections.add(g)
            Log.Info('Updating metadata collections')
        except:
            Log.Debug('Couldnt add collections to album.')
            
        try: 
            metadata.studio = info['studio']
            Log.Info('Updating metadata Studio')
        except:
            Log.Debug('Couldnt add studio to album.')
            

        try: 
            metadata.rating = float(info['rating'])
            Log.Info('Updating metadata Rating')
        except:
            Log.Debug('Couldnt add rating to album.')
            
        try:
            metadata.genres.clear()
            for g in info['genres']:
                metadata.genres.add(g)
            Log.Info('Updating metadata Genres')
        except:
            Log.Debug('Couldnt add genres to album.')

        try:
            metadata.similar.clear()
            for i in info['similar']:
                metadata.similar.add(i)
            Log.Info('Updating metadata similar')
        except:
            Log.Debug('Couldnt add similar albums to album.')

        try:
            for full_poster_url in info['posters']:
                Log.Debug('Adding poster ' + full_poster_url)
                metadata.posters[full_poster_url]        = Proxy.Media(HTTP.Request(full_poster_url, immediate=True).content)
            Log.Info('Updating metadata Artwork')
        except:
            Log.Debug('Couldnt add artwork to album.')

        try:
            for full_art_url in info['art']:
                Log.Debug('Adding poster ' + full_art_url)
                metadata.posters[full_art_url]        = Proxy.Media(HTTP.Request(full_art_url, immediate=True).content)
            Log.Info('Updating metadata Background Image')
        except:
            Log.Debug('Couldnt add Background Image to album.')
        
        try: 
            metadata.summary = info['description']
            Log.Info('Updating metadata Description')
        except:
            Log.Debug('Couldnt add description to album.')
        
        
        
        try:
            series = info['series']
        except:
            series = None

        try:
            title = info['title']
        except:
            title = ''

        # Apply article-movement to the title
        formatted_title = move_articles_to_end(simplify_title(title))
        
        if series:
            # If series is present, apply book-number to the title
            try:
                book_number = info['book_number']
            except:
                book_number = None

            if isinstance(book_number, list):
                book_number = book_number[0]
            book_number = str(book_number)

            if isinstance(series, list):
                if book_number:
                    # If both series and book_number are present
                    metadata.title_sort = series[0] + ", Book " + book_number +" - " + formatted_title
                else:
                    # If only series is present, but no book_number
                    metadata.title_sort = series[0] + " - " + formatted_title
            else:
                if book_number:
                    # If both series and book_number are present
                    metadata.title_sort = series + ", Book " + book_number + " - " + formatted_title
                else:
                    # If only series is present, but no book_number
                    metadata.title_sort = series + " - " + formatted_title
        else:
            # If no series, fallback to just the title
            metadata.title_sort = formatted_title
