from fastapi import FastAPI, Request, Response, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from typing import Union
import svgwrite
import hashlib
import os

load_dotenv()
API_KEY = os.getenv("API_KEY") # API key (optional)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    if API_KEY:
        if api_key_header == API_KEY:
            return api_key_header
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API Key",
            )
    else:
        return None


# NOTE
#
# I've tried to add as many comments as possible to explain the way Altar generates identicons.
# I hope they'll help you with figuring it out yourself or just understanding the code.
#
# For transparency reasons: 
# ChatGPT actually helped me especially with the color generation. The majority is built from the ground up though.


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
    return {"detail": "Altar Identicon API"}

@app.get("/generate")
def get_identicon(
        data: str, 
        color: Union[str, None] = None, 
        background: Union[str, None] = None, 
        size: Union[int, int] = 250,
        api_key: str = Security(get_api_key)
    ):
    binarized = binarize(data)

    color_data = binarized[:58] # Trim to 58 bits
    field_data = binarized[58:] # Trim to 198 bits
    
    if color == None:
        segment_length = 6  # Length of each segment
        
        color_map = {
            0: "#126ce2", # blue - my fav :)
            1: "#f7ce00", # yellow
            2: "#2cce1a", # green
            3: "#d63128", # red
            4: "#ed5204"  # orange
        }
        
        # get the first 6 bits of the color data
        color_data_segment = color_data[:segment_length]
        
        # Convert the segment from binary to decimal
        decimal_value = int(color_data_segment, 2)
        
        # Use hashlib to generate a hash value based on the segment
        hash_value = hashlib.md5(str(decimal_value).encode()).hexdigest()
        
        # Convert the hash value to an integer
        # thanks again ChatGPT! This conversion introduces a lot of randomness as the hash integer is quite large
        # the line below (hash_integer % len(color_map)) devides the hash integer by the length of the color map (in this case 5)
        # and returns the remainder, which is then used as the index for the color map
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
    
    if background != None:
        if background == "light":
            background = "#ffffff"
        elif background == "dark":
            background = "#212121"
        else:
            background = "#" + background
            
        try:
            dwg.add(dwg.rect((0, 0), (size, size), fill=background)) # fill background
        except TypeError:
            raise HTTPException(status_code=400, detail="Invalid background color – only pass on HEX colors without the '#' prefix or 'light'/'dark'")
    
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
                try:
                    dwg.add(dwg.rect((x, y), (cell_size, cell_size), fill=color))
                except TypeError:
                    raise HTTPException(status_code=400, detail="Invalid fill color – only pass on HEX colors without the '#' prefix")
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
                try:
                    dwg.add(dwg.rect((x, y), (cell_size, cell_size), fill=color))
                except TypeError:
                    raise HTTPException(status_code=400, detail="Invalid fill color – only pass on HEX colors without the '#' prefix")
            else:
                pass # pass instead of continue because continue would skip the index increment
            row_list_index += 1
    
    # Get the SVG as a string
    svg_string = dwg.tostring()

    # Set the response type to SVG
    return Response(content=svg_string, media_type="image/svg+xml")


# - RUNNER - #

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
