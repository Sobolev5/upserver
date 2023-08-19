import re
import re


def parse_nginx_log(f_binary):

    # default nginx conf 
    '''
    log_format combined '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';    
    
    '''

    conf =  '$remote_addr - $remote_user [$time_local] '\
             '"$request" $status $body_bytes_sent ' \
             '"$http_referer" "$http_user_agent"'
    
    regex = ''.join(
        '(?P<' + g + '>.*?)' if g else re.escape(c)
        for g, c in re.findall(r'\$(\w+)|(.)', conf))
    
    parsed_lines = []   

    for f_line in f_binary.decode().split("\n"):
        
        if len(f_line) > 2000:
            continue

        try:
            matched = re.match(regex, f_line)
            if matched:
                raw_data = matched.groupdict()
                request = raw_data.pop("request")
                raw_data["request_method"], raw_data["request_uri"], *_ = request.split()

                if raw_data:
                    parsed_lines.append(raw_data)
        except:
            continue

    return parsed_lines
