from notification_services.src.broker.producer import RabbitMQ
from notification_services.src.core.sql import SQL_QUERIES
from notification_services.src.db.db_connection import open_postgres_connection


class NotifyBroker:

    def __init__(self):
        self.sql_queries = SQL_QUERIES
        self.notify_list = []

    def db_read(self):
        with open_postgres_connection() as pg_cursor:
            pg_cursor.execute(
                self.sql_queries.get("EVERY_X_DAYS")
            )
            self.notify_list = [notify for notify in pg_cursor.fetchall()]
            return True

    async def notify_broker(self):
        rabbit = RabbitMQ("amqp://guest:guest@localhost/")
        await rabbit.connect_broker()
        with open_postgres_connection() as pg_cursor:
            for note in self.notify_list:
                produce_access = await rabbit.produce({note[0]: note[1]})
                if produce_access:
                    pg_cursor.execute(
                        self.sql_queries.get("PROCESSED_ROWS"),
                        (note[0]),
                    )

    # def check_processed(self):
    #     with open_postgres_connection() as pg_cursor:
    #         pg_cursor.execute(
    #             self.sql_queries.get("SEND_BROKER")
    #         )
    #         # notify_list = pg_cursor.fetchall()
    #         self.notify_list = [notify for notify in pg_cursor.fetchall()]
    #         return True

# class ETL:
#     def __init__(self) -> None:
#         self.data_extractor_obj = self.Extractor()
#         self.data_transformer = self.Transformer()
#         self.data_loader = self.Loader()
#
#     def run(self) -> None:
#         raw_data = self.data_extractor_obj.collect_data()
#         es_data = self.data_transformer.transform_data(raw_data)
#         for index_name, data in es_data.items():
#             self.data_loader.load_to_es(index_name, data)
#
#     class Extractor:
#         def __init__(self) -> None:
#             self._person_ids: list[uuid.UUID] = []
#             self._movies_ids: list[uuid.UUID] = []
#             self._last_modified_person: datetime
#
#         def get_notify(self) -> None:
#             with open_postgres_connection() as pg_cursor:
#                 try:
#                     if state.get_state(STATE_JSON_KEY) is None:
#                         self._last_modified_person: datetime = (
#                             LAST_MODIFIED_DATA
#                         )
#                     else:
#                         self._last_modified_person: datetime = (
#                             datetime.fromisoformat(
#                                 state.get_state(STATE_JSON_KEY)
#                             )
#                         )
#
#                     pg_cursor.execute(
#                         sql_selects.get(SELECT_PERSONS).format(
#                             self._last_modified_person
#                         )
#                     )
#                     persons = pg_cursor.fetchall()
#                     if not persons:
#                         self._person_ids = []
#                         return
#                     self._person_ids = [person[0] for person in persons]
#
#                     state.state = (
#                         STATE_JSON_KEY,
#                         persons[len(persons) - 1][1].isoformat(),
#                     )
#
#                 except Exception as e:
#                     logger.error(f'Cannot get person ids {e}')
#
#     class Transformer:
#         def __init__(self) -> None:
#             self._how_many_movies_inserted: int = 0
#             self._how_many_persons_inserted: int = 0
#             self._how_many_genres_inserted: int = 0
#
#         def _process_movies(self, data: list) -> list:
#             if not data:
#                 return []
#
#             _aux_dict = defaultdict(
#                 lambda: {
#                     'imdb_rating': '',
#                     'genre': [],
#                     'title': '',
#                     'description': '',
#                     'actors_names': [],
#                     'actors': [],
#                     'writers_names': [],
#                     'writers': [],
#                     'directors': [],
#                     'director': '',
#                 }
#             )
#             for row in data:
#                 if _aux_dict.get(row['fw_id']) is None:
#                     _aux_dict[row['fw_id']]['imdb_rating'] = row['rating']
#                     _aux_dict[row['fw_id']]['title'] = row['title']
#                     _aux_dict[row['fw_id']]['description'] = row['description']
#
#                 if (
#                     row.get('name') is not None
#                     and {'name': row['name'], 'id': row['g_id']}
#                     not in _aux_dict[row['fw_id']]['genre']
#                 ):
#                     _aux_dict[row['fw_id']]['genre'].append(
#                         {'name': row['name'], 'id': row['g_id']}
#                     )
#
#                 if (
#                     row['role'] == 'actor'
#                     and row['full_name']
#                     not in _aux_dict[row['fw_id']]['actors_names']
#                 ):
#                     _aux_dict[row['fw_id']]['actors_names'].append(
#                         row['full_name']
#                     )
#                     _aux_dict[row['fw_id']]['actors'].append(
#                         {'id': row['p_id'], 'name': row['full_name']}
#                     )
#                 if (
#                     row['role'] == 'writer'
#                     and row['full_name']
#                     not in _aux_dict[row['fw_id']]['writers_names']
#                 ):
#                     _aux_dict[row['fw_id']]['writers_names'].append(
#                         row['full_name']
#                     )
#                     _aux_dict[row['fw_id']]['writers'].append(
#                         {'id': row['p_id'], 'name': row['full_name']}
#                     )
#                 if (
#                     row['role'] == 'director'
#                     and row['full_name'] != _aux_dict[row['fw_id']]['director']
#                 ):
#                     _aux_dict[row['fw_id']]['director'] = row['full_name']
#                     _aux_dict[row['fw_id']]['directors'].append(
#                         {'id': row['p_id'], 'name': row['full_name']}
#                     )
#
#             chunk = []
#             for k, v in _aux_dict.items():
#                 filmwork = {
#                     'id': k,
#                     'imdb_rating': v['imdb_rating'],
#                     'genre': v['genre'],
#                     'title': v['title'],
#                     'description': v['description'],
#                     'director': v['director'],
#                     'actors_names': v['actors_names'],
#                     'writers_names': v['writers_names'],
#                     'actors': v['actors'],
#                     'writers': v['writers'],
#                     'directors': v['directors'],
#                 }
#                 chunk.append(filmwork)
#
#             self._how_many_movies_inserted += len(chunk)
#             logger.info(f'Total processed: {self._how_many_movies_inserted}')
#             return chunk
#
#         def _process_genres(self, data: list) -> list:
#             if not data:
#                 return []
#
#             chunk = []
#             for row in data:
#                 chunk.append(
#                     {
#                         'id': row['uuid'],
#                         'name': row['name'],
#                     }
#                 )
#
#             self._how_many_genres_inserted += len(chunk)
#             logger.info(f'Total processed: {self._how_many_genres_inserted}')
#
#             return chunk
#
#         def _process_persons(self, data: list) -> list:
#             if not data:
#                 return []
#
#             _aux_dict = defaultdict(
#                 lambda: {
#                     'id': '',
#                     'name': '',
#                     'films': [{'id': '', 'roles': []}],
#                 }
#             )
#
#             chunk = []
#             for item in data:
#                 uuid, full_name, roles = item
#                 roles_by_film_id = defaultdict(list)
#                 aux = []
#                 for role in roles:
#                     roles_by_film_id[role['uuid']].append(role['roles'])
#
#                 for f_id, f_roles in roles_by_film_id.items():
#                     aux.append(
#                         {
#                             'id': f_id,
#                             'roles': list(set(f_roles)),
#                         }
#                     )
#                 chunk.append({'id': uuid, 'name': full_name, 'films': aux})
#
#             self._how_many_persons_inserted += len(chunk)
#             logger.info(f'Total processed: {self._how_many_persons_inserted}')
#             return chunk
#
#         def transform_data(
#             self, data: dict[str, list[tuple]]
#         ) -> dict[str, list[tuple]]:
#             return {
#                 'movies': self._process_movies(data['movies']),
#                 'genres': self._process_genres(data['genres']),
#                 'persons': self._process_persons(data['persons']),
#             }
#
#     class Loader:
#
#         def load_to_es(self, index: str, data: list) -> None:
#             if not data:
#                 return
#             actions = [
#                 {
#                     '_index': index,
#                     '_id': row['id'],
#                     '_source': row,
#                 }
#                 for row in data
#             ]
#             with open_elasticsearch_connection() as es:
#                 res = helpers.bulk(es, actions)
#                 logger.info(res)