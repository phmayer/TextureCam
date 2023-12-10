import requests

pic = open('C:/Users/Philipp/Desktop/WS2324_KIT/repos/TextureCam/exmple_pictures/example.JPG', 'rb')


response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': pic},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'ewob8qd3EsiDV1KRGE1ATgH6'},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)


"""
takes an input image + options as booleans
returns array of output images
"""
#def processImage(inputImage, removeBg, wantNormalMap, wantDisplacement, wantAmbientOcc, wantSpecular)


"""
takes an input image
returns all 4 maps for the image in an dict
"""
def getMapsForImage(inputImage)
    

