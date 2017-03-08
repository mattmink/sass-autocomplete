class Engine:
    completionList=[]

    def isSass(myview):
        extension='.scss'

        if(isinstance(myview,sublime.View)):
            return myview.file_name().endswith(extension)
        else:
            return myview.endswith(extension)

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


    def removeDollarSlashes(text):
        return text.replace('\\','')


    def runEngine(self,view):
        if Engine.isSass(view):
            Engine.completionList=[]
            sassFolder=Engine.getSassFolder(view)
            if sassFolder != '':
                allSass=Engine.getSassFolderText(sassFolder, view)

                Engine.completionList+=Engine.addVariablesCompletion(r'\$([\w*-]*):(.*?);',allSass)
                Engine.completionList+=Engine.addMixinsCompletion('\@mixin ([\w*-]*)\s{0,}(\((.*?)\)|{|\n)',allSass)
                Engine.completionList+=Engine.addFunctionsCompletion('\@function ([\w*-]*)\s{0,}(\((.*?)\)|{|\n)',allSass)
