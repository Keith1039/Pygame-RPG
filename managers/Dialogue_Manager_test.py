from managers.Dialogue_Manager import DialogueManager
from managers.Screen_Manager import Event

dialogueManager = DialogueManager()
mockDialogEvent = Event(None, "Dialogue","event_text/Test_dialogue.txt")

def mock_draw_dialogue(dialogueTimer):
    # Version of draw_dialogue that doesn't do any of the drawing.
    text = dialogueManager.prevText
    if dialogueTimer % 180 == 0:
        text = dialogueManager.get_text()
    # There is an easier way to do this but it makes my eyes bleed so no :)
    return text != ""
def test_load_file():
    # Load file just uses open() to get a file object. Loading a valid file should 
    # actually load the file thus making file not None
    dialogueManager.load_file(mockDialogEvent)
    assert dialogueManager.file is not None

def test_clear_file():
    # Checks if the file value in the manager is None and the file is cleared properly
    # Also checks if the events activated value has been changed. This logic is going to cause problems in the future
    # But that is future Keith's problem.
    dialogueManager.load_file(mockDialogEvent)
    dialogueTimer = 180
    flag = True
    file = dialogueManager.file
    while flag:
        flag = mock_draw_dialogue(dialogueTimer)
        dialogueTimer += 1
    # Might make dialogueManager keep the file even after it has been closed.
    assert file.closed and dialogueManager.file is None and mockDialogEvent.activated
