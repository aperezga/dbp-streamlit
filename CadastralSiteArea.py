import tkinter as tk
from tkinter import simpledialog, ttk
import requests
import tempfile
from zipfile import ZipFile
import geopandas as gpd
import io

class GMLData:
    def __init__(self, url):
        self.url = url

    def process_gml(self):
        """Downloads, extracts, and loads the GML file without leaving residual files on the system."""
        response = requests.get(self.url, stream=True)
        if response.status_code != 200:
            print("Error downloading the file.")
            return None

        with tempfile.TemporaryDirectory() as temp_dir:  # Temporary folder automatically deleted
            with ZipFile(io.BytesIO(response.content), "r") as zipObj:
                # Find the first file with a .gml extension inside the ZIP
                gml_filename = next((f for f in zipObj.namelist() if f.endswith(".gml")), None)

                if not gml_filename:
                    print("No GML file found in the ZIP.")
                    return None

                zipObj.extract(gml_filename, temp_dir)  # Extract the GML file into the temporary folder
                gml_path = f"{temp_dir}/{gml_filename}"

                # Load the file with GeoPandas
                self.gml_data = gpd.read_file(gml_path, driver="GML")

                return self.gml_data

    def get_surface(self, cadastral_ref):
        """Retrieves the surface area of a cadastral parcel based on its cadastral reference."""
        if self.gml_data is None:
            print("Error: GML data has not been loaded.")
            return None

        ref_column = "nationalCadastralReference"
        surface_column = "areaValue"

        if ref_column in self.gml_data.columns and surface_column in self.gml_data.columns:
            cadastral_parcel = self.gml_data[self.gml_data[ref_column] == cadastral_ref]

            if not cadastral_parcel.empty:
                surface = cadastral_parcel[surface_column].values[0]
                
            else:
                print(f"No cadastral parcel found with reference {cadastral_ref}")
                return None
        else:
            print("Required columns not found in the GML. Please check the file structure.")

def obtain_cadastral_ref():
    root = tk.Tk()
    root.withdraw()
    cadastral_ref = simpledialog.askstring("Input", "Enter the cadastral reference:")
    return cadastral_ref

def obtaining_url():
    url_gml = None

    def select():
        nonlocal url_gml
        selection = combo.get()
        label.config(text=f"Selected: {selection}")

        # Obtaining the URL
        postal_code = selection[:5]
        municipality = selection[6:]

        url_common = "http://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels"
        municipality_code = "38"
        cadastre_service_code = "A.ES.SDGC.CP."

        url_gml = url_common + "/" + municipality_code + "/" + selection + "/" + cadastre_service_code + postal_code + ".zip"

    # Create main window
    root = tk.Tk()
    root.title("Lista Desplegable en Tkinter")

    # Create a list of options
    options = ["38001-ADEJE", "38002-AGULO", "38003-ALAJERO", "38004-ARAFO", "38005-ARICO", "38006-ARONA", "38007-BARLOVENTO", "38008-BREÑA ALTA", "38009-BREÑA BAJA", "38010-BUENAVISTA DEL NORTE", "38011-CANDELARIA", "38027-EL PASO", "38054-EL PINAR DE EL HIERRO", "38032-EL ROSARIO", "38044-EL TANQUE", "38012-FASNIA", "38013-FRONTERA", "38014-FUENCALIENTE DE LA PALMA", "38015-GARACHICO", "38016-GARAFIA", "38017-GRANADILLA DE ABONA", "38019-GUIA DE ISORA", "38020-GUIMAR", "38021-HERMIGUA", "38022-ICOD DE LOS VINOS", "38018-LA GUANCHA", "38025-LA MATANZA DE ACENTEJO", "38026-LA OROTAVA", "38051-LA VICTORIA DE ACENTEJO", "38024-LOS LLANOS DE ARIDANE", "38031-LOS REALEJOS", "38042-LOS SILOS", "38028-PUERTO DE LA CRUZ", "38029-PUNTAGORDA", "38030-PUNTALLANA", "38033-SAN ANDRES Y SAUCES", "38023-SAN CRISTOBAL DE LA LAGUNA", "38034-SAN JUAN DE LA RAMBLA", "38035-SAN MIGUEL DE ABONA", "38036-SAN SEBASTIAN DE LA GOMERA", "38037-SANTA CRUZ DE LA PALMA", "38900-SANTA CRUZ DE TENERIFE", "38039-SANTA URSULA", "38040-SANTIAGO DEL TEIDE", "38041-SAUZAL", "38043-TACORONTE", "38045-TAZACORTE", "38046-TEGUESTE", "38047-TIJARAFE", "38049-VALLE GRAN REY", "38050-VALLEHERMOSO", "38048-VALVERDE", "38052-VILAFLOR DE CHASNA", "38053-VILLA DE MAZO"
    ]

    # Variable to store the selected value
    selected_value = tk.StringVar()

    # Create a combobox (dropdown list)
    combo = ttk.Combobox(root, values=options, state="readonly", textvariable=selected_value)
    combo.pack(pady=10)

    # Button to confirm selection
    boton = tk.Button(root, text="Select", command=select)
    boton.pack()

    # Label to display the selection
    label = tk.Label(root, text="")
    label.pack()

    # Start the aplication
    root.mainloop()

    return url_gml