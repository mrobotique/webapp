import copy

logFile = 'static/Log/log.csv'


def csv2list(file_name):
    """
    Abre un archivo CSV y lo pasa a una lista. Cada elemento de la lista es una lista que contiene cada
    uno de los campos del renglon csv
    :param file_name: nombre del archivo
    :type file_name: string
    :return: lista de listas con los campos de cada renglon del csv
    :rtype: lista de listas[str, str.., str]
    """
    entries_list = []
    with open(file_name) as f:
        lines = f.read().splitlines()
        for line in lines:
            entries_list.append(line.split(","))
    f.close()
    return entries_list


def genera_html(entries_list):

    # lee el header de la pagina
    with open('static/Log/aux/file_head.html') as f:
        head = f.read()
    f.close()

    # lee el final de la pagina
    with open('static/Log/aux/file_tail.html') as f:
        tail = f.read()
    f.close()

    dinamyc_page = head
    index = 1
    inverted_list = copy.deepcopy( entries_list[1:])
    inverted_list.reverse()
    for entry in inverted_list: #El primer renglon es el hedader del archivo con los nombres de las columnas
        try:
            [fecha, hora, expo, lugar] = entry
            dinamyc_page += '        <tr>'
            dinamyc_page += '<td colspan="4" style="text-align:center;">'
            dinamyc_page += fecha
            dinamyc_page += '</td>'
            dinamyc_page += '<td colspan="4" style="text-align:center;">'
            dinamyc_page += hora
            dinamyc_page += '</td>'
            dinamyc_page += '<td colspan="3" style="text-align:center;">'
            dinamyc_page += expo
            dinamyc_page += '</td>'
            dinamyc_page += '<td colspan="7" style="text-align:center;">'
            dinamyc_page += lugar
            dinamyc_page += '</td>'
            dinamyc_page += '<td colspan="3" style="text-align:center;"><input type="checkbox" id="check_'
            dinamyc_page += str(index)
            dinamyc_page += '"> </td>'
            dinamyc_page += "</tr>"
            index += 1
        except ValueError:
            pass
    dinamyc_page += tail
    return dinamyc_page


def list2str(list_name):
    result = ""
    for element in list_name:
        try:
            result += element
        except TypeError:
            result += str(element)
        result += ','
    result = result[:-1] #quita la ultima coma
    result += "\n"
    return result


def del_log():
    csv_file = csv2list(logFile)
    new_file = open(logFile, "w")
    new_file.write(list2str(csv_file[0]))
    new_file.close()


def add_new_entry(entry):
    # Open a file with access mode 'a'
    file_object = open(logFile, 'a')
    file_object.write(list2str(entry))
    file_object.close()


def del_rows(row_list):
    csv_file = csv2list(logFile)
    # Borra las entradas seleccionadas
    buffer = []
    buffer.append(csv_file.pop(0))
    for i in range(len(row_list)):
        if row_list[i] == 0:
            buffer.append(csv_file[i])
    # Guarda el nuevo archivo
    new_file = open(logFile, "w")
    for row in buffer:
        new_file.write(list2str(row))
    new_file.close()


def run_guts():
    csv_file = csv2list(logFile)

    return genera_html(csv_file)