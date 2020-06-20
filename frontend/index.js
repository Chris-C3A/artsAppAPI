const api = 'http://0.0.0.0:5000';

let User = {
    "username": "c3a",
    "password": "Password123"
}


async function login(user) {
    let response = await fetch(api+'/login', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    });
    let data = await response.json()
    return data;
}

async function getArts() {
    let response = await fetch(api+'/');
    return await response.json();
}

const say = () => {
    console.log("hello");
}
say();

let User = {
    id: 1,
    name: 'chris',
    getID: () => {
        return this.id;
    }
}


async function getImgFromId(img_id, img_ext) {
    let response = await fetch(api+'/get_image', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "img_id": img_id,
            "img_ext": img_ext
        })
    });
    const imgBlob = await response.blob()

    outside = URL.createObjectURL(imgBlob);
    let img = document.createElement("img");
    img.setAttribute('src', outside);
    document.getElementById("imgs").appendChild(img);
}

getArts().then(data => {
    for (let art of data) {
        console.log(art.img_id);
        getImgFromId(art.img_id, "jpeg")
            .catch(err => console.error(err));
    }
    console.log(data);
    console.log(`likes ${data[0].likes.length}`)
}).catch(err => console.error(err));
