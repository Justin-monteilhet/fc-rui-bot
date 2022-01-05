from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from json import dumps
from typing import Tuple, List
from pprint import pprint

from utils import char_to_alphabet_pos, int_to_sheet_row, rgb_to_chap_state
from constants import PLANNING_DOC_URL, PLANNING_SHEET_NAME, PLANNING_ROW_RANGE, PLANNING_START_COL, PLANNING_TASKS_ORDER, ChapterState

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("./data/credentials.json", scope)
service = discovery.build('sheets', 'v4', credentials=creds)
sheets = service.spreadsheets()


class SheetData:
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} value={self.value} bgColor={self.bgColor}>"
    
    def __repr__(self) -> str:
        return self.__str__()

    def __init__(self, row_values):
        self.row_values = row_values
        self.cells = []
        for x, row in enumerate(self.row_values):
            self.cells.append([])
            for y, cell in enumerate(row['values']):
                self.cells[-1].append(SheetCell.from_dict(cell))
        
        self.size = len(self.cells), len(self.cells[0])

    @classmethod
    def from_dict(cls, d:dict):
        values = d['sheets'][0]['data'][0]['rowData']
        return cls(values)

    @classmethod
    def from_id(cls, sheetId:str, ranges="FULL"):
        if ranges == "FULL" :
            dim_rq = sheets.get(spreadsheetId=sheetId).execute()
            planning_sheet = None
            for sheet in dim_rq['sheets']:
                if sheet['properties']['title'] == PLANNING_SHEET_NAME:
                    planning_sheet = sheet
                    break

            grid_properties = sheet["properties"]["gridProperties"]
            cols = grid_properties["columnCount"] - char_to_alphabet_pos(PLANNING_START_COL)

            first_coo = f"{PLANNING_START_COL}{PLANNING_ROW_RANGE[0]}"
            last_coo = f"{int_to_sheet_row(cols)}{PLANNING_ROW_RANGE[1]}"
            ranges = f"{PLANNING_SHEET_NAME}!{first_coo}:{last_coo}"

        rq = sheets.get(spreadsheetId=sheetId, ranges=ranges, includeGridData=True)
        data = rq.execute()
        return cls.from_dict(data)

    def get_chapter_column(self, num:int):
        col_index = None
        for i, chap_num_cell in enumerate(self.cells[0]):
            if chap_num_cell.value == str(num):
                col_index = i
                break
        if col_index is not None:
            return [row[col_index] for row in self.cells[1:]]

    def get_chapter_data(self, num:int):
        column = self.get_chapter_column(num)
        if column:
            return ChapterData(num, column)

class SheetCell:
    def __init__(self, value:str, bgColor:Tuple[float, float, float]) -> None:
        self.value = value
        self.bgColor = Color.from_rgb_dict(bgColor)
    
    @classmethod
    def from_dict(cls, d:dict):
        value = d.get('formattedValue', None)
        try : col = d['effectiveFormat']['backgroundColor']
        except : col = None
        return cls(value, col)

class ChapterData:
    def __init__(self, chap_num:int, cells:List[SheetCell]) -> None:
        self.tasks:List[Task] = []
        for task_name, cell in zip(PLANNING_TASKS_ORDER, cells):
            tsk = Task(chap_num, worker=cell.value, type_=task_name, state=rgb_to_chap_state(cell.bgColor))
            self.tasks.append(tsk)

class Task:
    def __init__(self, chapter:int, worker:str, type_:str, state:ChapterState) -> None:
        self.chapter = chapter
        self.worker = worker
        self.type = type_
        self.state = state

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"<Chapter {self.chapter} {self.type} from {self.worker} : {self.state}"

class Color:
    def __init__(self, col:Tuple[float, float, float]) -> None:
        self.red, self.green, self.blue = self.rgb = tuple(map(float, col))

    @classmethod
    def from_rgb_dict(cls, d:dict):
        color = []
        for col in ['red', 'green', 'blue']:
            if col in d:
                color.append(d[col])
                continue
            color.append(0.)

        return cls(tuple(color))
    
    def __str__(self) -> str:
        return self.rgb.__str__()
