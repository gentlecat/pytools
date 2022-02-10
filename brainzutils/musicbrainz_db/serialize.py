from brainzutils.musicbrainz_db.models import ENTITY_MODELS
from mbdata.utils.models import get_link_target
from sqlalchemy_dst import row2dict


def serialize_areas(area, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': area.gid,
        'name': area.name,
    }

    if 'relationship_objs' in includes:
        serialize_relationships(data, area, includes['relationship_objs'])
    return data


def serialize_relationships(data, source_obj, relationship_objs):
    """Convert relationship objects to dictionaries.

    Args:
        data (dict): Dictionary containing info of source object.
        source_obj (mbdata.models): object of source entity.
        relationship_objs (dict): Dictionary containing list of objects of different relations.

    Returns:
        Dictionary containing lists of dictionaries of related entities.
    """

    for entity_type in ENTITY_MODELS:
        relation = '{0}-rels'.format(entity_type)
        if relation in relationship_objs:
            data[relation] = []
            for obj in relationship_objs[relation]:
                link_data = {
                    'type': obj.link.link_type.name,
                    'type-id': obj.link.link_type.gid,
                    'begin-year': obj.link.begin_date_year,
                    'end-year': obj.link.end_date_year,
                }
                link_data['direction'] = 'forward' if source_obj.id == obj.entity0_id else 'backward'
                if obj.link.ended:
                    link_data['ended'] = True
                link_data[entity_type] = SERIALIZE_ENTITIES[entity_type](get_link_target(obj, source_obj))
                data[relation].append(link_data)


def serialize_artist_credit(artist_credit):
    """Convert artist_credit object into a list of artist credits."""
    data = []
    for artist_credit_name in artist_credit.artists:
        artist_credit_data = {
            'mbid': artist_credit_name.artist.gid,
            'name': artist_credit_name.artist.name,
        }

        if artist_credit_name.name != artist_credit_name.artist.name:
            artist_credit_data['credited_name'] = artist_credit_name.name

        if artist_credit_name.join_phrase:
            artist_credit_data['join_phrase'] = artist_credit_name.join_phrase

        data.append(artist_credit_data)

    return data


def serialize_recording(recording, includes=None):
    """Convert recording objects into dictionary."""
    if includes is None:
        includes = {}
    data = {
        'mbid': recording.gid,
        'name': recording.name,
    }

    if recording.comment:
        data['comment'] = recording.comment

    if recording.length:
        # Divide recording length by 1000 to convert milliseconds into seconds
        data['length'] = recording.length / 1000.0

    if recording.video:
        data['video'] = True

    if 'rating' in includes and includes['rating']:
        data['rating'] = recording.rating

    if 'artist' in includes:
        data['artist'] = recording.artist_credit.name
    elif 'artists' in includes:
        data['artists'] = serialize_artist_credit(recording.artist_credit)
        data['artist-credit-phrase'] = includes['artist-credit-phrase']

    if 'isrc' in includes:
        data['isrcs'] = [isrc.isrc for isrc in recording.isrcs]

    return data


def serialize_places(place, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': place.gid,
        'name': place.name,
        'address': place.address,
    }

    if 'type' in includes and includes['type']:
        data['type'] = includes['type'].name

    if place.coordinates:
        data['coordinates'] = {
            'latitude': place.coordinates[0],
            'longitude': place.coordinates[1],
        }

    if 'area' in includes and includes['area']:
        data['area'] = serialize_areas(includes['area'])

    if 'relationship_objs' in includes:
        serialize_relationships(data, place, includes['relationship_objs'])
    return data


def serialize_labels(label, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': label.gid,
        'name': label.name,
    }

    if label.comment:
        data['comment'] = label.comment

    if 'type' in includes and includes['type']:
        data['type'] = includes['type'].name

    if 'area' in includes and includes['area']:
        data['area'] = includes['area'].name

    if 'rating' in includes and includes['rating']:
        data['rating'] = label.rating

    if 'relationship_objs' in includes:
        serialize_relationships(data, label, includes['relationship_objs'])

    return data


def serialize_artists(artist, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': artist.gid,
        'name': artist.name,
        'sort_name': artist.sort_name,
    }

    if 'comment' in includes:
        data['comment'] = artist.comment

    if 'type' in includes:
        data['type'] = artist.type.name

    if 'rating' in includes and includes['rating']:
        data['rating'] = artist.rating

    if 'relationship_objs' in includes:
        serialize_relationships(data, artist, includes['relationship_objs'])

    return data


def serialize_artist_credit_names(artist_credit_name):
    data = {
        'name': artist_credit_name.name,
        'artist': serialize_artists(artist_credit_name.artist),
    }
    if artist_credit_name.join_phrase:
        data['join_phrase'] = artist_credit_name.join_phrase
    return data


def serialize_release_groups(release_group, includes=None):
    if includes is None:
        includes = {}

    data = {
        'mbid': release_group.gid,
        'title': release_group.name,
    }

    if 'type' in includes and includes['type']:
        data['type'] = includes['type'].name

    if 'rating' in includes and includes['rating']:
        data['rating'] = release_group.rating

    if 'artist-credit-phrase' in includes:
        data['artist-credit-phrase'] = includes['artist-credit-phrase']

    if 'meta' in includes and includes['meta'] and includes['meta'].first_release_date_year:
        data['first-release-year'] = includes['meta'].first_release_date_year

    if 'artist-credit-names' in includes:
        data['artist-credit'] = [serialize_artist_credit_names(artist_credit_name)
                                 for artist_credit_name in includes['artist-credit-names']]

    if 'releases' in includes:
        data['release-list'] = [serialize_releases(release) for release in includes['releases']]

    if 'relationship_objs' in includes:
        serialize_relationships(data, release_group, includes['relationship_objs'])

    if 'tags' in includes:
        data['tag-list'] = includes['tags']
    return data


def serialize_medium(medium, includes=None):
    if includes is None:
        includes = {}
    data = {
        'name': medium.name,
        'track_count': medium.track_count,
        'position': medium.position,
    }
    if medium.format:
        data['format'] = medium.format.name

    if 'tracks' in includes and includes['tracks']:
        data['track-list'] = [serialize_track(track) for track in includes['tracks']]
    return data


def serialize_track(track):
    return {
        'mbid': track.gid,
        'name': track.name,
        'number': track.number,
        'position': track.position,
        'length': track.length,
        'recording_id': track.recording.gid,
        'recording_title': track.recording.name,
        'artist-credit': [serialize_artist_credit_names(artist_credit_name)
                          for artist_credit_name in track.recording.artist_credit.artists],
        'artist-credit-phrase': track.recording.artist_credit.name
    }


def serialize_releases(release, includes=None):
    if includes is None:
        includes = {}

    data = {
        'mbid': release.gid,
        'name': release.name,
    }

    if 'relationship_objs' in includes:
        serialize_relationships(data, release, includes['relationship_objs'])

    if 'release-groups' in includes:
        data['release-group'] = serialize_release_groups(includes['release-groups'])

    if 'artist-credit-phrase' in includes:
        data['artist-credit-phrase'] = includes['artist-credit-phrase']

    if 'artist-credit-names' in includes:
        data['artist-credit'] = [serialize_artist_credit_names(artist_credit_name)
                                 for artist_credit_name in includes['artist-credit-names']]

    if 'media' in includes:
        data['medium-list'] = [serialize_medium(medium, includes={'tracks': medium.tracks})
                               for medium in includes['media']]

    if 'comment' in includes:
        data['comment'] = release.comment

    return data


def serialize_events(event, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': event.gid,
        'name': event.name,
    }
    if 'type' in includes and includes['type']:
        data['type'] = includes['type'].name

    if 'rating' in includes and includes['rating']:
        data['rating'] = event.rating

    if 'relationship_objs' in includes:
        serialize_relationships(data, event, includes['relationship_objs'])
    return data


def serialize_url(url, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': url.gid,
        'url': url.url,
    }

    if 'relationship_objs' in includes:
        serialize_relationships(data, url, includes['relationship_objs'])
    return data


def serialize_works(work, includes=None):
    if includes is None:
        includes = {}
    data = {
        'mbid': work.gid,
        'name': work.name,
    }

    if 'type' in includes and includes['type']:
        data['type'] = includes['type'].name

    if 'rating' in includes and includes['rating']:
        data['rating'] = work.rating

    if 'relationship_objs' in includes:
        serialize_relationships(data, work, includes['relationship_objs'])

    return data


def serialize_editor(editor, includes=None):
    data = row2dict(editor, exclude_pk=True, exclude={'password', 'ha1'})

    # TODO: Add includes to data here (BU-18)

    return data


def serialize_series(series, includes=None):
    if includes is None:
        includes = []

    data = {
        'mbid': series.gid,
        'name': series.name,
    }

    if 'relationship_objs' in includes:
        serialize_relationships(data, series, includes['relationship_objs'])

    return data


SERIALIZE_ENTITIES = {
    'artist': serialize_artists,
    'release_group': serialize_release_groups,
    'release': serialize_releases,
    'medium': serialize_medium,
    'url': serialize_url,
    'editor': serialize_editor,
    'recording': serialize_recording,
    'place': serialize_places,
    'area': serialize_areas,
    'event': serialize_events,
    'series': serialize_series,
}
