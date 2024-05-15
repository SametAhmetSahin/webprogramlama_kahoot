var baseurl = "http://localhost:8001"
$.support.cors = true

function readCookies() {
	let cookies = {}
	for (let item of document.cookie.split(";")) {
		let match = item.match(/^\s*([^]*?)="?([^]*?)"?\s*$/)
		if (match)
			cookies[match[1]] = decodeURIComponent(match[2])
	}
	return cookies
}

function clearCookies() {
    document.cookie += ";expires=Thu, 01 Jan 1970 00:00:00 GMT";
}

function setCookies(cookies) {
    clearCookies()
    for (var c in cookies) {
        document.cookie += ";"
        console.log(";" + c + "=" + cookies[c])
        document.cookie += c + "=" + cookies[c]
    }
    return document.cookie
}

function setCookie(key, value) {
    cookies = readCookies()
    
    console.log("key is " + cookies[key] + " val is " + value)
    cookies[key] = value
    console.log("final cookies " + JSON.stringify(cookies))
    return setCookies(cookies)
}

function checkLogin() {
    cookies = readCookies()

    var login = false
    
    if ("id" in cookies) {
        if (cookies["id"] != "") {
            login = true
        }
    }
    
    if (!login) {
        window.location.replace(`login.html`)
    }
}

function logout() {
    clearCookies()
    window.location.replace(`login.html`)
}

function get_request(url) {
    var res = undefined
    $.get({url: `${baseurl}${url}`, async: false}, (data, status) => {res = data})
    return res
}

function post_request(url, data) {
    var res = undefined
    console.log(data)
    console.log(JSON.stringify(data))
    $.post({url: `${baseurl}${url}`, async: false, data:JSON.stringify(data)}, (data, status) => {res = data})
    return res
}

async function toggleElementClass(element_name, sleep_time, first_class, second_class) {
    $(`#${element_name}`).removeClass(first_class);

    $(`#${element_name}`).addClass(second_class);

    await sleep(sleep_time*1000);

    $(`#${element_name}`).removeClass(second_class);
    $(`#${element_name}`).addClass(first_class);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}