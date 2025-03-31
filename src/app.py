from .config import Environment, KeyListPairsEnvironment
from patent_collections.modified_collections import Limited, WithExtendsColumn
from patent_collections.sources import PatentsInFile
from patent_collections.destinations import PatentsToFile


class App:
    """

    patents = CleanedPatents(
        Limited(
            OnlyWith(
                WithRenamedColumn(
                    PatentsFromFile(
                        str(data_dir / 'patents_raw.csv'),
                        columns=all_columns,
                        skip_rows=1
                    ),
                    'result link',
                    'uri'
                ),
                'uri'
            ),
            10
        ),
        columns
    )

    self._all_columns = [
            'id', 'title', 'assignee', 'inventor/author', 'priority date',
            'filing/creation date', 'publication date', 'grant date',
            'uri', 'representative figure link'
        ]

    """

    def __init__(self):
        self._environment = Environment(True)
        self._key_list_pairs_environment = KeyListPairsEnvironment('::', True)

    def run(self):
        # Processed patent collection
        patents = WithExtendsColumn(
            Limited(
                PatentsInFile(
                    self._environment.field('SOURCE_CSV_PATH'),
                    self._key_list_pairs_environment.field('COLUMNS'),
                ),
                int(self._environment.field('MAX_PATENTS')),
            )
        )

        # Patent Destination
        file = PatentsToFile(
            self._environment.field('FINAL_CSV_PATH'),
            patents,
            True
        )

        # Save patents
        file.save()
