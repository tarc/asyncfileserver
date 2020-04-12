class REPLCommand(object):
    def start(self):
        return True

    def stop(self):
        return False

    def quit(self):
        return False

    def error(self):
        return False
