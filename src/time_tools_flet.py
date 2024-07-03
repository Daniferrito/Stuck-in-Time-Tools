import flet as ft
import time_tools as tt
from pathlib import Path

def main(page: ft.Page):
    page.title = "Time Tools"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 500


    picker_save = ft.FilePicker()
    picker_json = ft.FilePicker()
    picker_csv  = ft.FilePicker()

    def decompress_click(_):
        def decompress_second(input: ft.FilePickerResultEvent):
            def decompress_third(output: ft.FilePickerResultEvent):
                tt.decompress(Path(input.files[0].path), Path(output.files[0].path))
            picker_json.on_result = decompress_third
            picker_json.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"])
        picker_save.on_result = decompress_second
        picker_save.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["save"])
    
    def compress_click(_):
        def compress_second(input: ft.FilePickerResultEvent):
            def compress_third(output: ft.FilePickerResultEvent):
                tt.compress(Path(input.files[0].path), Path(output.files[0].path))
            picker_save.on_result = compress_third
            picker_save.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["save"])
        picker_json.on_result = compress_second
        picker_json.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"])

    def insert_click(_):
        def insert_second(input: ft.FilePickerResultEvent):
            def insert_third(output: ft.FilePickerResultEvent):
                tt.insert(Path(input.files[0].path), Path(output.files[0].path))
            picker_save.on_result = insert_third
            picker_save.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["save"])
        picker_csv.on_result = insert_second
        picker_csv.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["csv", "tsv"])
    
    def extract_click(_):
        def extract_second(input: ft.FilePickerResultEvent):
            def extract_third(output: ft.FilePickerResultEvent):
                tt.extract(Path(input.files[0].path), Path(output.files[0].path))
            picker_csv.on_result = extract_third
            picker_csv.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["csv", "tsv"])
        picker_save.on_result = extract_second
        picker_save.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["save"])
    
    def map_click(_):
        def map_second(input: ft.FilePickerResultEvent):
            def map_third(output: ft.FilePickerResultEvent):
                tt.map(Path(input.files[0].path), Path(output.files[0].path))
            picker_csv.on_result = map_third
            picker_csv.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["csv", "tsv"])
        picker_json.on_result = map_second
        picker_json.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"])
    
    def type_click(_):
        def type_second(input: ft.FilePickerResultEvent):
            tt.type(Path(input.files[0].path))
        picker_csv.on_result = type_second
        picker_csv.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["csv", "tsv"])


    page.overlay.append(picker_save)
    page.overlay.append(picker_json)
    page.overlay.append(picker_csv)

    page.add(
        ft.Column(
            [
                ft.ElevatedButton("Decompress", on_click=decompress_click),
                ft.ElevatedButton("Compress", on_click=compress_click),
                ft.ElevatedButton("Insert", on_click=insert_click),
                ft.ElevatedButton("Extract", on_click=extract_click),
                ft.ElevatedButton("Map", on_click=map_click),
                ft.ElevatedButton("Type", on_click=type_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )

ft.app(target=main)