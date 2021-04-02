
import shlex
import requests
import webbrowser
from subprocess import Popen, PIPE


''' FUNCTION TO EXECUTE EXTERNAL PYTHON SCRIPT AND GET ITS RETURNCODE, STDOUT AND STDERR '''

def execute_and_return(cmd):
    arguments = shlex.split(cmd)
    process = Popen(arguments, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    return output,error


''' FUNCTION TO GET THE ERROR TYPE AND ERROR MESSAGE '''

def error_type(error):
    error_message = error.decode("utf-8").strip().split('\r\n')[-1]
    return error_message


''' FUNCTION TO MAKE A HTTP GET REQUEST ''' 

def make_request(error):
    response = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return response.json()


''' FUNCTION TO GET LINKS WHICH RELATE TO STACK OVERFLOW THREADS '''

def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count = count+1
        if count == 3 or count == len(json_dict["items"]):
            break
    
    for i in url_list:
        webbrowser.open(i)   
    
    
''' CODE FOR THE WORKING FLOW OF AUTOSEARCH TOOL '''

if __name__ == "__main__":
    opt, err = execute_and_return("python test.py")
    err_msg = error_type(err)
    output = opt.decode("utf-8").strip().split('\r\n')[-1]
    print(err_msg)

    if err_msg:
        filter_error = err_msg.split(":")
        json_1 = make_request(filter_error[0])
        json_2 = make_request(filter_error[1])
        json_3 = make_request(err_msg)
        get_urls(json_1)
        get_urls(json_2)
        get_urls(json_3)

    else:
        print("NO ERRORS!!")
        print(output)

        


















