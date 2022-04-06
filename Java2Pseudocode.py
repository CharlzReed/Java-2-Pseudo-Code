from random import randint
import os

def main(filePath):
    if os.path.isfile(filePath):
        with open(filePath, 'r') as file:
            lines = file.read()
    else:
        return "File not found"

    class_name = lines[lines.index("public class") + 12 : lines.index("{")].strip()
    method_starts = ['public', 'private', 'protected']
    var_types = ['int', 'double', 'float', 'long', 'short', 'byte', 'char', 'boolean', 'Boolean', 'String']
    statement_start = ["for", "while", "if", "else", "try", "catch", "switch", "except", "throw"]
    operator_sub = {
        '.equals(': ' is equivalent to ',
        '.contains(' : ' contains ',
        '.length()': "'s length",
        '.substring(': " substring ",

        ' >= ': ' is greater than or equal to ',
        ' <= ': ' is less than or equal to ',
        ' != ': ' is not equal to ',
        ' == ': ' is equivalent to ',
        ' && ': ' and ',
        ' || ': ' or ',

        ' + ': ' plus ',
        ' - ': ' minus ',
        ' * ': ' times ',
        ' / ': ' divided by ',
        ' !': '  not  ',
        ' % ': ' modulus ',
        ' = ': ' equals ',
        ' > ': ' is greater than ',
        ' < ': ' is less than ',
        ' : ': ' in ',
    }


    def get_indent_level(String):
        return (len(String) - len(String.lstrip())) * " "


    while lines.count('/*') > 0:
        lines = lines.replace(lines[lines.index('/*'):lines.index('*/') + 2], '')
    while lines.count('//') > 0:
        startpoint = lines.index('//')
        endpoint = lines.index('\n', startpoint)
        lines = lines.replace(lines[startpoint:endpoint], '')
    while lines.count('\nimport') > 0:
        startpoint = lines.index('\nimport')
        endpoint = lines.index('\n', startpoint + 2)
        lines = lines.replace(lines[startpoint:endpoint], '')
    while lines.count('package') > 0:
        startpoint = lines.index('package')
        endpoint = lines.index('\n', startpoint)
        lines = lines.replace(lines[startpoint:endpoint], '')
        
    lines = lines.split('\n')

    counter = 0
    while counter < len(lines):
        if len(lines[counter]) * ' ' == lines[counter]:
            del lines[counter]
        else:
            counter += 1

    any_direction = ["+", "-", "*", "/", "!", "%", "=", ">", "<", ":", "<=", ">=", "!=", "==", "&&", "||"]
    char_last = [";", "]", "}", ")", ","]
    char_first = ["(", "[", "{"]
    leave_alone = ["++", "--"]
    alphanumeric = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    combos = {}
    for char in alphanumeric:
        for sign in any_direction:
            combos[char + sign] = char + " " + sign
            combos[sign + char] = sign + " " + char
        for sign in leave_alone:
            combos[char + sign] = char + sign
            combos[sign + char] = sign + char
        for char in char_last:
            combos[sign + char] = sign + " " + char
        for char in char_first:
            combos[char + sign] = char + " " + sign

    for i in range(len(lines)):
        for key, value in combos.items():
            # check if the key is inside a string
            if key in lines[i]:
                if '"' in lines[i] and lines[i].count('"') % 2 == 1:
                    if lines[i].index(key) < lines[i].index('"') or lines[i].index(key) > lines[i].rindex('"'):
                        continue
                    else:
                        lines[i] = lines[i].replace(key, value)
                        continue



    for i in range(len(lines)):
        indents = get_indent_level(lines[i])
        


        if " = " in lines[i] and lines[i].strip().split(" ")[0] in var_types:
            var = lines[i].strip().split(" ")
            var = indents + "Create new variable called " + var[1] + ", of type " + var[0]
            lines[i] = var


        elif " = " in lines[i] and lines[i].strip().split(" ")[0] not in statement_start and lines[i].strip().split(" ")[0] not in method_starts:
            var = lines[i].strip().split(" = ")
            var = indents + "Set " + var[0] + " to " + var[1]
            lines[i] = var
        
        if "[" in lines[i] and "]" in lines[i] and " = new" not in lines[i]:
            var = lines[i].replace("[", " at index ").replace("]", " ")
            lines[i] = var

        elif "for (" in lines[i]:
            if ":" not in lines[i]:
                var = lines[i].strip().split(";")
                iterator = var[0][5:].replace("=", "equals")
                condition = var[1][1:].strip()
                increment = var[2][1:].strip()[:-3]
                var = indents + "For loop (starting at " + iterator + " and continuing while " + condition + ", incrementing by " + increment + ") {"
            else:
                var = lines[i].strip().split(" ")
                var = var
                dataset = var[-2]
                iterator = str(var[1]) + " " + str(var[2])
                iterator = iterator.replace('(', '').replace(')', '')
                var = indents + "For loop (to iterating through the '" + dataset + "' dataset containing " + iterator + ") {"
            lines[i] = var
        

        elif "if (" in lines[i]:
            var = lines[i][lines[i].index("(") + 1:lines[i].rindex(")")].strip()
            var = var
            var = indents + "If (" + var + ") {"
            lines[i] = var
        

        elif lines[i].strip().split(" ")[0] in method_starts and "class" not in lines[i] and "{" in lines[i] and class_name not in lines[i]:
            var = lines[i].replace("(", " ( ")
            var = var.replace(")", " ) ")
            var = var.strip().split(" ")
            var = [x for x in var if x != '']
            modifier = var[0]
            static = " " + var[1] if var[1] == "static" else ""
            if static != "":
                return_type = var[2].strip()
                method_name = var[3].strip()
                parameters = var[4:]
            else:
                return_type = var[1].strip()
                method_name = var[2].strip()
                parameters = var[3:]
            parameters = " ".join(parameters)
            parameters = parameters[ : parameters.index("{") - 1]
            parameters = parameters.replace("( ", "(").replace(" )", ")")
            var = indents + "Start of " + modifier + static + " method called " + method_name + ", with parameters " + parameters + ", and return type " + return_type + " {"
            lines[i] = "\n\n\n" + "=+=+=+=+=\n" + indents + "Pre-condition: " + parameters + "\n" + indents + "Post-condition: " + return_type + "\n=+=+=+=+=\n" + var
    

        elif lines[i].strip().split(" ")[0] in method_starts and "class" not in lines[i] and class_name in lines[i] and ")" in lines[i]:
            var = lines[i].strip().replace("("," ( ").replace(")"," )").split(" ")
            parameters = var[3:var.index(")")]
            parameters = "(" + " ".join(parameters) + ")"
            var = indents + "Start of constructor method called " + class_name + ", with parameters " + parameters + ", and no return type {"
            lines[i] = "\n" + "=+=+=+=+=\n" + indents + "Pre-condition: " + parameters + "\n" + indents + "Post-condition: None\n=+=+=+=+=\n" + var
        

        elif ".add(" in lines[i]:
            var = lines[i][ : lines[i].index(".add(")].strip()
            parameter = lines[i][lines[i].index("(") + 1:lines[i].rindex(")")]
            var = indents + "Add " + parameter + " to " + var
            lines[i] = var
        elif ".addAll(" in lines[i]:
            var = lines[i][ : lines[i].index(".addAll(")].strip()
            parameter = lines[i][lines[i].index("(") + 1:lines[i].rindex(")")]
            var = indents + "Add all items from " + parameter + " to " + var
            lines[i] = var
        elif ".remove(" in lines[i]:
            var = lines[i][ : lines[i].index(".remove(")].strip()
            parameter = lines[i][lines[i].index("(") + 1:lines[i].rindex(")")]
            var = indents + "Remove " + parameter + " from " + var
            lines[i] = var


    
    lines = "\n".join(lines)
    lines = lines.split("\n")
    
    for i in range(len(lines)):
        indents = get_indent_level(lines[i])
        if "  " in lines[i].strip():
            var = lines[i].strip().replace("  ", " ")
            lines[i] = indents + var
        
        elif lines[i].strip().split(" ")[0] in method_starts and "class" not in lines[i] and "{" not in lines[i] and class_name not in lines[i]:
            var = lines[i].strip().split(" ")
            modifier = var[0]
            static = " " + var[1] if var[1] == "static" or var[1] == "final" else ""
            if static != "":
                var_type = var[2].strip()
                var_name = var[3].strip()
            else:
                var_type = var[1].strip()
                var_name = var[2].strip()
            var = indents + "Create new field called " + var_name[:-1] + ", of type " + var_type
            lines[i] = var
        

    for i in range(len(lines)):
        for j in operator_sub.keys():
            lines[i] = lines[i].replace(j, operator_sub[j])

    return "\n".join(lines)


# create list of every file in the directory
def get_files():
    files = []
    for (dirpath, dirnames, filenames) in os.walk('.'):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

# create a directory for the output located in the same directory as Java2PseudoCode.py
def create_output_directory():
    if not os.path.exists("output"):
        os.makedirs("output")
    #return the path to the output directory
    return os.path.join(os.getcwd(), "output")

allFiles = get_files()
dumpLocation = create_output_directory()

for fileName in allFiles:
    if fileName.endswith(".java"):
        print("Converting " + dumpLocation + "\\" + fileName.split("\\")[-1] + "(pseudo)" + ".txt")
        try:
            pseudo = main(fileName)
        except:
            pseudo = "Error converting file"
        with open(dumpLocation + "\\" + fileName.split("\\")[-1][:-5] + "PSEUDO" + str(randint(100,999)) + ".txt", "w") as f:
            f.write(pseudo)
        print("Done!")
