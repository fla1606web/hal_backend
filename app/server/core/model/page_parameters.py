from typing import List

import pymongo

from app.server.models.entity_field import EntityField
from app.server.core.model.filter import Filter

class PageParameters():
    filters: List[Filter]
    parentFilter: Filter
    page: int
    pageSize: int
    entitySort: str
    entitySortType: str
    fields: List[str] 

    def __init__(self, filters, parentFilter, page, pageSize, entitySort, entitySortType, fields):
        self.filters = filters
        self.parentFilter = parentFilter
        self.page = page
        self.pageSize = pageSize
        self.entitySort = entitySort
        if entitySortType == "asc":
            self.entitySortType = pymongo.ASCENDING
        else:
            self.entitySortType = pymongo.DESCENDING
        self.fields = fields