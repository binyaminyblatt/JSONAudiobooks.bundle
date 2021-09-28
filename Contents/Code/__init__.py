import os, json, urllib, re

class JSONAgent(Agent.Artist):
    name = 'JSON Metadata'
    languages = [Locale.Language.English]
    primary_provider = True
    persist_stored_files = False
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        return
        
    def update(self, metadata, media, lang):
        return

class JSONAgent(Agent.Album):
    name = 'JSON Metadata'
    languages = [Locale.Language.English]
    primary_provider = True
    persist_stored_files = False
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        path = os.path.join(os.path.dirname(urllib.unquote_plus(media.filename)), 'Info.json')

        if os.path.exists(path):
            results.Append(MetadataSearchResult(id = path, name=media.album, score = 100, lang=lang))

    def update(self, metadata, media, lang):
        path = metadata.id
        
        info = JSON.ObjectFromString(Core.storage.load(path))

        try: metadata.originally_available_at = Datetime.ParseDate(info['date'])
        except:
            pass

        try: metadata.title = info['title']
        except:
            pass

        try: media.artist = info['authors']
        except:
            pass

        metadata.moods.clear()
        try: metadata.moods.add(info['series'])
        except:
            pass
        
        metadata.genres.clear()
        try:
            for g in info['narrators']:
                metadata.styles.add(g)
        except:
            pass
            
        try: metadata.studio = info['studio']
        except:
            pass

        try: metadata.rating = float(info['rating']) * 2
        except:
            pass
        
        metadata.genres.clear()
        try:
            for g in info['genres']:
                metadata.genres.add(g)
        except:
            pass
            
        try: metadata.summary = info['description']
        except:
            pass
