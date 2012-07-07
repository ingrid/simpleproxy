source ./proxy.sh

function test(){
    proxy teacup
    curl -L ingridcheung.com
    proxy none
}