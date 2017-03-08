import sublime
import sublime_plugin
import os
import re
import fnmatch

pathSlash ='/' if sublime.platform()!='windows' else '\\'

class SassAutocompleteCommand(sublime_plugin.EventListener):
    def on_activated(self, view):       
        if not len(Engine.completionList):
            Engine.runEngine(self,view)
            print(Engine.completionList)

    def on_post_save(self, view):        
        Engine.runEngine(self,view)

    def on_query_completions(self, view, prefix, locations):

        isSass = view.match_selector(locations[0], 'source.scss')
        if isSass:
            return Engine.completionList
