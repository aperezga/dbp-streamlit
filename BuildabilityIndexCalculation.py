import CadastralSiteArea

url_gml = CadastralSiteArea.obtaining_url()
cadastral_ref = CadastralSiteArea.obtain_cadastral_ref()
cadastral_data = CadastralSiteArea.GMLData(url_gml)
cadastral_data.process_gml()
cadastral_data.get_surface(cadastral_ref) # test reference: 1308102CS7511S