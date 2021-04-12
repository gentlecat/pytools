from collections import defaultdict
from unittest import TestCase
from unittest.mock import MagicMock
from mbdata import models
from brainzutils.musicbrainz_db.serialize import serialize_relationships
from brainzutils.musicbrainz_db.helpers import get_relationship_info
import brainzutils.musicbrainz_db as mb
from brainzutils.musicbrainz_db.helpers import get_tags
from brainzutils.musicbrainz_db.test_data import linkplaceurl_1, linkplaceurl_2, place_suisto


class HelpersTestCase(TestCase):

    def setUp(self):
        mb.mb_session = MagicMock()
        self.mock_db = mb.mb_session.return_value.__enter__.return_value
        self.tags_query = self.mock_db.query.return_value.join.return_value.\
            join.return_value.filter.return_value.group_by.return_value.all
        self.relationships_query = self.mock_db.query.return_value.options.return_value.\
            options.return_value.filter.return_value.options

    def test_get_tags(self):
        data = defaultdict(dict)
        self.tags_query.return_value = [(1820974, ['hip hop', 'hip-hop/rap'])]
        release_group_tags = get_tags(
            db=self.mock_db,
            entity_model=models.ReleaseGroup,
            tag_model=models.ReleaseGroupTag,
            foreign_tag_id=models.ReleaseGroupTag.release_group_id,
            entity_ids=['1820974'],
        )
        for release_group_id, tags in release_group_tags:
            data[release_group_id]['tags'] = tags
        expected_data = {
            1820974: {
                'tags': ['hip hop', 'hip-hop/rap']
            }
        }
        data = dict(data)
        self.assertDictEqual(data, expected_data)

    def test_get_relationship_info(self):
        data = {}
        self.relationships_query.return_value = [linkplaceurl_1, linkplaceurl_2]
        includes_data = defaultdict(dict)
        get_relationship_info(
            db=self.mock_db,
            target_type='url',
            source_type='place',
            source_entity_ids=['955'],
            includes_data=includes_data,
        )
        serialize_relationships(data, place_suisto, includes_data[place_suisto.id]['relationship_objs'])
        expected_data = {
            'url-rels': [
                {
                    'type': 'official homepage',
                    'type-id': '696b79da-7e45-40e6-a9d4-b31438eb7e5d',
                    'begin-year': None,
                    'end-year': None,
                    'direction': 'forward',
                    'url': {
                        'id': '7462ea62-7439-47f7-93bc-a425d1d989e8',
                        'url': 'http://www.suisto.fi/'
                    }
                },
                {
                    'type': 'social network',
                    'type-id': '040de4d5-ace5-4cfb-8a45-95c5c73bce01',
                    'begin-year': None,
                    'end-year': None,
                    'direction': 'forward',
                    'url': {
                        'id': '8de22e00-c8e8-475f-814e-160ef761da63',
                        'url': 'https://twitter.com/Suisto'
                    }
                }
            ]
        }
        self.assertDictEqual(data, expected_data)
