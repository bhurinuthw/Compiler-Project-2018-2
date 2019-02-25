import datetime
import regexParser as rp


def regex_preformatter(regex):
    temp = ""
    iteration = 0
    operator_list = ['(', '|', '*', ')', '_']
    for character in regex:
        temp = temp + character
        if(iteration == len(regex)-1):
            break
        if(regex[iteration+1] not in operator_list):
            if(character not in operator_list):
                temp = temp + '_'

        iteration += 1

    return temp

def regex_formatter(regex_list):

    parse = 'regex_list = ['
    temp = regex_list
    for regex in regex_list:
        name = regex[0]
        regex = regex_preformatter(regex[1])
        #print(regex)
        parsed = rp.parse(name, regex, temp)
        parse = parse + parsed + ','
        temp = None

    parse = parse[:-1]
    #print(parse)

    return parse + ']'
        
def readFile(fileName):
    regex = open(fileName, 'r')
    temp = ""
    temp_name = None
    regex_list = []
    for line in regex:
       #print("LINE ",line)
        for character in line:
            if(character != " " and character != "\n"):
                temp = temp + character
            if(character == " " and temp_name is None):
                temp_name = temp
                temp = ""
        temp_expr = temp
        regex_list.append((temp_name, temp_expr))
        temp = ""
        temp_name = None


    generate_scanner(regex_formatter(regex_list))
    
def generate_scanner(regex):

    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fileName = "58090030_scanner_" + time+".py"

    automaton_template = "scanner_template.py"

    template = open(automaton_template, 'r')
    out_file = open(fileName,'w')

    data_dump = regex
    data_dump = data_dump + '\n\n' + template.read()

    out_file.write(data_dump)
    out_file.close()


if __name__ == '__main__':
    inp = input("Please enter file name (default is in sampleRegex.txt): ")
    readFile(inp)
