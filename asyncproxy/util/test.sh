source ./proxy.sh

function test(){
    proxy teacup
    curl ingridcheung.com
    proxy none
}