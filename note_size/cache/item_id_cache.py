import logging
from logging import Logger
from typing import Sequence, Any

from anki.cards import CardId, Card
from anki.notes import NoteId

from .cache import Cache
from ..common.collection_holder import CollectionHolder

log: Logger = logging.getLogger(__name__)


class ItemIdCache(Cache):

    def __init__(self, collection_holder: CollectionHolder) -> None:
        super().__init__()
        self.__collection_holder: CollectionHolder = collection_holder
        self.__id_cache: dict[CardId, NoteId] = {}
        self.invalidate_cache()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_cache(self) -> None:
        log.debug(f"Initializing ItemIdCache: size={len(self.__id_cache)}")
        with self._lock:
            for cid, nid in self.__collection_holder.col().db.execute("select id, nid from cards"):
                self.__id_cache[cid] = nid
        log.debug(f"Initialized ItemIdCache: size={len(self.__id_cache)}")

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        with self._lock:
            if card_id not in self.__id_cache:
                card: Card = self.__collection_holder.col().get_card(card_id)
                self.__id_cache[card_id] = card.nid
            return self.__id_cache[card_id]

    def get_note_ids_by_card_ids(self, card_ids: Sequence[CardId]) -> Sequence[NoteId]:
        with self._lock:
            return list({self.get_note_id_by_card_id(card_id) for card_id in card_ids})

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for cid, nid in list(self.__id_cache.items()):
                if nid == note_id and note_id in self.__id_cache:
                    del self.__id_cache[cid]

    def as_dict_list(self) -> list[dict[Any, Any]]:
        with self._lock:
            return [self.__id_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__id_cache = caches[0]
            log.info("Cache was read from dict list")

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__id_cache.clear()

    def get_cache_size(self) -> int:
        with self._lock:
            return len(self.__id_cache.keys())

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
