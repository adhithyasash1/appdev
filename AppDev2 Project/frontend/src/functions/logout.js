async function logout(url = 'http://localhost:8080/logout', data = {}) {
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
            'Content-Type': 'application/json',
            'Allow-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('Authentication-Token')
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json().then((response) => {
    if (response.meta.code === 200) {
    console.log(response);
    localStorage.removeItem('Authentication-Token');
    window.location.assign('/')
    }
    else {
        console.log(response);
    }
})}
export default logout