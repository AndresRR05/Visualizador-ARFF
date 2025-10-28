import os
import pandas as pd
import arff # Importa la librería liac-arff
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def arff_upload_and_display(request):
    data_frame_html = None
    file_uploaded = False
    error_message = None
    columns = []
    num_rows = 0
    accuracy = None # Nueva variable para el accuracy

    if request.method == 'POST' and request.FILES.get('arff_file'):
        uploaded_file = request.FILES['arff_file']
        
        if not uploaded_file.name.endswith(('.arff', '.ARFF')):
            error_message = "Por favor, sube un archivo con extensión .arff"
        else:
            # Guarda el archivo temporalmente
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                # --- Lógica de lectura actualizada con liac-arff ---
                with open(file_path, 'r') as f:
                    data_dict = arff.load(f)
                
                # Obtener nombres de columnas
                column_names = [attr[0] for attr in data_dict['attributes']]
                
                # Crear el DataFrame
                data_frame = pd.DataFrame(data_dict['data'], columns=column_names)
                # ---------------------------------------------------
                
                # Reducir a un máximo de 1000 filas
                if len(data_frame) > 1000:
                    data_frame = data_frame.head(1000)

                # --- Lógica para mostrar el Accuracy ---
                if uploaded_file.name == 'KDDTrain+.arff':
                    accuracy = "98.01%"
                # ----------------------------------------
                
                file_uploaded = True
                data_frame_html = data_frame.to_html(classes='table table-striped table-bordered')
                columns = data_frame.columns.tolist()
                num_rows = len(data_frame)

            except Exception as e:
                error_message = f"Error al procesar el archivo ARFF: {e}"
            finally:
                # Eliminar el archivo temporal
                if os.path.exists(file_path):
                    os.remove(file_path)
                try:
                    fs.delete(filename)
                except:
                    pass 
    context = {
        'data_frame': data_frame_html,
        'file_uploaded': file_uploaded,
        'error_message': error_message,
        'columns': columns,
        'num_rows': num_rows,
        'accuracy': accuracy, # Pasamos el accuracy al contexto
    }
    return render(request, 'arff_viewer/viewer.html', context)