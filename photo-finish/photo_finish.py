import xlrd
import os
import PIL
from PIL import Image, ImageDraw, ImageFont
from shutil import copyfile


#setup files
resource_dir = "img/"
input_dir = "input/"
output_dir = "output/"
result_file = "results.xlsx"
background_file = "background.jpg"
header_font = "c:/windows/Fonts/coopbl.ttf"
font_size = 50
font_colour = (0,0,0) 

workbook = xlrd.open_workbook(input_dir + result_file)
header_sheet = workbook.sheet_by_index(0)
result_sheet = workbook.sheet_by_index(1)

event = header_sheet.cell_value(0,2)
Date = header_sheet.cell_value(1,2)
weather = header_sheet.cell_value(2,2)

#create output file name based on event title
output_file = output_dir + event +".jpg"

#Draw the header info onto background image 
im= Image.open(resource_dir + background_file)
position = (600,00)
font = ImageFont.truetype(header_font, size=font_size)

draw = ImageDraw.Draw(im)
draw.text(position,event+'   '+Date+'\n'+ weather ,fill = font_colour,font = font)

im.save(output_file)
copyfile(input_dir+"results.xlsx", output_dir + event + "_results.xlsx")

#Pull results data from the spreadie 
data = [[result_sheet.cell_value(r,c) for c in range (result_sheet.ncols)]for r in range(result_sheet.nrows)]

#loop through and paste the cars onto the background
try:
    img = Image.open(output_file)
                
    for item in data:
        a, b, c = item
        driver = str(int(a))
        img2 = Image.open(resource_dir + driver + ".jpg")
        img.paste(img2,(int(b),int(c)))
        print(driver)
    img.save(output_file) 

except IOError:
    print (IOError)
    pass
    
    
