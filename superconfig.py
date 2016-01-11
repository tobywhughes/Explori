#File interprets the config.cfg file and returns a config object for the main file to use. Will also eventually allow ways to change the config file from inside Explori session


class Config:
    
    def __init__(self):

        #Initialize DEF values
        self.width = 150
        self.height = 450
        self.tab_width = 150
        self.tab_height =  20
        self.title =  "Explori"
        self.color_dict = {}

        self.read_data()

    def read_data(self):
        with open('config.cfg', 'r') as config_file:
            for current_line in config_file:
                #Splits line by white spaces
                current_line_parsed = current_line.split()

                #Grabs data that happens to be in config file
                if len(current_line_parsed) == 0:
                    pass
                elif current_line_parsed[0][0] == '#':
                    pass
                elif current_line_parsed[0] == 'STYLE':
                    if current_line_parsed[1] == 'DEF':
                        break
                elif current_line_parsed[0] == 'WIDTH':
                    if current_line_parsed[1] != 'DEF':
                        self.width = int(current_line_parsed[1])
               
                elif current_line_parsed[0] == 'HEIGHT':
                    if current_line_parsed[1] != 'DEF':
                        self.height = int(current_line_parsed[1])

                elif current_line_parsed[0] == 'TABWIDTH':
                    if current_line_parsed[1] != 'DEF':
                        self.tab_width = int(current_line_parsed[1])
    
                elif current_line_parsed[0] == 'TABHEIGHT':
                    if current_line_parsed[1] != 'DEF':
                        self.tab_height = int(current_line_parsed[1])
    
                elif current_line_parsed[0] == 'TITLE':
                    if current_line_parsed[1] != 'DEF':
                        self.title = current_line_parsed[1][1:-2]

                elif current_line_parsed[0] == 'FOLDER':
                    self.color_dict['FOLDER'] = int(current_line_parsed[1]), int(current_line_parsed[2]), int(current_line_parsed[3]), int(current_line_parsed[4])

                elif current_line_parsed[0][0] == '.':
                    self.color_dict[current_line_parsed[0][1:]] = int(current_line_parsed[1]), int(current_line_parsed[2]), int(current_line_parsed[3]), int(current_line_parsed[4])
