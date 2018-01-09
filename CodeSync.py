import sublime
import sublime_plugin
import threading
import socket
import time
from .Settings import Settings

#########################################################################################################
def whole_region(view,index):
    return sublime.Region(index, view.size())

def get_text(view,index):
    # set timeout
    selection = sublime.Region(index, view.size())
    # get the text
    text = view.substr(selection)
    return text

#########################################################################################################
# Extends TextCommand so that run() receives a View to modify.
class SyncCodeListener(sublime_plugin.EventListener ):

    # when you open a file
    def on_load_async(self, view):
        view.run_command("sync_code_stream")
    # when you save a file
    def on_pre_save_async(self, view):
        view.run_command("sync_code_stream")

    def on_modified_async(self,view):
        view.run_command("sync_code_syncable_checker")

#########################################################################################################
class SyncCodeSyncableCheckerCommand(sublime_plugin.TextCommand):

    def run(self,edit):
        if self._check_if_streammable():
            self.view.run_command("sync_code_send_update")
        elif  self._check_if_recivable():
            self.view.run_command("sync_code_recive")

    def _check_if_streammable(self):
        text = get_text(self.view,0)
        return text.startswith("#@ SYNCCODE STREAM")

    def _check_if_recivable(self):
        text = get_text(self.view,0)
        return text.startswith("#@ SYNCCODE RECIVE")


#########################################################################################################
class SyncCodeSendUpdateCommand(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
        self.settings = Settings(view).settings

    def run(self,edit):
        self._start_sync()

    def _start_sync(self):
        if SyncCodeSyncableCheckerCommand(self.view)._check_if_streammable():
            data = get_text(self.view,self.settings["index_offset"])
            t = SendToServer_Thread(data,self.view)
            t.start()



# view.run_command("sync_code_stream")
class SyncCodeStreamCommand(sublime_plugin.TextCommand):

    def __init__(self,view):
        self.view = view
        self.settings = Settings(view).settings

    def run(self,edit):
        self._start_sync()

    def _start_sync(self):

        if SyncCodeSyncableCheckerCommand(self.view)._check_if_streammable():
            self._send_to_server()

    def _send_to_server(self):
        t = SendToServer_Thread(data,self.view)
        t.start()

class SendToServer_Thread (threading.Thread): 
        
    def __init__(self,data,view):
        threading.Thread.__init__(self)
        self.data = data
        self.settings = Settings(view).settings

    def run(self):

        host = self.settings["ip"]   
        port = self.settings["port"]                  
         # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(self.data.encode())
        s.close()

#########################################################################################################

# view.run_command("sync_code_recive")
class SyncCodeReciveCommand(sublime_plugin.TextCommand):

    def __init__(self,view):
        self.view = view
        self.settings = Settings(view).settings

    def run(self,edit):
        t = ReciveFromServer_Thread(self.view,edit)
        t.start()


class ReciveFromServer_Thread (threading.Thread):


    def __init__(self,view,edit):
        
        threading.Thread.__init__(self)
        self.settings = Settings(view).settings
        self.view = view
        self.edit = edit

    def run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(( '',self.settings["port"]))
            s.listen(1)
            while SyncCodeSyncableCheckerCommand(self.view)._check_if_recivable():
                conn, addr = s.accept()
                print('Connected by', addr)
                data = conn.recv(self.settings["buffer_size"])
                conn.close()
                self.view.run_command("code_sync_view_edit",{"data":data.decode()})
        except:
            pass
            
class CodeSyncViewEditCommand(sublime_plugin.TextCommand):

    def __init__(self,view):
        self.view = view
        self.settings = Settings(view).settings


    def run(self,edit,data):
        self.edit = edit
        self.view.replace(self.edit,whole_region(self.view,self.settings["index_offset"]),data)

        #old = self. _get_text()
        #index = 0
        #for line1,line2 in zip(old.split("\n"),data.split("\n")):
        #    index += len(line2)
        #    if line1 == line2:
        #        pass
        #    else:
        #        self.view.erase(self.edit,sublime.Region(index,index + len(line1)))
        #        self.view.insert(self.edit,index,line1)
