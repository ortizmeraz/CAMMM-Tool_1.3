import shapefile

P=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\NetWorkProduction\Lines_VilleMarie.shp"
Pr=P
Pr=str(P.split(".shp")[0])+".prj"
print(Pr)
# f=open(Pr)
# for Line in f.readlines():
#     print(Line)


# sf = shapefile.Reader(P)


from epsg_ident import EpsgIdent

ident = EpsgIdent()
ident.read_prj_from_file(Pr)
print(ident.get_epsg(),type(ident.get_epsg()))