import datetime
import os
import PySimpleGUI as sg
import backend
import service
import logging

logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler("app.log"),
	]
)


def gui():
	sg.set_options(font="Any 16")
	layout = [
		[sg.Text('Select source directory:', size=(25, 1)), sg.InputText(key='source', size=(50, 1)), sg.FolderBrowse(size=(10, 1))],
		[sg.Text('Select destination directory:', size=(25, 1)), sg.InputText(key='destination', size=(50, 1)), sg.FolderBrowse(size=(10, 1))],
		[sg.Button('Generate CSV', size=(15, 1)), sg.Button('Exit', size=(15, 1)), sg.Button('Copy tags', size=(15, 1))],
		[sg.Table(
			values=[[''] * 3] * 10,
			headings=['Origem', 'Arquivo origem', 'Tag', 'Arquivo destino', 'Destino'],
			display_row_numbers=False,
			num_rows=500,
			key='-TABLE-',
			visible=False,
			font="Any 14",
			auto_size_columns=False,
			col_widths=[30, 30, 50],
			justification='left',
			alternating_row_color='lightblue',
			def_col_width=20,
			text_color='black'
		)]
	]

	window = sg.Window('Tag Copier', layout, resizable=True, size=(1000, 600))
	csv_file = None
	while True:
		try:
			event, values = window.read()
			logging.info(f"Event: {event}, Values: {values}")

			if event == sg.WIN_CLOSED or event == 'Exit':
				logging.info("Exiting the application")
				break
			if event == 'Generate CSV':
				logging.info("Starting CSV generation")
				print('inicio', datetime.datetime.now())
				if not values['source'] or not os.path.exists(values['source']):
					sg.popup_error('Por favor, forneça um caminho de origem válido.')
					logging.error("Invalid source path provided")
					continue
				if not values['destination'] or not os.path.exists(values['destination']):
					sg.popup_error('Por favor, forneça um caminho de destino válido.')
					logging.error("Invalid destination path provided")
					continue
				csv_file, source_destination_file_map = backend.csv_assembler(values['source'], values['destination'])
				if not csv_file or not os.path.exists(csv_file):
					sg.popup_error('Erro ao gerar o arquivo CSV.')
					logging.error("Failed to generate CSV file")
					continue
				table_data = service.read_csv(csv_file)
				if table_data:
					window['-TABLE-'].update(values=table_data)
					window['-TABLE-'].update(visible=True)
					logging.info("CSV file displayed in the table")
				else:
					sg.popup_error('Arquivo CSV vazio ou inválido.')
					logging.error("Empty or invalid CSV file")
			elif event == 'Copy tags':
				logging.info("Starting tag copying process")
				if csv_file and os.path.exists(csv_file):
					updated_rows = backend.insert_tags_in_destinations(source_destination_file_map)
					for index in updated_rows:
						window['-TABLE-'].update(row_colors=[(index, 'green', 'black')])
					logging.info(f"Tags copied to {len(updated_rows)} files")
				else:
					sg.popup_error('Por favor, gere o arquivo CSV primeiro.')
					logging.error("CSV file not generated before copying tags")
		except Exception as e:
			sg.popup_error(f"Ocorreu um erro: {e}")
			logging.exception("An error occurred")
	window.close()
	logging.info("Application window closed")


if __name__ == '__main__':
	gui()
