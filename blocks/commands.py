import sublime
import sublime_plugin
import os
import re
import fnmatch

pathSlash ='/' if sublime.platform()!='windows' else '\\'

class SassAutocompleteCommand(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        isSass = Engine.isSass(view);
        isHtml = Engine.isHtml(view);
        isNewView = Engine.currentProjectPath != view.window().folders()[0];
        if isNewView or (isHtml and not len(Engine.htmlCompletionList)) or (isSass and not len(Engine.sassCompletionList)):
            Engine.runEngine(self,view)

    def on_post_save_async(self, view):
        isSass = Engine.isSass(view);
        if(isSass):
            Engine.runEngine(self,view)

    def on_query_completions(self, view, prefix, locations):
        isSassCompletion = view.match_selector(locations[0], 'source.scss')
        isHtmlCompletion = view.match_selector(locations[0], 'text.html string.quoted')

        if isSassCompletion:
            return Engine.sassCompletionList
        if isHtmlCompletion:
            return Engine.htmlCompletionList
