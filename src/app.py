from pathlib import Path

from patent_collections.modified_collections import Limited, WithExtendsColumn
from patent_collections.sources import PatentsFile, PatentsFromFile


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

    """

    def __init__(self):
        self.all_columns = [
            'id', 'title', 'assignee', 'inventor/author', 'priority date',
            'filing/creation date', 'publication date', 'grant date',
            'uri', 'representative figure link'
        ]
        self.columns = [
            'id', 'title', 'assignee', 'inventor/author', 'priority date',
            'filing/creation date', 'publication date', 'grant date', 'uri'
        ]
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.final_csv_path = self.data_dir / 'final.csv'
        self.test_csv_path = self.data_dir / 'test.csv'
        self.source_csv_path = self.data_dir / 'source.csv'
        self.raw_csv_path = self.data_dir / 'patents_raw.csv'
        self.max_patents = 5

    def run(self):
        patents = Limited(
            PatentsFromFile(str(self.source_csv_path), self.columns, 0), self.max_patents
        )

        file = PatentsFile(
            str(self.test_csv_path),
            WithExtendsColumn(patents),
            True
        )

        file.save()  # Сохранение файла


if __name__ == '__main__':
    app = App()
    app.run()
