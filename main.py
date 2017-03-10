import sublime
import sublime_plugin
import os
import re
import fnmatch

pathSlash ='/' if sublime.platform()!='windows' else '\\'

class SassAutocompleteCommand(sublime_plugin.EventListener):
    def on_activated(self, view):       
        isSass = Engine.isSass(view);
        isHtml = Engine.isHtml(view);
        if (isHtml and not len(Engine.htmlCompletionList)) or (isSass and not len(Engine.sassCompletionList)):
            Engine.runEngine(self,view)

    def on_post_save(self, view):        
        Engine.runEngine(self,view)

    def on_query_completions(self, view, prefix, locations):

        isSassCompletion = view.match_selector(locations[0], 'source.scss')
        isHtmlCompletion = view.match_selector(locations[0], 'text.html string.quoted')

        if isSassCompletion:
            return Engine.sassCompletionList
        if isHtmlCompletion:
            return Engine.htmlCompletionList

class Engine:
    sassCompletionList=[]
    htmlCompletionList=[]

    def loadSettings():
        return sublime.load_settings('sass-autocomplete.sublime-settings')

    def getHtmlExtensions():
        return Engine.loadSettings().get('extensions').get('html')

    def getSassExtensions():
        return Engine.loadSettings().get('extensions').get('sass')

    def getCurrentFileExtension(view):
        fileName=''
        extension=''

        if(isinstance(view,sublime.View)):
            fileName=view.file_name();
        else:
            fileName=view

        fileNameList=fileName.split('.')

        if len(fileNameList) > 1:
            extension=fileNameList[len(fileNameList) - 1]

        return extension

    def isSass(view):
        fileExtension=Engine.getCurrentFileExtension(view)
        return Engine.getSassExtensions().count(fileExtension) > 0

    def isHtml(view):
        fileExtension=Engine.getCurrentFileExtension(view)
        return Engine.getHtmlExtensions().count(fileExtension) > 0

    def getSassFolder(view):
        currentFilePath=view.file_name();
        sassDirIndex=currentFilePath.find("/scss/");
        sassFolder=''
        if sassDirIndex < 0:
            sassDirIndex=currentFilePath.find("/sass/");
        if sassDirIndex >= 0:
            sassDirIndex+=5
            sassFolder=currentFilePath[:sassDirIndex]
        return sassFolder


    def getFoldersFilesRecursively(folder):
        matches=[]

        for root, dirnames, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, '*.scss'):
                matches.append(os.path.join(root, filename))

        return matches


    def getSassFolderText(folder,view):
        code=''

        for file in Engine.getFoldersFilesRecursively(folder):
            code+=open(file,'r', encoding="utf8").read()

        return code


    def escapeDollar(text,replaceDollar=True):
        return text.replace('$','\$' if replaceDollar else '$')


    def escapeClosingCurlyBracet(text,replaceDollar=True):
        return text.replace('}','\}')


    def addFunctionsCompletion(pattern,code):
        functionsCompletion=[]

        for x in re.findall(pattern,code):
            functionName=Engine.escapeDollar(x[0])
            functionArguments=Engine.escapeDollar(x[2])

            zeroSlashesFunctionArguments=Engine.removeDollarSlashes(functionArguments)
            functionArguments=Engine.escapeClosingCurlyBracet(functionArguments)

            functionsCompletion.append((functionName+'('+zeroSlashesFunctionArguments+')',functionName+'(${1:'+functionArguments+'})'))

        return functionsCompletion


    def addMixinsCompletion(pattern,code):
        mixinsCompletion=[]

        for x in re.findall(pattern,code):
            mixinName=Engine.escapeDollar(x[0])
            mixinArguments=Engine.escapeDollar(x[2])

            zeroSlashesMixinArguments=Engine.removeDollarSlashes(mixinArguments)
            mixinArguments=Engine.escapeClosingCurlyBracet(mixinArguments)

            mixinsCompletion.append((mixinName+'('+zeroSlashesMixinArguments+')','@include '+mixinName+'(${1:'+mixinArguments+'})'))

        return mixinsCompletion


    def addVariablesCompletion(pattern,code):
        variablesCompletion=[]

        for x in re.findall(pattern,code):
            variableName=Engine.escapeDollar(x[0])
            variableValue=Engine.escapeDollar(x[1],False)

            variablesCompletion.append(('$'+variableName+'\t'+variableValue,'\$'+variableName))

        return variablesCompletion

    def addCssClassesCompletion(pattern,code):
        classesCompletion=[]

        for className in re.findall(pattern,code):
            item=('.'+className, className)
            if classesCompletion.count(item) <= 0:
                classesCompletion.append(item)

        return classesCompletion


    def removeDollarSlashes(text):
        return text.replace('\\','')


    def runEngine(self,view):
        if Engine.isSass(view):
            Engine.sassCompletionList=[]
            sassFolder=Engine.getSassFolder(view)
            if sassFolder != '':
                allSass=Engine.getSassFolderText(sassFolder, view)

                Engine.sassCompletionList+=Engine.addVariablesCompletion(r'\$([\w*-]*):(.*?);',allSass)
                Engine.sassCompletionList+=Engine.addMixinsCompletion('\@mixin ([\w*-]*)\s{0,}(\((.*?)\)|{|\n)',allSass)
                Engine.sassCompletionList+=Engine.addFunctionsCompletion('\@function ([\w*-]*)\s{0,}(\((.*?)\)|{|\n)',allSass)
        if Engine.isHtml(view):
            Engine.htmlCompletionList=[]
            currentProjectPath = view.window().folders()[0];
            allSass=Engine.getSassFolderText(currentProjectPath, view)

            Engine.htmlCompletionList+=Engine.addCssClassesCompletion('\.(-?[_a-zA-Z]+[_a-zA-Z0-9-]*)',allSass)
