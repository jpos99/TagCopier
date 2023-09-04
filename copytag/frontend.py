import datetime
import os
import PySimpleGUI as sg
import backend
import service


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

			if event == sg.WIN_CLOSED or event == 'Exit':
				break
			if event == 'Generate CSV':
				print('inicio', datetime.datetime.now())
				if not values['source'] or not os.path.exists(values['source']):
					sg.popup_error('Por favor, forneça um caminho de origem válido.')
					continue
				if not values['destination'] or not os.path.exists(values['destination']):
					sg.popup_error('Por favor, forneça um caminho de destino válido.')
					continue
				csv_file, source_destination_file_map = backend.csv_assembler(values['source'], values['destination'])
				if not csv_file or not os.path.exists(csv_file):
					sg.popup_error('Erro ao gerar o arquivo CSV.')
					continue
				table_data = service.read_csv(csv_file)
				if table_data:
					window['-TABLE-'].update(values=table_data)
					window['-TABLE-'].update(visible=True)
				else:
					sg.popup_error('Arquivo CSV vazio ou inválido.')
			elif event == 'Copy tags':
				if csv_file and os.path.exists(csv_file):
					updated_rows = backend.insert_tags_in_destinations(source_destination_file_map)
					for index in updated_rows:
						window['-TABLE-'].update(row_colors=[(index, 'green', 'black')])
				else:
					sg.popup_error('Por favor, gere o arquivo CSV primeiro.')
		except Exception as e:
			sg.popup_error(f"Ocorreu um erro: {e}")
	window.close()


if __name__ == '__main__':
	gui()
