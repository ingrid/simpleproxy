source ./proxy.sh

function test(){
    proxy teacup

    echo curl -L ingridcheung.com

    proxy none
}