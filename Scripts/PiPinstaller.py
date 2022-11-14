import os
def Update():
    # os.system('/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7 -m pip install --upgrade pip')
    os.system("sudo apt update")
    os.system("sudo apt upgrade -y")
    os.system("sudo apt-get -y install python3-pip")
    os.system("sudo apt-get install python3-tk")
    os.system("pip3 install pyproj")
    os.system("pip3 install pyproj")
    os.system("pip3 install networkx")
    os.system("pip3 install numpy")
    os.system("pip3 install pandas")
    os.system("pip3 install colour")
    os.system("pip3 install pyproj")
    os.system("pip3 install jenkspy")
    os.system("pip3 install plotly")
    os.system("pip3 install statistics")
    os.system("pip3 install geojson")
    os.system("pip3 install epsg-ident")
    os.system("pip3 install Pillow")
    os.system("pip3 install scipy")
    os.system("pip3 install six")
    os.system("pip3 install pyshp")
    os.system("pip3 install fiona")
    os.system("pip3 install geopandas")
    os.system("pip3 install matplotlib")
    os.system("pip3 install Cython")
    os.system("pip3 install utm")
    os.system("pip3 install colorama")
    os.system("pip3 install tqdm")
    os.system("pip3 install Calculations")


if __name__ == "__main__":
    Update()

    