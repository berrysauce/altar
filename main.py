import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Union
import hashlib
import svgwrite

app = FastAPI(docs_url=None, redoc_url=None, openapi_url="/openapi")
templates = Jinja2Templates(directory="templates")

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")


# - FUNCTIONS - #

def binarize(string: str):
    # Create a SHA256 hash of the input string
    hash = hashlib.sha256(bytes(string, "utf-8")).hexdigest()
    
    # Convert hex string to decimal value
    decimal_value = int(hash, 16)
    
    # Convert decimal value to binary string, excluding the '0b' prefix
    binary_string = bin(decimal_value)[2:]
    
    # increase string length to 256 if not long enoughs
    while len(binary_string) < 256:
        binary_string = "0" + binary_string
    
    return binary_string # Returns a 256 long string of binary


# - ROUTES - #

@app.get("/")
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/docs")
def get_docs():
    # 301 - moved permanently
    # 302 - moved temporarily
    # redirecting to GitHub for now, maybe I'll make a docs site later
    return RedirectResponse("https://github.com/berrysauce/altar/blob/master/README.md#settings", status_code=302)

@app.get("/generate")
def get_identicon(data: str, color: Union[str, None] = None, size: Union[int, int] = 250):
    binarized = binarize(data)

    color_data = binarized[:58] # Trim to 58 bits
    field_data = binarized[58:] # Trim to 198 bits
    
    if color == None:
        segment_length = 6  # Length of each segment
        
        color_map = {
            0: "#5bc0eb", # blue - my fav :)
            1: "#fde74c", # yellow
            2: "#9bc53d", # green
            3: "#e55934", # red
            4: "#fa7921"  # orange
        }
        
        # get the first 6 bits of the color data
        color_data_segment = color_data[:6]
        
        # Convert the segment from binary to decimal
        decimal_value = int(color_data_segment, 2)
        
        # Use hashlib to generate a hash value based on the segment
        hash_value = hashlib.md5(str(decimal_value).encode()).hexdigest()
        
        # Convert the hash value to an integer
        hash_integer = int(hash_value, 16)
        
        # Map the integer value to an index within the range of available colors
        color_index = hash_integer % len(color_map)
        
        # Get the color based on the index
        color = color_map[color_index]
        
    else:
        color = "#" + color    
    
    fields = []
    
    for i in range(66):
        fields.append(field_data[:3]) # get first 3 bits
        field_data = field_data[3:] # then remove them

    field_fill = []
    
    for field in fields:
        # convert bits to list (010 -> [0, 1, 0])
        bit_list = list(field)
        
        # sum all bits
        bit_sum = int(bit_list[0]) + int(bit_list[1]) + int(bit_list[2])
        
        if bit_sum <= 1:
            field_fill.append(False)
        elif bit_sum >= 2:
            field_fill.append(True)

    # x, y, x-limit (see comments above) (max: 11,11,6)
    usable_grid_size = [5, 5, 3]
    
    # credits to ChatGPT lol, didn't know this existed
    dwg = svgwrite.Drawing("identicon.svg", profile="tiny")
    
    # Size of each identicon cell (e.g. 250 / 5 = 50)
    cell_size = size / usable_grid_size[0]
    
    # iterate through y
    for i in range(usable_grid_size[1]):
        row_list = []
        
        # iterate through x
        for j in range(usable_grid_size[2]):
            # i (row) * x (size, e.g. 11) + j (column index) -> list index
            if field_fill[i*usable_grid_size[2]+j] == True:
                # Calculate cell position
                x = j * cell_size
                y = i * cell_size

                # Draw cell rectangle with the assigned color
                dwg.add(dwg.rect((x, y), (cell_size, cell_size), fill=color))
            else:
                pass # pass instead of continue because continue would skip the row_list appending
            
            # make a speperate list for reversing
            row_list.append(field_fill[i*usable_grid_size[2]+j])
        
        # reverse the list & remove the first element (the middle one / x-limit)
        row_list_reversed = list(reversed(row_list))[1:]
        
        # make a seperate index for the reversed list since k is not an index like j
        row_list_index = 0
        
        for k in row_list_reversed:
            if k == True:
                # Calculate cell position
                x = (row_list_index + usable_grid_size[2]) * cell_size
                y = i * cell_size

                # Draw cell rectangle with the assigned color
                dwg.add(dwg.rect((x, y), (cell_size, cell_size), fill=color))
            else:
                pass # pass instead of continue because continue would skip the index increment
            row_list_index += 1
    
    # Get the SVG as a string
    svg_string = dwg.tostring()

    # Set the response type to SVG
    return Response(content=svg_string, media_type="image/svg+xml")


# - RUNNER - #

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)