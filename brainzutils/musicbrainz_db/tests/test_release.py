import pytest

from brainzutils.musicbrainz_db import release as mb_release
from brainzutils.musicbrainz_db.unknown_entities import unknown_release


@pytest.mark.database
class TestRelease:

    def test_get_by_id(self, engine):
        release = mb_release.get_release_by_id(
            'fed37cfc-2a6d-4569-9ac0-501a7c7598eb',
            includes=['media', 'release-groups'],
        )
        assert release["name"] == "Master of Puppets"
        assert len(release["medium-list"][0]["track-list"]) == 8

        assert release["medium-list"][0]["track-list"] == [
            {
               "id":"58c97804-bd98-3bc6-b8c7-5234db05bc2e",
               "name":"Battery",
               "number":"1",
               "position":1,
               "length":312373,
               "recording_id":"3bfda26a-49fa-4bc4-a4d6-8bbfa0767ab7",
               "recording_title":"Battery"
            },
            {
               "id":"51b179fa-8e72-383b-9549-0ae9a6dd9cfb",
               "name":"Master of Puppets",
               "number":"2",
               "position":2,
               "length":515226,
               "recording_id":"0151d8a4-50c8-4036-b824-4a4f4b140e8e",
               "recording_title":"Master of Puppets"
            },
            {
               "id":"052e25d8-373e-3a5a-bced-bd47eb209dc5",
               "name":"The Thing That Should Not Be",
               "number":"3",
               "position":3,
               "length":396200,
               "recording_id":"f5267fe1-5cb6-47f7-8df2-e6e8f09fa7ad",
               "recording_title":"The Thing That Should Not Be"
            },
            {
               "id":"00367246-d956-3a44-af4b-bc3cfd34ec49",
               "name":"Welcome Home (Sanitarium)",
               "number":"4",
               "position":4,
               "length":386866,
               "recording_id":"a20860e9-7636-422b-a9cd-2da671b242a8",
               "recording_title":"Welcome Home (Sanitarium)"
            },
            {
               "id":"77fac948-8223-3077-a25e-50d9512142f0",
               "name":"Disposable Heroes",
               "number":"5",
               "position":5,
               "length":496640,
               "recording_id":"93ae3251-d9b5-46ee-9849-7b16d5e57d8b",
               "recording_title":"Disposable Heroes"
            },
            {
               "id":"7f97a9e0-89ec-37ed-a3d7-5a7390ffa43b",
               "name":"Leper Messiah",
               "number":"6",
               "position":6,
               "length":339866,
               "recording_id":"2d9a5b40-f5e6-4499-ab7a-567fe3b42ab9",
               "recording_title":"Leper Messiah"
            },
            {
               "id":"b7e772d3-3a9b-32ad-8e5c-e8c079d5e4f4",
               "name":"Orion",
               "number":"7",
               "position":7,
               "length":507426,
               "recording_id":"b6cbe414-8b21-4600-8588-f6a80fd7043a",
               "recording_title":"Orion"
            },
            {
               "id":"0949ef68-edef-39a1-a3a0-dc666920f629",
               "name":"Damage, Inc.",
               "number":"8",
               "position":8,
               "length":330933,
               "recording_id":"01ea1189-e0d2-48a0-9dc2-c615785a5ae0",
               "recording_title":"Damage, Inc."
            }
        ]

    def test_fetch_multiple_releases(self, engine):
        releases = mb_release.fetch_multiple_releases(
            mbids=['e327da6d-717b-4eb3-b396-bbce6b9466bc', 'b1bb026c-e813-407f-ba7b-db7466cdc56c'],
        )
        assert len(releases) == 2
        assert releases['e327da6d-717b-4eb3-b396-bbce6b9466bc']['name'] == 'Without a Sound'
        assert releases['b1bb026c-e813-407f-ba7b-db7466cdc56c']['name'] == 'War All the Time'

    def test_fetch_multiple_releases_empty(self, engine):
        releases = mb_release.fetch_multiple_releases(
            mbids=['f51598f5-4ef9-4b8a-865d-06a077bf78cf', 'a64a0467-9d7a-4ffa-90b8-d87d9b41e311'],
            includes=['media', 'release-groups', 'url-rels'],
            unknown_entities_for_missing=True
        )
        assert releases['a64a0467-9d7a-4ffa-90b8-d87d9b41e311']['name'] == unknown_release.name
        assert releases['f51598f5-4ef9-4b8a-865d-06a077bf78cf']['name'] == unknown_release.name

    def test_get_releases_using_recording_mbid(self, engine):
        """Tests if releases are fetched correctly for a given recording MBID"""
        releases = mb_release.get_releases_using_recording_mbid('5465ca86-3881-4349-81b2-6efbd3a59451')
        assert releases == [
            {'id': '89f64145-2f75-41d1-831a-517b785ed75a', 'name': "The Blueprint Collector's Edition"},
            {'id': 'f1183a86-36d2-4f1f-ab8f-6f965dc0b033', 'name': 'The Hits Collection Volume One'},
            {'id': '77a74b85-0ae0-338f-aaca-4f36cd394f88', 'name': 'Blueprint 2.1'},
            {'id': '7111c8bc-8549-4abc-8ab9-db13f65b4a55', 'name': 'Blueprint 2.1'},
            {'id': '2c5e4198-24cf-3c95-a16e-83be8e877dfa', 'name': 'The Blueprint²: The Gift & The Curse'},
            {'id': '3c535d03-2fcc-467a-8d47-34b3250b8211', 'name': 'The Hits Collection Volume One'},
            {'id': 'c84d8fa8-6f8d-42c9-87cc-b726e859b41d', 'name': 'The Hits Collection Volume One'},
            {'id': '4f41108c-db36-4616-8614-f504fdef287a', 'name': 'Blueprint 2.1'},
            {'id': 'b0075ce9-58c8-47e2-8a72-5f783314a97e', 'name': 'The Hits Collection Volume One'},
            {'id': 'd75e103c-5ef4-4146-ae81-e27d19dc7fc4', 'name': "The Blueprint Collector's Edition"},
            {'id': '4a441628-2e4d-4032-825f-6bdf4aee382e', 'name': 'The Hits Collection, Volume 1'},
            {'id': '5e782ae3-602b-48b7-99be-de6bcffa4aba', 'name': 'The Hits Collection, Volume 1'},
            {'id': '7ebaaa95-e316-3b20-8819-7e4ca648c135', 'name': 'The Hits Collection, Volume 1'},
            {'id': '0ff452e3-c306-4082-b0dc-223725f4fbbf', 'name': 'The Blueprint²: The Gift & The Curse'},
            {'id': '801678aa-5d30-4342-8227-e9618f164cca', 'name': 'The Blueprint²: The Gift & The Curse'}
        ]
