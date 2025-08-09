#!/bin/bash

# 代理配置
PROXY_HOST=127.0.0.1
PROXY_PORT=10808
HTTP_PROXY_VAL="http://$PROXY_HOST:$PROXY_PORT"
SOCKS_PROXY_VAL="socks5://$PROXY_HOST:$PROXY_PORT"

# 获取当前活动的网络服务名称
function get_active_network_service() {
    local device
    # 首先尝试通过 scutil 获取主网络接口 (e.g., en0)
    device=$(scutil --nwi | grep 'Network interfaces' | awk -F': ' '{print $2}' | awk -F, '{print $1}')

    # 如果 scutil 失败，尝试通过 route 命令作为备用方案
    if [ -z "$device" ]; then
        device=$(route -n get default | grep 'interface:' | awk '{print $2}')
    fi

    if [ -z "$device" ]; then
        # 两个方法都失败了
        echo "错误：无法确定主网络设备。" >&2
        return 1
    fi

    # 根据设备名称 (e.g., en0) 获取网络服务名称 (e.g., Wi-Fi)
    # networksetup -listnetworkserviceorder 的输出格式如下:
    # (1) Wi-Fi
    # (Hardware Port: Wi-Fi, Device: en0)
    # 我们 grep 设备名称，并获取其前一行，然后提取服务名称
    local service
    service=$(networksetup -listnetworkserviceorder | grep -B 1 "Device: $device)" | head -n 1 | awk -F'\\) ' '{print $2}')
    
    if [ -z "$service" ]; then
        echo "错误：找不到设备 $device 对应的网络服务。" >&2
        return 1
    fi

    echo "$service"
    return 0
}


# 设置代理
function set_proxy() {
    local service
    service=$(get_active_network_service)
    if [ $? -ne 0 ] || [ -z "$service" ]; then
        echo "错误：无法设置代理，因为未能检测到活动的网络服务。请检查您的网络连接。" >&2
        return 1
    fi
    echo "为 '$service' 设置系统代理..."

    # 设置系统 HTTP, HTTPS 和 SOCKS 代理
    networksetup -setwebproxy "$service" $PROXY_HOST $PROXY_PORT
    networksetup -setsecurewebproxy "$service" $PROXY_HOST $PROXY_PORT
    networksetup -setsocksfirewallproxy "$service" $PROXY_HOST $PROXY_PORT

    # 为命令行设置环境变量
    export http_proxy=$HTTP_PROXY_VAL
    export https_proxy=$HTTP_PROXY_VAL
    export all_proxy=$SOCKS_PROXY_VAL
    export HTTP_PROXY=$HTTP_PROXY_VAL
    export HTTPS_PROXY=$HTTP_PROXY_VAL
    export ALL_PROXY=$SOCKS_PROXY_VAL
    
    # 设置 git 代理
    git config --global http.proxy $HTTP_PROXY_VAL
    git config --global https.proxy $HTTP_PROXY_VAL
    
    echo "系统和终端代理已开启"
    echo "HTTP 代理: $HTTP_PROXY_VAL"
    echo "SOCKS5 代理: $SOCKS_PROXY_VAL"
    echo "Git 代理已设置"
}

# 取消代理
function unset_proxy() {
    local service
    service=$(get_active_network_service)
    if [ $? -ne 0 ] || [ -z "$service" ]; then
        echo "错误：无法取消代理，因为未能检测到活动的网络服务。请检查您的网络连接。" >&2
        return 1
    fi
    echo "取消 '$service' 的系统代理..."

    # 关闭系统代理
    networksetup -setwebproxystate "$service" off
    networksetup -setsecurewebproxystate "$service" off
    networksetup -setsocksfirewallproxystate "$service" off

    # 取消环境变量
    unset http_proxy
    unset https_proxy
    unset all_proxy
    unset HTTP_PROXY
    unset HTTPS_PROXY
    unset ALL_PROXY
    
    # 取消 git 代理
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    
    echo "系统和终端代理已关闭"
    echo "Git 代理已取消"
}

# 查看代理状态
function show_proxy() {
    local service
    service=$(get_active_network_service)
    if [ $? -ne 0 ] || [ -z "$service" ]; then
        echo "错误：无法查看代理状态，因为未能检测到活动的网络服务。请检查您的网络连接。" >&2
        return 1
    fi
    
    echo "当前 '$service' 的系统代理设置："
    echo "网页代理 (HTTP):"
    networksetup -getwebproxy "$service"
    echo "安全网页代理 (HTTPS):"
    networksetup -getsecurewebproxy "$service"
    echo "SOCKS 防火墙代理:"
    networksetup -getsocksfirewallproxy "$service"
    echo ""
    echo "当前终端代理设置："
    echo "http_proxy: $http_proxy"
    echo "https_proxy: $https_proxy"
    echo "all_proxy: $all_proxy"
    echo ""
    echo "Git 代理设置:"
    echo "Git http proxy: $(git config --global --get http.proxy)"
    echo "Git https proxy: $(git config --global --get https.proxy)"
}

# 根据参数执行相应操作
case "$1" in
    "on")
        set_proxy
        ;;
    "off")
        unset_proxy
        ;;
    "show")
        show_proxy
        ;;
    *)
        echo "使用方法："
        echo "  source ./proxy.sh on   # 开启全局代理"
        echo "  source ./proxy.sh off  # 关闭全局代理"
        echo "  ./proxy.sh show        # 显示全局代理状态"
        ;;
esac
