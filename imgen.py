from PIL import Image, ImageFont, ImageDraw
import random
import os
import requests
from io import BytesIO

# Construct final twitter image
class Twimage:

    def __init__(self, match_info):
        self.event = match_info.event
        self.round = match_info.round
        self.map_info = match_info.map_info
        self.team_info = match_info.team_info
        self.mvp_info = match_info.mvp_info
        self.mvp = {

            "name": self.mvp_info['name'],
            "K/D": self.mvp_info['kills'] + "/" + self.mvp_info['deaths'] + "/" + self.mvp_info['assists'],
            "ACS": self.mvp_info['acs'],
            "+/-": self.mvp_info['pm'],
            "HSP": self.mvp_info['hsp'],
            "agent": self.mvp_info['agent'],
            "img": self.mvp_info['url']

        } 
        self.template = Image.new("RGBA", (1600, 900), (0, 0, 0, 0))
        self.font = ImageFont.truetype("Assets\MISC\RussoOne-Regular.ttf", 100)
        team_names = [team_name for team_name in self.team_info.keys()]
        self.team1 = team_names[0]
        self.team2 = team_names[1]
        self.mvp_guy_link = self.mvp['img']

#Function to change a url into an image

    def urlpull(self, url):
        team_logo = requests.get(url)
        return Image.open(BytesIO(team_logo.content)).convert("RGBA")

# Choose random background image (stages) and add final box and MVP box

    def create_background(self):

        stages = os.listdir("Assets/STAGES")
        image_path = ("Assets/STAGES/" + str(random.choice(stages)))
        image_to_paste = Image.open(image_path).convert("RGBA")
        self.template.paste(image_to_paste, (0,0,1600,900), mask=image_to_paste)
        
        boiler_path = ("Assets\MISC\FINAL_BOX_MVP_CARD.png")
        boiler_to_paste = Image.open(boiler_path).convert("RGBA")
        self.template.paste(boiler_to_paste, (0,0,1600,900), mask=boiler_to_paste)

# Add team logos and final match score

    def final_score(self):
        
        

        logo1_url = self.team_info[self.team1]["logo"]
        logo2_url = self.team_info[self.team2]["logo"]

        logo1_img = self.urlpull(logo1_url)
        logo2_img = self.urlpull(logo2_url)

        logo1_img.thumbnail((130, 130), reducing_gap=2.0)
        self.template.paste(logo1_img, (87, 283), mask=logo1_img)

        logo2_img.thumbnail((130, 130), reducing_gap=2.0)
        self.template.paste(logo2_img, (523, 283), mask=logo2_img)

        draw = ImageDraw.Draw(self.template)

        start_x = 216
        end_x = 520
        start_y = 283
        end_y = 420

        matchscore_text = str(self.team_info[self.team1]['maps_won']) + " - " + str(self.team_info[self.team2]['maps_won'])

        text_width = draw.textlength(matchscore_text, font=self.font)
        center_x = (end_x - start_x) / 2 + start_x
        center_y = (end_y - start_y) / 1.4 + start_y

        draw.text((center_x - text_width / 2, center_y - 100), matchscore_text, font=self.font, fill="white")
        
# Add each map icon for the maps that were played and add boxes to them (adjust for series length) and add map scores 

    def add_maps(self):
        
        base_space_val = 100
        map_count = len(self.map_info)
        if map_count == 1:
            space_increment = 30
        else:
            space_increment = base_space_val//map_count
        start_coords = [81, 410]
        if map_count == 1:
            end_coords = [81, 620]
        else:
            end_coords = [81, (820 - space_increment)]
        vertical_space = (end_coords[1] - start_coords[1])
        negative_space = space_increment * (map_count)
        
        
        map_box = Image.open("Assets\MISC\map_box_transparent.png").convert("RGBA")

        map_box_width = (map_box.size[0])

        if map_count == 1:
            map_box_height = int((vertical_space - negative_space) / 1.5)   

        else:
            map_box_height = (vertical_space - negative_space) // map_count

        resized_map_box = map_box.resize((map_box_width, map_box_height))
        first_gap = space_increment
        map_box_gap = (space_increment + map_box_height)

        for check_TBD in self.map_info:
            if check_TBD == 'TBD':
                del self.map_info['TBD']
                break

        j = 0
        for current_map in self.map_info:


            map_dir = "Assets\MAPS\Loading_Screen_" + current_map + ".png"
            map_image = Image.open(map_dir).convert("RGBA")

            resized_map_image = map_image.resize((map_box_width//3, map_box_height))
            self.template.paste(resized_map_image, (73, (start_coords[1] + (map_box_gap)*(j)) + first_gap*(j+1)), mask=resized_map_image)

            j += 1

        for i in range(map_count):
            
            self.template.paste(resized_map_box, (73, (start_coords[1] + (map_box_gap)*(i)) + first_gap*(i+1)), mask=resized_map_box)
        
        text_indent  = map_box_height//10
        text_size = (map_box_height - 6*(text_indent))
        

        font = ImageFont.truetype("Assets\MISC\RussoOne-Regular.ttf", text_size)
        draw = ImageDraw.Draw(self.template)

        W = resized_map_box.size[0]

        logo_size = (text_size)

        logo1_url = self.team_info[self.team1]["logo"]
        logo2_url = self.team_info[self.team2]["logo"]

        logo1_img = self.urlpull(logo1_url)
        logo2_img = self.urlpull(logo2_url)

        logo1_img.thumbnail((logo_size, logo_size), reducing_gap=2.0)
        logo2_img.thumbnail((logo_size, logo_size), reducing_gap=2.0)

        k = 0
        for map in self.map_info:

            score  = self.map_info[map]['score'][0] + " - " + self.map_info[map]['score'][1]

            _, _, w, _ = draw.textbbox((0, 0), score, font=font)
            text_offset = ((W - w)/2)
            draw.text((73 + text_offset, (2.5*text_indent + start_coords[1] + (map_box_gap)*(k)) + first_gap*(k+1)), score, font=font, fill="white")
            TEXT_X_POS = int(73 + text_offset)

            for team in self.team_info:
                
                if (team) == (self.team1):

                    KRU_X_POSITION = 73 + int(text_offset) - int(text_offset)//3
                    GAP_TEXT = TEXT_X_POS - (KRU_X_POSITION + logo1_img.size[0])
                    self.template.paste(logo1_img, (73 + int(text_offset) - int(text_offset)//3, (3*text_indent + start_coords[1] + (map_box_gap)*(k)) + first_gap*(k+1)), mask=logo1_img)

                else:

                    self.template.paste(logo2_img, (73 + int(text_offset) + w + GAP_TEXT, (3*text_indent + start_coords[1] + (map_box_gap)*(k)) + first_gap*(k+1)), mask=logo2_img)

            k += 1

# Add MVP image and stats and agent

    def add_mvp(self):

        start_coords = [757, 740]
        end_coords = [1031, 740]
        draw = ImageDraw.Draw(self.template)
        text_size = 21
        

        mvp_agent = self.mvp['agent']
        mvp_name = self.mvp['name']

        i = 0
        for stat in self.mvp:

            font = ImageFont.truetype("Assets\MISC\RussoOne-Regular.ttf", text_size)

            if self.mvp[stat] == (mvp_name):

               
                name_coords = [758, 680]
                #name_end_coords = [1020, 234]
                text_name_construction = str((self.mvp[stat]))
                font = ImageFont.truetype("Assets\MISC\RussoOne-Regular.ttf", 40)
                _, _, w, _ = draw.textbbox((0, 0), text_name_construction, font=font)
                #name_centered = (name_coords[0] + ((name_end_coords[0]) - name_coords[0] - w)/2)
                draw.text((name_coords[0], name_coords[1]), text_name_construction, font=font, fill='white')
                i += 1
                continue

            if self.mvp[stat] == (mvp_agent):
                i += 1
                continue

            text_construction = str(list(self.mvp.keys())[list(self.mvp.values()).index(self.mvp[stat])]) + ":  " + str(self.mvp[stat])
            _, _, w, _ = draw.textbbox((0, 0), text_construction, font=font)
            
            if i == 1:
                draw.text((start_coords[0], start_coords[1] + 50*((i-1))) , text_construction, font = font, fill='white')
            if i == 2:
                draw.text((end_coords[0] - w, start_coords[1] + 50*((i-2))) , text_construction, font = font, fill='white')
            if i == 3:
                draw.text((start_coords[0], start_coords[1] + 50*((i-2))) , text_construction, font = font, fill='white')
            if i == 4:
                draw.text((end_coords[0] - w, start_coords[1] + 50*((i-3))) , text_construction, font = font, fill='white')
            
            i += 1
        #AGENTS\Skye_Artwork_Full.png
        agent_image = Image.open("Assets\AGENTS\\" + mvp_agent + "_Artwork_Full.png").convert("RGBA") 
        agent_image.thumbnail((1500, 1500), reducing_gap=2.0)

        self.template.paste(agent_image, (850, -20), mask=agent_image)

        mvp_img = self.urlpull(self.mvp_guy_link)
        resized_mvp_img = mvp_img.resize((250, 250), reducing_gap= 2.0)
        self.template.paste(resized_mvp_img, (770, 323), mask=resized_mvp_img)

#Add stage name and round

    def add_stageinfo(self):
        
        start_coords = [75, 35]
        draw = ImageDraw.Draw(self.template)
        text_size = 22

        text_construction = str(self.event) + ": (" + str(self.round) + ")"

        font = ImageFont.truetype("Assets\MISC\RussoOne-Regular.ttf", text_size)
        draw.text((start_coords[0], start_coords[1]), text_construction, font=font, fill='white')

# Construct final image    

    def construct_image(self):
        self.create_background()
        self.final_score()
        self.add_maps()
        self.add_mvp()
        self.add_stageinfo()
        return self.template
