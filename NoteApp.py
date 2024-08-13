from typing import List
from textual import on, events
from textual.app import App
from textual.widgets import Button, Input, Static, ListItem, ListView, Label
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import Reactive

class NoteApp(App):

    CSS = """
    
    Screen {
        align: center top;
        padding: 1;
    }
    
    Static{
    }
    
    #addNote {
        width: 3fr;
    }

    #addNoteInput {
        width: 97fr;
    }

    Horizontal {
        height: auto;
    }

    #noteList {
        margin: 1;
    }

    #edit_input {
        width: 100%;
        margin-bottom: 3;
    }

    #editDialog {
        width: 50%;
        height: auto;
        background: $background;
        border: solid $panel-darken-3;
        padding: 1;

        align: center middle;
    }

    #delete_button {
        color: red;
    }

    """

    notes: Reactive[List[Static]] = Reactive([])  # ノートのリストを保持

    def compose(self):

        self.notes_display = ListView(id="noteListView")
        self.input = Input(placeholder="新しいノートを入力...", id="addNoteInput")

        # コンテナにウィジェットを追加
        yield Vertical(
            Horizontal(
                self.input,
                Button("追加", id="addNote"),
                ),
            Vertical(
                Static("ノート\n", classes="notes"),
                self.notes_display,
                id="noteList"
                ),
            )

    @on(Button.Pressed, "#addNote")
    def add_note(self):
        # ノートを追加するメソッド
        note_text = self.input.value.strip()
        if note_text:
            self.notes_display.append(ListItem(Label(note_text)))  # ノートをリストに追加
            self.input.value = ""  # 入力フィールドをクリア

    @on(ListView.Selected, "#noteListView")
    async def on_list_view_selected(self, event: ListView.Selected):
        list_item = event.item
        if isinstance(list_item, ListItem):
            # 編集ダイアログを表示
            await self.show_edit_dialog(list_item)

    async def show_edit_dialog(self, list_item: ListItem) -> None:
        # Get the label widget from the ListItem
        label_widget = list_item.query_one(Label)
        current_text = str(label_widget.renderable) # テキストを取得する

        self.edit_input = Input(value=current_text, id="edit_input")

        # Create a dialog for editing
        self.dialog = Container(
            self.edit_input,
            Button("保存", id="save_button"),
            Button("キャンセル", id="cancel_button"),
            Button("削除", id="delete_button"),
            id="editDialog"
        )
        
        await self.mount(self.dialog)

        self.parentLabel = self.dialog.parent.query_one(Label)
    
    @on(Button.Pressed, "#save_button")
    async def save_changes(self) -> None:
        self.parentLabel.update(self.edit_input.value)  # Update the label's content
        await self.dialog.remove()

    @on(Button.Pressed, "#cancel_button")
    async def cancel_changes(self) -> None:
        await self.dialog.remove()

    @on(Button.Pressed, "#delete_button")
    async def delete_item(self) -> None:
        await self.notes_display.remove_items([self.notes_display.index])
        await self.dialog.remove()


if __name__ == "__main__":
    NoteApp().run()