import sublime

import json
import os
import sys

class Settings():

    settings = {}

    def __init__(self,view=None):

        with open(sublime.packages_path() + "/CodeSync/CodeSync.sublime-settings","r") as f:
            self.settings = json.load(f)

        if view != None:
            selection = sublime.Region(0, view.size())
            # get the text
            text = view.substr(selection)

            if text.startswith("#@ SYNCCODE STREAM") or text.startswith("#@ SYNCCODE RECIVE"):

                lines = list(filter(lambda x: x if x[:2] == "#@" else None,text.split("\n")))

                if len(lines) >= 2:
                    string = ""
                    for line in lines[1:]:
                        string += line

                    options_lenght = len(string)
                    string = string.replace("#@","")

                    try:
                        dictionary = json.loads(string)
                        self.settings.update(dictionary)
                    except:
                        print("cant parse file options")
                        print(string)

                    self.settings.update({"index_offset":18 + options_lenght})
                else:
                    self.settings.update({"index_offset":18})
            else:
                self.settings.update({"index_offset":0})


