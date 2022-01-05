from discord import Embed, Color

TOKEN_FILE = "./data/keys.json"

PLANNING_DOC_URL = "https://docs.google.com/spreadsheets/d/1g2Erqr_j_CYyxYOv6aNbcA-qwyYSVBcXsZ2CbyRYzNc/edit?usp=sharing"
PLANNING_DOC_ID = "1g2Erqr_j_CYyxYOv6aNbcA-qwyYSVBcXsZ2CbyRYzNc"
PLANNING_SHEET_NAME = 'DNK'
PLANNING_ROW_RANGE = (3, 9)     # included
PLANNING_START_COL = 'B'
PLANNING_TASKS_ORDER = ['traduction', 'clean', 'redraw', 'correction', 'edit', 'verification']

STAFF_ROLE = '923724925523603496'
FCRUI_ROLE = '923724998420623360'

PERMISSION_LEVELS = ['member', 'fcrui', 'staff']

unauthorized_embed = Embed(title="Erreur",
                        description="Vous n'êtes pas autorisé à utiliser cette commande, ou vous n'avez pas suivi son usage. Utilisez help.",
                        color=Color.red())

class ChapterState : pass
class Done(ChapterState) : 
    def __str__(self) -> str:
        return 'fait'

class InProgress(ChapterState) : 
    def __str__(self) -> str:
        return 'en cours'

class NotStarted(ChapterState) : 
    def __str__(self) -> str:
        return 'non commencé'