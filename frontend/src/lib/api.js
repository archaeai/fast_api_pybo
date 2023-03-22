import qs from "qs"
import { access_token,username,is_login } from "./store"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

const fastapi = (operation,url,params,success_callback,failure_callback) => {
    // operation은 소문자만 처리 (get,post 등등 )
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    // qs를 사용해서 name=asd&age=30이놈을 dict타입으로 변경하거나 반대로 하거나 하는 행위등을 할 수 있다.
    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }

    let _url =import.meta.env.VITE_SERVER_URL + url

    
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }
    
    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== 'get') {
        options['body'] = body
    }
    
    fetch(_url, options)
        .then(response => {
            if(response.status === 204) {
                if(success_callback) {
                    success_callback()
                }
                return
                // return이 나오면 함수가 종료되기 떄문에, 불필요한 것들이 실행되는 것을 막기위해 return을 사용했다
            }
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {
                            success_callback(json)
                        }else if(operation !== 'login' && response.status === 401) {
                            access_token.set('')
                            username.set('')
                            is_login.set(false)
                            alert("로그인이 필요합니다")
                            push('/user-login')
                        }
                    }else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })
        })
}
export default fastapi