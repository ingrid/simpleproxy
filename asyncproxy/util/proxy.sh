# Proxies!

read -d '' get_local_host_addr << "BLOCK"
import socket
print socket.gethostbyname(socket.gethostname())
BLOCK

local_host_addr=$(echo "$get_local_host_addr" | python)

teacup=$local_host_addr:'8000'
webscarab='localhost:8008'
none=''

function proxy(){
    local preset="${1:none}"
    export HTTP_PROXY=${!preset}
    export http_proxy=$HTTP_PROXY
}